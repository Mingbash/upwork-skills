# Strict account evidence and guard v1.1

This contract applies only to explicitly requested strict readiness checks. Default fit analysis needs no account. There is no bundled adapter: discover an approved API integration whose permitted scope covers the operation. A callable browser/connector is not permission. No automated login browsing, scraping or browser-cookie access. If no permitted capability is available, record its absence once as a failed capability check and continue with supplied evidence. Do not pretend an account page was read.

## Evidence envelope

```json
{
  "check_id": "unique-run-check",
  "attempted_at": "2026-01-01T12:00:00Z",
  "account_id": null,
  "source_kind": "user_provided_export",
  "failure_reason": "no approved API capability available",
  "fields": {
    "identity": {"status": "unknown", "value": null, "observed_at": null, "source": null},
    "connects": {"status": "unknown", "value": null, "observed_at": null, "source": null},
    "applications": {"status": "unknown", "value": null, "observed_at": null, "source": null},
    "offers": {"status": "unknown", "value": null, "observed_at": null, "source": null},
    "contracts": {"status": "unknown", "value": null, "observed_at": null, "source": null}
  },
  "optional": {}
}
```

`source_kind` is approved_api, user_provided_export, user_confirmed, or legacy_unverified. Only a complete current approved_api envelope can produce `live`. The agent verifies actual authorization and provenance; the helper cannot prove truth from a label. Old envelopes with no kind remain historical/legacy_unverified, not verified live reads. Do not relabel them.

Core fields are identity, Connects, submitted applications, pending offers and active contracts. Collect workload/deadlines only where available; contract count does not establish capacity. Additional historical performance metrics are optional, not a mandatory 30-day collection task.

Successful fields have status ok, real observation time and source locator. Identity value equals account_id. Connects is finite nonnegative numeric; other core values are lists of objects with job ID or canonical URL, status and relevant visible details. Observed empty lists are []; failed reads are null/unknown. A check uses one account and check_id. Times fall between that check's attempted_at and evaluation time. Never assemble old fields into a new live check. Oldest core observation determines snapshot age.

For supplied exports, preserve source observation/capture time, not import time; if unavailable, strict freshness cannot be established. Keep source assertions and user confirmations distinct. In a requested workspace save attempts and complete snapshots immutably under state/account; otherwise operate on supplied evidence in memory.

## Helper

Python 3.9+, standard library only, no network or writes:

```text
python3 scripts/screen_guard.py account --input request.json
```

Request fields: `expected_account`, timezone-aware `now`, this run's `live` attempt, list `snapshots`; optional `max_age_hours` (default 72) and `local_submissions` (default []). Each local submission has same `account_id`, `job_id`, `status`, timezone-aware `submitted_at`, and source locator. Read CLI output status; exit 0 means computation completed, not approval to apply.

Observed account mismatch blocks even if a matching cache exists. Complete same-account snapshots with age <= configured maximum may support cached advice. Boundary is inclusive; zero disables fallback. Future/naive/inconsistent timestamps are invalid. A supplied complete export in live is treated as historical, never live. `blocked` concerns readiness, not job fit.

The result exposes source kind, original time/age, failure, historical balance, a newer lower observation where valid and excluded_job_ids from supplied applications/offers/contracts plus local submissions. This is not a full eligibility engine or spending ledger. Drafts stay candidates; submitted/withdrawn applications remain follow-up/history, not new recommendations. For URL-only histories the agent must also dedupe canonical URLs. A newer restriction blocks readiness even if a numeric balance exists.

Reconcile known post-snapshot spending with unique transaction IDs, times and pending/posted status before recommending any budget. Do not double-subtract amounts already in an observed balance. The helper's conservative balance is explicitly BEFORE unreconciled spending; unknown activity remains a risk. Partial newer fields never turn the selected cache live. Historical advice is conditional and must disclose missing-new-activity risk. No status authorizes spending, messaging or submission.
