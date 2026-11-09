---
name: upwork-needs-analysis
description: Find recurring buyer needs in a set of Upwork posts or a research brief. Group jobs by the work buyers want done, the systems they use, and how they’ll accept delivery. Keep jobs that the current freelancer would skip in the research sample.
license: MIT
---

# Upwork Needs Analysis

Environment: Works from pasted jobs or supplied files. Optional Python 3.9+ aggregation helper uses the standard library.

Use jobs as scoped buyer-demand evidence, not a keyword list. Read the [session/workspace contract](references/workspace.md), [research method](references/research-method.md) and [optional settings](references/options.md).

## Independent inputs

Accept pasted jobs, explicitly supplied files, screening captures (including rejected/applied jobs), or an independent brief. Optional persistent scope lives in `reference/research-preferences.md`; neither a Profile, Connects balance nor workspace is required. Never load personal screening filters for research. Permitted source access affects collection coverage, not whether demand exists. Do not automate Upwork browsing or scrape pages.

## Capture and aggregate

For a small one-off task, use an evidence table in chat. For structured aggregation or persistence, use [blank need record](assets/need.json). Preserve explicit statements with quotes/locators, reasoned inferences with rationale and not-stated values separately. Do not turn proposed acceptance criteria into buyer requirements.

Version by job ID or canonical URL and do not count versions as new jobs. For text with no source URL, use a clearly labeled stable local input locator and disclose unverified platform provenance; never fabricate an Upwork URL. Confirm buyer identity only when supported; unknown buyers stay unknown. Same-buyer duplicate tasks must not inflate independent demand.

Group by business process/pain, system combination and delivery/acceptance pattern. Report unique jobs, conservative need groups, confirmed buyers, unknown-buyer records, sample window and source mix. Read the helper interface before optional execution. Numeric aggregation cannot replace evidence reading or semantic clustering.

Posted budgets are not paid prices. Separate fixed/hourly, currencies, exact amounts/ranges, absent/inferred values and duplicates; state denominators. Keyword frequency and a few large budgets do not establish demand strength.

Deliver service hypotheses with source locators, independent-buyer support, uncertainty and next validation. Personal ability overlay is opt-in and separate. Save only when requested; never modify Profile, screening preferences, prices or schedules.
