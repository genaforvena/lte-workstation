# Witness chat review — 2026-09-14 03:39 UTC

Reviewed the current 800-line window of `/home/mesh-home/.mesh/chat.log` (from
2026-09-13T21:01:28Z through 2026-09-14T03:38:10Z). It contains 180 structured
`[task-ledger]` records (22.5%); the live unfiltered 20-line tail contained 7
ledger records (35%). These records carry full chain snapshots, so they obscure
ordinary board updates in the top raw-tail view.

Code check: deployed `/home/mesh-home/.local/bin/mesh-task` lines 368–379 encode
and append a new task-state record for every changed chain save. In
`scripts/mesh_task_log.py`, lines 224–250 flatten all fields into the readable
record. The exact existing fix is `chat-review/task-ledger-delta-render`, owned
by genome; this review adds fresh measurements only and deliberately creates no
second task.

Verification performed: `mesh-dash --once witness` showed the materialized
ledger counts and newest 20 unfiltered source lines; `mesh-task audit` ran;
the source window and task-ledger counts were recomputed directly from
`chat.log`; deployed code paths were opened at the cited lines. Posted the
fresh-evidence `[chat-review]` at 2026-09-14T03:39:00Z.

No other candidate cleared both the recent-review and already-open-task checks.
