---
name: upwork-bid-screen
description: Help a freelancer decide which Upwork jobs are worth applying to. Use job posts, their experience, and their time or price limits to rank the fit and flag open questions. When requested, check account readiness as a separate step.
license: MIT
---

# Upwork Bid Screen

Environment: Supplied text supports fit analysis. Strict account helper needs Python 3.9+; optional YAML validation also needs PyYAML. No bundled scraper or connector.

Read the [session/workspace contract](references/workspace.md) and [optional settings](references/options.md). Keep acquisition, account readiness, personal fit and economics separate. Default to **fit analysis**; strict account readiness is opt-in. Neither mode submits or spends.

## Fit analysis — default

1. Accept job text/files, explicit personal evidence or optional cached Profile, and current constraints. Do not require an account, resume search, existing Profile, workspace or another skill. Ask only for decision-changing gaps.
2. If a workspace was supplied, reload [preferences](references/configuration.md); otherwise use explicit in-chat constraints and show assumptions. Missing spending limits are unknown, not unlimited authorization.
3. Capture source locators, job IDs/URLs when available, observation times and coverage. Preserve changed versions. Record needs before personal exclusion using [needs handoff](references/needs-handoff.md).
4. Exclude known submitted applications from new-bid recommendations using supplied/local history. Drafts remain candidates. Without history, mark duplicate status unverified.
5. Apply hard eligibility before [fit and economics](references/decision-method.md). Unknown hard requirements are holds, not passes. Soft preferences affect ranking, not silent exclusion.
6. Return fit ranking, evidence, scope, conditional pricing and decisive unresolved conditions. Label **account readiness unverified** unless separately checked. Do not claim a live balance, complete application history or current ability to apply.

## Strict account readiness — explicit mode

First read [account contract](references/account.md). Establish the intended account and attempt a permitted approved API capability check. No connector means a failed capability check, not a platform read. User-provided exports can supply historical evidence but never become live observations.

Run the account helper with this attempt, historical snapshots and configured maximum age (default 72 hours). Observed identity mismatch blocks readiness even when a matching cache exists. Live success, historical fallback and blocked readiness are different states. Blocked readiness does not suppress useful fit analysis; it suppresses a verified-ready-to-apply conclusion. Apply newer partial facts, known submissions, spending and restrictions conservatively without relabeling a cache live.

Check available Connects (platform application credits), active workload, pending offers, known applications and user spending/capacity limits. Historical evidence supports conditional advice only. No helper result authorizes spending or submission.

## Deliver and persist

Return in chat by default. When requested, save a new immutable run with source versions, effective options/constraints, exclusions, ranking, economics, account status and unknowns. Cached output shows actual observation time, age, live failure and missing-new-activity risk. Read script interfaces before executing; without runtime, give qualitative analysis and state which checks were not performed. Do not buy Connects, Boost, send, submit, accept offers or schedule tasks.
