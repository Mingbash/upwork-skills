#!/usr/bin/env python3
"""Read-only account fallback and preference validation. No network or writes."""
import argparse
import copy
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sys

CORE = ('identity', 'connects', 'applications', 'offers', 'contracts')


def instant(value):
    if not isinstance(value, str):
        raise ValueError('timestamp must be an ISO string with timezone')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timestamp has no timezone')
    return result.astimezone(timezone.utc)


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def complete(check, expected, now):
    try:
        if not check.get('check_id') or check.get('account_id') != expected:
            return None
        started = instant(check['attempted_at'])
        fields = check['fields']
        times = []
        for key in CORE:
            field = fields[key]
            if field['status'] != 'ok' or not field.get('source'):
                return None
            time = instant(field['observed_at'])
            if not started <= time <= now:
                return None
            times.append(time)
        if fields['identity']['value'] != expected:
            return None
        balance = fields['connects']['value']
        if not number(balance) or balance < 0:
            return None
        for key in ('applications', 'offers', 'contracts'):
            value = fields[key]['value']
            if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
                return None
        return min(times)
    except (KeyError, TypeError, ValueError, AttributeError):
        return None


def account(request):
    max_age = request.get('max_age_hours', 72)
    if not number(max_age) or max_age < 0:
        raise ValueError('max_age_hours must be nonnegative finite numeric')
    expected = request.get('expected_account')
    if not isinstance(expected, str) or not expected:
        raise ValueError('expected_account is required')
    now = instant(request['now'])
    live = request.get('live')
    if not isinstance(live, dict) or not live.get('check_id'):
        raise ValueError('this run must supply an attempted live check')
    if instant(live['attempted_at']) > now:
        raise ValueError('live attempt is in the future')
    identities = [live.get('account_id')]
    identity = live.get('fields', {}).get('identity', {})
    if identity.get('status') == 'ok':
        identities.append(identity.get('value'))
    if any(x is not None and x != expected for x in identities):
        return {'status': 'blocked', 'reason': 'observed_account_mismatch'}
    observed = complete(live, expected, now) if live.get('source_kind') == 'approved_api' else None
    selected = live
    status = 'live'
    reason = None
    if observed is None:
        reason = live.get('failure_reason') or 'incomplete_or_invalid_live_core_fields'
        candidates = []
        # Supplied complete exports and legacy envelopes stay historical.
        for snap in request.get('snapshots', []) + [live]:
            stamp = complete(snap, expected, now)
            if stamp is not None and max_age > 0 and 0 <= (now - stamp).total_seconds() <= max_age * 3600:
                candidates.append((stamp, snap))
        if not candidates:
            return {'status': 'blocked', 'reason': reason, 'cache_reason': 'no_complete_same_account_snapshot_within_configured_age'}
        observed, selected = max(candidates, key=lambda pair: pair[0])
        status = 'cached'
    excluded = set()
    def add_jobs(items):
        for item in items:
            if item.get('status') != 'draft' and item.get('job_id'):
                excluded.add(str(item['job_id']))
    add_jobs(selected['fields']['applications']['value'])
    add_jobs(selected['fields']['offers']['value'])
    add_jobs(selected['fields']['contracts']['value'])
    newer_balance = None
    # Partial facts must have same-account provenance and a valid newer observation.
    if live.get('account_id') == expected:
        for key in ('applications', 'offers', 'contracts', 'connects'):
            field = live.get('fields', {}).get(key, {})
            try:
                valid = (field.get('status') == 'ok' and field.get('source') and
                         observed <= instant(field['observed_at']) <= now and
                         instant(live['attempted_at']) <= instant(field['observed_at']))
            except (KeyError, TypeError, ValueError):
                valid = False
            if not valid:
                continue
            value = field.get('value')
            if key == 'connects' and number(value) and value >= 0:
                newer_balance = value
            elif key != 'connects' and isinstance(value, list) and all(isinstance(x, dict) for x in value):
                add_jobs(value)
    local = request.get('local_submissions', [])
    if not isinstance(local, list) or any(not isinstance(x, dict) for x in local):
        raise ValueError('local_submissions must be a list of objects')
    for item in local:
        if item.get('account_id') != expected or not item.get('source'):
            raise ValueError('local submissions need same-account provenance')
        if instant(item['submitted_at']) > now:
            raise ValueError('local submission is in the future')
    add_jobs(local)
    balance = selected['fields']['connects']['value']
    return {
        'status': status, 'reason': reason, 'check_id': selected['check_id'],
        'observed_at': observed.isoformat(), 'age_seconds': (now-observed).total_seconds(),
        'balance': balance,
        'source_kind': selected.get('source_kind', 'legacy_unverified'),
        'max_age_hours': max_age,
        'newer_observed_balance': newer_balance,
        'conservative_balance_before_unreconciled_spending': min(balance, newer_balance) if newer_balance is not None else balance,
        'excluded_job_ids': sorted(excluded),
        'balance_label': 'observed_this_check' if status == 'live' else 'historical_not_current',
        'spending_authorized': False,
        'warning': 'Post-snapshot spending, submissions and workload may be missing.' if status == 'cached' else None,
    }


def load_preferences(path):
    try:
        import yaml
    except ImportError as exc:
        raise ValueError('config requires PyYAML; account checks do not') from exc

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError('duplicate YAML key: ' + str(key))
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    # Date scalars stay strings so the same configuration serializes reproducibly.
    UniqueLoader.yaml_implicit_resolvers = {
        k: [(tag, rx) for tag, rx in v if tag != 'tag:yaml.org,2002:timestamp']
        for k, v in UniqueLoader.yaml_implicit_resolvers.items()
    }
    lines = Path(path).read_text().splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('preferences need YAML frontmatter')
    try:
        end = lines.index('---', 1)
        data = yaml.load('\n'.join(lines[1:end]), Loader=UniqueLoader)
    except (ValueError, yaml.YAMLError) as exc:
        raise ValueError('invalid preferences: ' + str(exc)) from exc
    return data


