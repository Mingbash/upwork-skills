# Quick start

1. Install a complete skill directory using the README instructions. Standard skill metadata follows [Agent Skills](https://agentskills.io/specification). Codex local installs can use `.agents/skills/<name>/`; Claude Code project installs use `.claude/skills/<name>/`. Check your agent version's directory support. No global configuration change is required.
2. In a fresh chat invoke `$skill-name` in Codex or `/skill-name` in Claude Code, replacing the name with the installed skill. You can also describe the task naturally; explicit invocation is easiest to verify.
3. Paste your task and evidence. For proposal/screening provide relevant experience and constraints, for profile creation provide confirmed facts, and for research provide job text. No live account is required.
4. Review the result and its source limitations. Request strict account readiness only when needed; an unavailable approved API does not prevent fit analysis. Ask to persist only if you need history.

## Dependencies and isolation

Python 3.9+ is optional for deterministic helpers. Install PyYAML in a chosen environment only if using screening YAML validation; no automatic package install is authorized. Every skill includes its own needed files.

Keep user records outside the installed skill and source repository. When testing an upgrade, copy into a disposable project and avoid overwriting an existing customized install. Examples are fictional, not client claims. See [validation](VALIDATION.md) for observed support rather than assuming every Agent Skills consumer was tested.
