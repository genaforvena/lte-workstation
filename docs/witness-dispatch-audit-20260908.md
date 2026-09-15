# Witness dispatch audit — 2026-09-08

At 2026-09-08T09:35Z, `mesh-task replay --json` identified 14 open current
steps with no `waiting_for` prerequisite. Every one had `dispatch=sent`; the
dispatch queue and `mesh-task check dispatch` both accepted all 14 rows.

The remaining unfinished rows are dependency-waiting or typed BLOCKED rows.
No current dispatchable row had a missing owner. Live owner checks showed tg,
haunt, hire, and wake idle, and genome working but live/reachable; therefore no
owner substitution was needed.

Verification:

- `mesh-task --test` — pass
- `mesh-dispatch --test` — pass
- `mesh-task audit` — 16 BLOCKED, 126 QUEUED, 80 DONE, 7 REJECTED
- `~/.mesh/tasks.journal` — replay PASS, 242 rows, 14 current dispatchable rows
