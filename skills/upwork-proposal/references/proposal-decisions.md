# Evidence-backed proposal decisions

Choose proof that helps a buyer judge a specific requirement, delivery risk or acceptance condition. A real name is optional personalization, not an algorithm advantage. Do not invent a current alternative, familiarity, metrics or availability.

Use milestones when the buyer requires them or work has independent acceptance gates, external dependencies or significant handover risk. A small coherent deliverable may use one milestone; unknown access/data quality may justify paid discovery before quoting implementation. Never split by an arbitrary dollar threshold.

Each milestone has a title, amount/currency, client-language description and timing. Keep the plan identical in client copy and pricing notes. Use relative timing such as '3 working days after receiving approved source files' when start/access is unknown. Calendar dates require a stated start/access assumption. Acceptance criteria suggested by the agent remain proposed until agreed.

Descriptions have no universal length setting here. A configured `milestone_max_chars` is inclusive. Validate after final edits, report the count internally, and keep acceptance/exclusions outside a short destination field when needed. This helper counts Unicode code points, not bytes, graphemes or platform-specific UTF-16 units; confirm destination behavior when it matters. Do not assert a platform character limit without source evidence.

## Milestone helper

Python 3.9+, standard library only:

```text
python3 scripts/validate_milestones.py --max-chars 199 "First description" "Second description"
```

Omit `--max-chars` to count only; output must say NOT_ENFORCED, not PASS. With a limit, exit 0 means all nonempty descriptions meet it, 1 means validation failed, 2 means invalid command arguments. An empty description is invalid. Without a runtime, draft qualitatively and state that scripted validation was not performed; do not invent counts.

Quotes are proposals, not agreements; hourly weekly ceilings are not guaranteed spend. Include coordination, revisions, testing, delivery, deployment and handoff in cost. No universal newcomer discount. Never trade payment or a discount for a review. Current contact/portfolio rules still apply to existing proof; consult [sources](sources.md) if the decision relies on them.

A video is optional. If requested, outline a short demonstration tied to the buyer's decision, label what has actually been verified, and identify remaining dependencies. A view count does not establish why a buyer continued or stopped.
