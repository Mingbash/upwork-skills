# Generalization ledger

| Area | Keep | Configure / add | Remove |
|---|---|---|---|
| All | Evidence provenance, no implicit external actions | In-chat use, optional workspace, separate language/options | Mandatory workspace setup, global resume discovery |
| Profile | Actual contribution and conflict handling | Create from supplied experience; distinguish user draft/import | Existing Upwork Profile as prerequisite |
| Proposal | Buyer decision, relevant proof, scope and costs | Assets, fixed lines, video, language, inclusive cap, relative timing | Mandatory Loom, English milestones, hardcoded 199 cap, invented calendar dates |
| Screening | Hard vs soft filters, unknowns, costs, duplicate history | Fit default; strict opt-in; configurable cache; source kinds | Login-first gate, browser fallback, private screenshot dependency |
| Needs | Dedup, unknown buyers, budget denominators | Pasted input locators and one-off evidence tables | Profile/account eligibility contamination |
| Maintenance | Existing v1 YAML meaning | Additive options.json; standalone contract copies | Shared runtime dependency on sibling directories |

## Public interfaces

`reference/options.json` is optional and additive; see each skill's references/options.md. Existing screening YAML is read without rewriting and its absent optional platform_filters are defaulted in memory. New feed strings are source-specific preferences, not proof of availability.

Account helper adds optional max_age_hours and local_submissions. Legacy snapshots without source_kind can be historical evidence, never current verified API reads. Results add source_kind, max_age_hours, newer_observed_balance, conservative_balance_before_unreconciled_spending and excluded_job_ids; original fields remain. Missing timestamps are not repaired by import time.

Need records add source_locator/source_kind and allow a null canonical_url when a stable supplied-input locator exists. Old records remain accepted. Milestone helper now counts only by default, with optional inclusive --max-chars; old strict-less-than-200 behavior is explicitly selected with --max-chars 199. This intentional CLI behavior change avoids presenting a personal convention as a platform rule.
