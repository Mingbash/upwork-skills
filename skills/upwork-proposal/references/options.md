# Optional run options

All skills work with defaults. Read an explicitly supplied options object, or optional `reference/options.json` in the selected workspace. A user may express the same options in ordinary language. Missing fields get defaults; unknown fields or invalid values need correction, not silent ignoring. Record effective options only when saving a run. Do not make users fill every field.

| Field | Default | Meaning |
|---|---|---|
| `analysis_language` | `auto` | Follow the user's language, or use an explicit language name/code. |
| `client_language` | `auto` | Explicit client/user requirement first, then job language, otherwise English. |
| `required_assets` | `[]` | List of `{label, url}` objects the user requires. Missing/unverified items remain internal unresolved items, never invented links. |
| `fixed_lines` | `[]` | User-requested literal lines. Unsupported claims or prohibited content cannot override evidence rules; flag the conflict. |
| `video_outline` | `false` | Produce an optional generic demo/video outline; no required vendor. |
| `milestone_max_chars` | `null` | Optional positive integer, inclusive maximum in Unicode code points. This is a writing setting, not an asserted Upwork limit. Confirm actual destination limits when relevant. |
| `start_date` | `null` | Explicit ISO calendar date. Without it, use relative durations after access/approval, not invented dates. |
| `account_cache_max_hours` | `72` | Nonnegative finite hours; zero disables fallback. Historical snapshots never authorize spending. |

Use the blank `assets/options.json` included inside this skill directory when the user wants to save settings. Python helpers do not automatically discover these options: pass `account_cache_max_hours` as `max_age_hours` in the account request, and `milestone_max_chars` as `--max-chars` to the milestone helper when set. The agent validates other option types and records precedence. Screening YAML remains its own schema; never insert these fields there.

Old workspaces without options keep these defaults without being rewritten. Existing explicit user rules still apply unless revised, but must not be misrepresented as platform requirements. For legacy 'fewer than 200 characters', the equivalent configured inclusive limit is 199.

## Example

```json
{"analysis_language":"zh","client_language":"auto","required_assets":[],"fixed_lines":[],"video_outline":false,"milestone_max_chars":null,"start_date":null,"account_cache_max_hours":72}
```
