---
schema_version: 1
version: 1
goal:
  amount:
    value: null
    mode: context
  currency:
    value: null
    mode: context
  basis:
    value: null
    mode: context
  window_start:
    value: null
    mode: context
  window_end:
    value: null
    mode: context
contract:
  types:
    value: null
    mode: soft
  currency:
    value: null
    mode: soft
  budget_min:
    value: null
    mode: soft
  budget_max:
    value: null
    mode: soft
  hourly_min:
    value: null
    mode: soft
  hourly_max:
    value: null
    mode: soft
  scope:
    value: null
    mode: soft
connects:
  per_application_max:
    value: null
    mode: hard
  period_max:
    value: null
    mode: hard
  period_start:
    value: null
    mode: context
  period_end:
    value: null
    mode: context
  reserve:
    value: null
    mode: hard
  boost:
    value: null
    mode: soft
capacity:
  hours_per_week:
    value: null
    mode: hard
  timezone:
    value: null
    mode: context
  overlap:
    value: null
    mode: soft
  deadline:
    value: null
    mode: hard
search:
  topics:
    value: null
    mode: soft
  exclusions:
    value: null
    mode: soft
  qualifications:
    value: null
    mode: hard
  candidate_count:
    value: null
    mode: soft
score:
  weights:
    value: null
    mode: context
  rubrics:
    value: null
    mode: context
  tiers:
    value: null
    mode: context
  evidence_requirements:
    value: null
    mode: context
schedule:
  enabled:
    value: false
    mode: context
  frequency:
    value: null
    mode: context
  timezone:
    value: null
    mode: context
  notification:
    value: null
    mode: context
platform_filters:
  feed:
    value: null
    mode: context
  payment_verified:
    value: null
    mode: soft
  previous_clients_only:
    value: null
    mode: soft
  experience_levels:
    value: null
    mode: soft
  proposal_ranges:
    value: null
    mode: soft
  client_hires:
    value: null
    mode: soft
---

# Preferences

Null means unset. Every run reloads this file. Hard constraints gate recommendations; soft values express tradeoffs; context values describe the task. Fill values for this user only. A run override does not persist.

Goal basis: contract or net. Contract types: fixed/hourly. Budget/rate fields use the configured currency. Connects period caps require explicit dates. Scores need both weights and a usable rubric; otherwise use qualitative reasons. Scheduling remains a separate user-authorized action.
