# Senses live reflex-health gap — 2026-09-16

Timestamp: 2026-09-16T12:33Z (UTC)

## Live evidence

- Required pane read: `mesh-dash --once senses`, exit 0. Captured artifact: `/tmp/senses-live-20260916T122500Z.log`.
- Unfiltered pane state says: `mesh-reflex-health unavailable — produced NO output`.
- Direct real check: `timeout -k 3 15s /home/mesh-home/.local/bin/mesh-reflex-health --check`.
- Direct check result: exit `124` (timeout); stdout `0` bytes; stderr `0` bytes.
- Installed path resolves to `scripts/mesh-reflex-health`.
- Installed SHA-256: `b514c2ba14974a9e48b33aebd0c425d5c4c993f40b7d56e7862586b976e0394d`.
- Repository SHA-256: `b514c2ba14974a9e48b33aebd0c425d5c4c993f40b7d56e7862586b976e0394d`.

This is a real producer/runtime failure, not a dashboard filtering artifact: the producer itself
does not return a result within the bounded interval and emits no diagnostic output.

## Ownership / retry edge

Owner queue was empty with `mesh-task queue --dispatch --owner senses` exit 0. No active or blocked
ledger row matched `reflex-health` or this gap in the replay search. The intended exact-owner chain
`senses-reflex-health-20260916/diagnose-reflex-health` could not be created: repeated bounded
`mesh-task create` attempts failed or timed out; the final observed failure was
`task-state append failed; cache not changed: mesh-task-log: task-ledger rejected: log scrub would
alter structured data`. A subsequent status confirmed the chain is absent from `chat.log`.

Retry after the concurrent task-ledger/chat-log writers finish and the append scrub accepts a fresh
canonical row; then run `mesh-task create`, `mesh-task check dispatch ... senses`, and
`MESH_TASK_ACTOR=senses mesh-task take ...` before any repair. Re-run the bounded producer check after
the task is claimed. No service, routing, or substrate mutation was made.
