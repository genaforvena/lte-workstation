# Health-warning triage: witness-task-autonomy

Source warning: `/home/mesh-home/.mesh/chat.log:67738` at
`2026-09-15T19:41:22Z`; matching autonomy evidence is
`/home/mesh-home/.mesh/witness-task-autonomy.log:503`.

The warning reported two `reconcile-global-queue-rc-124` failures for
`witness-chat-range-review-near-58283-58355/review` and
`witness-chat-range-review-medium-63488-63815/review`, plus
`reconcile-still-in-owner-queue` for
`witness-chat-range-review-near-62002-62077/review`.

Action taken: `mesh-task reconcile health` completed with 487 canonical
pointers. The first two rows are now terminal `REJECTED` in
`/home/mesh-home/.mesh/tasks.journal:1535-1536`, with the documented stale
producer-backlog reason. The third remains an open witness-owned row and
`mesh-task check dispatch witness-chat-range-review-near-62002-62077/review health`
correctly exited 2, so health did not claim another mind's work.

The source condition is historical and explained by the retained backlog/cap
change documented in `docs/chat-range-review-backlog-cleanup-20260915.md:3-23`.
Later autonomy log rows include PASS at 02:40:20Z, but the bounded fresh
`timeout 45s mesh-witness-task-autonomy --once` did not complete (exit 124).
Therefore current end-to-end reflex health is not proven; this is a known
sampling/observer blind spot, not a success claim. `mesh-health` separately
showed this node and several LAN/tailnet peers reachable, with known offline
remote rows.

Delegation: Darwin performed a read-only audit. I personally inspected every
cited artifact and command result; no delegated report was treated as evidence
alone. No substrate changes were warranted.
