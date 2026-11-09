# Validation and compatibility / 验证与兼容性

Checked 2026-11-09 for v0.1.0. The runtime probes below were run against the candidate. The release rechecked metadata and packaging after the copy edit.

## Automated checks

- 39 Python unit tests passed. Account identity/freshness boundaries, configurable age including zero, supplied exports vs live, partial newer balances, submitted/draft history, legacy configuration and run overrides, duplicate/unknown-buyer needs, separate currencies/rates and budget missingness, Unicode/inclusive milestone limits.
- All installed skill directories passed the local skill frontmatter validator. Environment notes moved into the body because the local validator did not support the newer optional compatibility frontmatter key.
- Each skill copied into an otherwise empty temporary directory passed standalone link/metadata checks. Shared Upwork contract copies are byte-identical.
- Distribution text passed the configured private-path/credential-marker scan. Archives use an explicit file allowlist; source baselines and public docs contain no personal workspace paths or account records.
- Original installed skills were compared against the frozen 34-file baseline and remained unchanged.

Run `python3 scripts/check_release.py` and `python3 -m unittest discover -s tests -v` to repeat the deterministic checks. Install requirements-dev.txt in your chosen test environment for PyYAML; the other helpers use the standard library.

## Actual Agent behavior

| Runtime / 环境 | Observed result / 已观察结果 | Limit / 边界 |
|---|---|---|
| Codex CLI 0.167.0-alpha.3.2 | Five synthetic tasks produced actual outputs; Profile, Proposal, Needs and Opportunity core behavior passed independent review. Screening's cross-job budget carryover was fixed and a standalone final regression passed. | The full five-task corrective rerun timed out; final screening behavior was revalidated separately. This is smoke coverage, not an exhaustive benchmark. |
| Claude Code 2.1.217 | Candidate directories were installed in an isolated project. An earlier CLI attempt received no model response. | Runtime testing is excluded from this release scope at the user’s request. No Claude Code behavior claim is made. |
| Other Agent Skills consumers | Standard SKILL.md package with local relative references. | Format portability only; runtime not tested. |

Five-task smoke coverage: Chinese profile creation without an account, Spanish proposal with Chinese analysis/no video/relative timing, English screening with missing account facts, demand analysis with duplicates and unknown buyers, and offline local-business evaluation. All data were synthetic. No external messages, applications, purchases or public profile edits occurred.

An independent agent also forward-tested the five skills and reviewed seven exact README excerpts, their translations, source context and privacy. Both reviews passed within the stated scopes; the initial runtime budget error is preserved in private evaluation evidence rather than hidden.

## Release scope / 发布范围

1. The MIT copyright notice is confirmed as Kudrat Kurban. Third-party references are linked and attributed; no third-party source content has been identified as bundled. Recheck if later revisions import such content.
2. The Codex samples cover the documented tasks. Claude Code remains outside the runtime test scope.

自动检查和已记录的 Codex 样例通过；按用户要求不再安排 Claude Code 实测，也不声明其行为已验证。所有原话追溯、原始快照和运行日志保留在候选仓库之外的私有审查目录，不进入下载包。
