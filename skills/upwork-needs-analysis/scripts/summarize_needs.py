#!/usr/bin/env python3
"""Summarize versioned buyer evidence without profile or account inputs."""
import argparse
from collections import Counter
from datetime import datetime
import json
import math
from pathlib import Path
import sys

FIELDS = {'scenario','workflow','pain','systems','inputs','outputs','outcome','acceptance','budget','deadline','dependencies'}


def timestamp(value):
    t = datetime.fromisoformat(value.replace('Z','+00:00'))
    if t.tzinfo is None:
        raise ValueError('observation needs timezone')
    return t


def nonnegative(v):
    return type(v) in (int,float) and math.isfinite(v) and v >= 0


def locator(record):
    return record.get('canonical_url') or record.get('source_locator')


def validate(record):
    if not (record.get('job_id') or locator(record)):
        raise ValueError('record needs job ID or canonical URL')
    if record.get('source_entry') not in {'screen','research'}:
        raise ValueError('source_entry must be screen or research')
    if record.get('buyer_id') is not None and not isinstance(record['buyer_id'], str):
        raise ValueError('buyer_id must be string or null')
    if record.get('duplicate_group') is not None and not isinstance(record['duplicate_group'], str):
        raise ValueError('duplicate_group must be string or null')
    if not record.get('version') or not isinstance(locator(record), str) or not locator(record):
        raise ValueError('version and canonical_url or source_locator required for provenance')
    time = timestamp(record['observed_at'])
    if timestamp(record['first_observed_at']) > time:
        raise ValueError('first observation later than version observation')
    fields = record.get('fields',{})
    if set(fields) != FIELDS:
        raise ValueError('record needs all demand fields; use not_stated for missing facts')
    for name, field in fields.items():
        status = field.get('status')
        if status not in {'explicit','inferred','not_stated'}:
            raise ValueError('invalid evidence status: '+name)
        if status == 'explicit' and (field.get('value') is None or not field.get('evidence')):
            raise ValueError('explicit fact needs value and evidence: '+name)
        if status == 'inferred' and (field.get('value') is None or not field.get('reason')):
            raise ValueError('inference needs value and reason: '+name)
        if status == 'not_stated' and field.get('value') is not None:
            raise ValueError('not_stated must be null: '+name)
    b = fields['budget']
    if b['status'] == 'explicit':
        v = b['value']
        if not isinstance(v,dict) or v.get('type') not in {'fixed','hourly'} or not isinstance(v.get('currency'),str) or not v['currency']:
            raise ValueError('explicit budget needs type and currency')
        if 'amount' in v:
            if 'min' in v or 'max' in v or not nonnegative(v['amount']):
                raise ValueError('budget must have exact amount OR range')
        elif not (nonnegative(v.get('min')) and nonnegative(v.get('max')) and v['min'] <= v['max']):
            raise ValueError('invalid budget range')
    return time


def summarize(records):
    if not isinstance(records,list):
        raise ValueError('input must be a list of record versions')
    # Bridge URL-only captures to a later known ID. Conflicting IDs stay an error.
    ids_by_url = {}
    for r in records:
        validate(r)
        if r.get('job_id'):
            url = locator(r)
            if url in ids_by_url and ids_by_url[url] != r['job_id']:
                raise ValueError('canonical URL maps to conflicting job IDs')
            ids_by_url[url] = r['job_id']
    latest = {}
    for r in records:
        key = ('id', r.get('job_id') or ids_by_url.get(locator(r))) if r.get('job_id') or locator(r) in ids_by_url else ('url',locator(r))
        time = timestamp(r['observed_at'])
        previous = latest.get(key)
        if previous and time == previous[0] and r != previous[1]:
            raise ValueError('conflicting equal-time versions')
        if not previous or time > previous[0]:
            latest[key] = (time,r)
    groups = {}
    buyers = set()
    unknown = 0
    for key,(time,r) in latest.items():
        buyer = r.get('buyer_id')
        if buyer:
            buyers.add(buyer)
        else:
            unknown += 1
        group = ('duplicate',buyer,r['duplicate_group']) if buyer and r.get('duplicate_group') else ('job',key)
        if group not in groups or time > groups[group][0]:
            groups[group] = (time,r)
    budgets = {}
    missing = Counter()
    links = []
    for _,r in groups.values():
        links.append(locator(r))
        b = r['fields']['budget']
        if b['status'] != 'explicit':
            missing[b['status']] += 1
            continue
        v = b['value']
        key = v['type'] + '/' + v['currency'].upper()
        group = budgets.setdefault(key, {'exact':[], 'ranges':[], 'sample_count':0})
        group['sample_count'] += 1
        if 'amount' in v:
            group['exact'].append(v['amount'])
        else:
            group['ranges'].append([v['min'],v['max']])
    for group in budgets.values():
        group['exact'].sort()
        group['ranges'].sort()
    total = len(groups)
    entries = Counter(r['source_entry'] for _,r in latest.values())
    return {'input_versions':len(records), 'unique_jobs':len(latest),
            'need_groups':total, 'collapsed_duplicate_jobs':len(latest)-total,
            'known_distinct_buyers':len(buyers), 'unknown_buyer_jobs':unknown,
            'source_jobs':dict(entries),
            'source_share':{k:v/len(latest) for k,v in entries.items()},
            'budget_denominator':'deduplicated_need_groups_latest_representative',
            'budget_missing':sum(missing.values()),'budget_missing_by_status':dict(missing),
            'budget_missing_ratio':sum(missing.values())/total if total else None,
            'posted_budgets':budgets,'representative_links':links,
            'limitations':['Posted budgets are not paid prices.','Unknown buyers do not establish independence.','Semantic duplicate labels require evidence; the helper does not infer them.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(summarize(json.loads(Path(args.input).read_text())),indent=2,allow_nan=False))
    except (ValueError,TypeError,KeyError,OSError,AttributeError) as exc:
        print(json.dumps({'error':str(exc)}),file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