def validate(data, template):
    # Optional additive v1 extension: existing workspaces remain valid.
    if isinstance(data, dict) and 'platform_filters' not in data and 'platform_filters' in template:
        data = dict(data, platform_filters=copy.deepcopy(template['platform_filters']))
    if not isinstance(data, dict) or set(data) != set(template):
        raise ValueError('configuration keys must match schema v1')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('unsupported schema_version')
    if type(data['version']) is not int or data['version'] < 1:
        raise ValueError('version must be a positive integer')
    numeric = {'amount','budget_min','budget_max','hourly_min','hourly_max',
               'per_application_max','period_max','reserve','hours_per_week','candidate_count'}
    lists = {'types','topics','exclusions','qualifications','evidence_requirements',
             'experience_levels','proposal_ranges','client_hires'}
    maps = {'weights','rubrics','tiers'}
    for group, defaults in template.items():
        if not isinstance(defaults, dict):
            continue
        if not isinstance(data[group], dict) or set(data[group]) != set(defaults):
            raise ValueError('invalid fields in ' + group)
        for key, default in defaults.items():
            leaf = data[group][key]
            label = group + '.' + key
            if not isinstance(leaf, dict) or set(leaf) != {'value','mode'}:
                raise ValueError(label + ' requires value and mode')
            mode, value = leaf['mode'], leaf['value']
            allowed = {'context'} if default['mode'] == 'context' else {'hard','soft'}
            if mode not in allowed:
                raise ValueError('invalid mode: ' + label)
            if value is None:
                continue
            if key in numeric:
                if not number(value) or value < 0:
                    raise ValueError(label + ' must be nonnegative finite numeric')
                if key in {'per_application_max','period_max','reserve','candidate_count'} and type(value) is not int:
                    raise ValueError(label + ' must be integer')
            elif key in lists:
                if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
                    raise ValueError(label + ' must be a list of strings')
            elif key in maps:
                if not isinstance(value, dict):
                    raise ValueError(label + ' must be a mapping')
            elif key in {'enabled','boost','payment_verified','previous_clients_only'}:
                if type(value) is not bool:
                    raise ValueError(label + ' must be boolean')
            elif not isinstance(value, str):
                raise ValueError(label + ' must be a string')
    def val(g,k): return data[g][k]['value']
    filters = data.get('platform_filters', {})
    enums = {
        'experience_levels': {'entry','intermediate','expert'},
        'proposal_ranges': {'lt5','5to10','10to15','15to20','20to50'},
        'client_hires': {'none','1to9','10plus'},
    }
    for key, allowed in enums.items():
        values = filters.get(key, {}).get('value')
        if values is not None and (not set(values) <= allowed or len(set(values)) != len(values)):
            raise ValueError('invalid platform_filters.' + key)
    if filters.get('feed', {}).get('value') is not None and not filters['feed']['value'].strip():
        raise ValueError('invalid platform_filters.feed')
    if val('goal','basis') not in (None,'contract','net'):
        raise ValueError('goal.basis must be contract or net')
    if val('contract','types') is not None and not set(val('contract','types')) <= {'fixed','hourly'}:
        raise ValueError('contract.types must use fixed/hourly')
    for lo,hi in [('budget_min','budget_max'),('hourly_min','hourly_max')]:
        a,b=data['contract'][lo],data['contract'][hi]
        if a['value'] is not None and b['value'] is not None and a['value'] > b['value'] and a['mode']==b['mode']=='hard':
            raise ValueError('inverted hard contract bounds: '+lo)
    for group,lo,hi in [('goal','window_start','window_end'),('connects','period_start','period_end')]:
        a,b=val(group,lo),val(group,hi)
        parsed_a,parsed_b=instant(a) if a else None,instant(b) if b else None
        if parsed_a and parsed_b and parsed_a >= parsed_b:
            raise ValueError('invalid time window: '+group)
    if val('connects','period_max') is not None and not all(val('connects',x) for x in ['period_start','period_end']):
        raise ValueError('period cap needs start and end')
    if val('capacity','deadline') is not None:
        instant(val('capacity','deadline'))
    weights=val('score','weights')
    if weights is not None:
        if not weights or any(not number(v) or v < 0 for v in weights.values()) or sum(weights.values()) <= 0:
            raise ValueError('score weights must be nonnegative with positive total')


def config(request):
    template = load_preferences(Path(__file__).resolve().parents[1] / 'assets/preferences.md')
    saved = load_preferences(request['path'])
    validate(saved, template)
    effective = copy.deepcopy(saved)
    if 'platform_filters' not in effective and 'platform_filters' in template:
        effective['platform_filters'] = copy.deepcopy(template['platform_filters'])
    overrides = request.get('overrides', {})
    if not isinstance(overrides, dict):
        raise ValueError('overrides must be a mapping')
    for group, leaves in overrides.items():
        if group not in effective or not isinstance(effective[group], dict) or not isinstance(leaves, dict):
            raise ValueError('invalid override group')
        for key, leaf in leaves.items():
            if key not in effective[group]:
                raise ValueError('unknown override field')
            effective[group][key] = copy.deepcopy(leaf)
    validate(effective, template)
    return {'saved_version': saved['version'], 'effective': effective, 'overrides': overrides}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['account','config'])
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    try:
        request = json.loads(Path(args.input).read_text())
        result = account(request) if args.mode == 'account' else config(request)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, TypeError, KeyError, OSError, AttributeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
