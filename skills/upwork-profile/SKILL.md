---
name: upwork-profile
description: Write, import, review, or update an Upwork freelancer profile from supplied profile text or project experience. Draft a title and overview that make it clear what the freelancer can do and what work supports each claim.
license: MIT
---

# Upwork Profile

Environment: Works from supplied text; optional filesystem persistence. No required connector or script runtime.

Read the [session/workspace contract](references/workspace.md) and [optional settings](references/options.md). Respond in the user's language unless configured otherwise. Creation, import, audit and refresh are different operations; none publishes online.

## Choose the evidence source

- **Create:** accept explicitly supplied experience, resumes, cases or user-confirmed facts. Draft a title, overview and relevant proof suggestions. Label the result a new profile draft, not an imported account. Ask only for material missing facts; do not invent tenure, availability, credentials, reviews or metrics.
- **Load:** if the selected workspace contains populated `reference/profile.md`, use its version and provenance. A blank template is not evidence. Do not refresh it automatically during screening or proposal work.
- **Import:** accept provided profile text/export, or a permitted approved API source. Confirm the intended identity when associating material with an account. Use the [profile template](assets/profile.md). Label a supplied export as such; do not claim a live read.
- **Refresh/correct:** only on request; preserve the previous version before updating a local current copy. Keep user-confirmed corrections separate from still-published text. No workspace is required for an in-chat revision.

## Audit and draft

Match positioning, title, opening, portfolio and proof to the buyer outcomes the user wants to serve. Show actual contribution, process, deliverables and supported results. Distinguish demonstrated ability from a service the user wants to sell. Produce proposed copy and a compact internal claim-to-source ledger with material unresolved questions.

Use only explicitly supplied supplements or an explicit manifest. Mark conflicts, omit unresolved conflicting claims from proposed copy, and never attribute resume content to an Upwork Profile. Lack of a resume or live account is not a blocker when adequate supplied evidence exists.

Before advising on mutable platform features, contact rules or ranking claims, read [rule sources](references/sources.md) and verify the relevant current rule. Relevance and specificity are professional heuristics, not promises of impressions or hires.

Deliver copy plus provenance/limitations in chat; if persistence was requested, save the audit and source versions in a new run. Keep internal notes separate from copy-ready text. No automatic profile edits, messages or purchases.
