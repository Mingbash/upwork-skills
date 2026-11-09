# Demand research method and record interface

## Sampling and evidence

Read only research preferences (or the explicit brief). Null scope means not set; use a clearly labeled exploratory sample rather than pretending a representative market census. Record query/theme, actual time window, source coverage, acquisition method, language, collection failures and screen/independent entry. Avoid sorting solely by high budgets or personal skill fit unless the research question requires it and the bias is disclosed.

Use assets/need.json for each sufficiently complete job. All need fields use `status` = explicit/inferred/not_stated, value, evidence, reason. Explicit requires a short quote or locator. Inferred requires rationale; not_stated keeps value null. Budget value when explicit is `{type: fixed|hourly, currency: <code>, amount: <number>}` OR `{type, currency, min, max}`. A range is not an exact quote. Empty, inferred or malformed budgets must not enter the posted-price distribution.

The workflow field describes what is purchased, e.g. input → business transformation → output → recipient; it is not a list of tool names. Preserve pain, current systems, desired outcome, acceptance, deadline and dependencies independently. Missing acceptance is not permission to invent it. Optional recommended acceptance belongs in analysis, labeled proposed.

Versions share job_id or canonical_url. Pasted material without a URL uses canonical_url: null and a stable source_locator such as input:brief-A/job-1, with source_kind: user_provided_text; this is not verified platform provenance. Preserve that locator across versions. The helper accepts either a canonical URL or source_locator, requires version and actual observation time, and returns locators as representative_links. Never merge different unlinked texts merely because they look similar. Deduplicate canonical links by removing tracking parameters/fragments while retaining any meaningful job identifier; do not equate merely similar URLs. Changed text creates a new version, not an extra buyer. Give confirmed repeated tasks from the same identified buyer a duplicate_group; separate different buyers even when they buy the same workflow. Unknown identities cannot prove independent buyers or prove sameness. Do not infer identity from geography/style.

## Deterministic aggregation

```text
python3 scripts/summarize_needs.py --input <records.json>
```

Python 3.9+ standard library only. Input is a JSON array of record versions; helper selects newest observed version per job_id or canonical_url. Equal-time conflicting versions raise an error. It validates structured evidence, counts unique jobs, known buyers, unknown-buyer records and need groups; groups confirmed same-buyer duplicates. Budget distributions use one representative (latest) per deduplicated need group. Output includes missing budget denominator, exact values and ranges separately by type/currency, duplicate and source counts. Numeric results do not perform semantic clustering or validate the truth of citations. Exit nonzero means repair input, not empty demand.

Budget missingness includes not_stated or inferred budget, reported separately. Preserve source job links and do not mix currencies or fixed/hourly values. Display sample counts; a small or biased sample supports hypotheses, not market-size or conversion claims. Unknown buyers are reported explicitly; distinct known buyers is a lower bound, not total market size.

## Interpret

For each cluster report purchased process, pain, recurring systems, desired deliverable and actually stated acceptance patterns, linked evidence, unique jobs/need groups/known buyers/unknown identities and budget missingness. Describe service opportunities as testable offers with the assumptions and buyer questions still open. Separate demand evidence from current user's delivery fit. A personal overlay requires explicit input and must not change source records or screen settings.
