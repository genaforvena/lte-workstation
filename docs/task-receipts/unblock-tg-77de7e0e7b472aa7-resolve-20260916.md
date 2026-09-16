# Unblock receipt: tg task-ledger delivery contention

- Blocked parent: `unblock-skill-no-human-dependency-20260916/deliver-unblock-skill-no-human-dependency`
- Recovery task: `unblock/tg/77de7e0e7b472aa7/resolve`
- Block predicate: the delivery step was blocked because task-ledger writer contention had
  prevented `mesh-task done` from settling it, despite an existing verified Telegram receipt.
- Evidence inspected: `docs/task-receipts/unblock-skill-no-human-dependency-delivery-20260916.md`
  records `mesh-tg` `ok:true` at `2026-09-16T08:22:01Z`; `/home/mesh-home/.mesh/tasks.journal`
  recorded the delivery step as blocked and this recovery row as active.
- Recovery action: after the recorded retry event, ran `mesh-task resume` for the blocked
  delivery step, confirmed the exact-owner `tg` step was active, and retried `mesh-task done`.
- Verification: `mesh-task status unblock-skill-no-human-dependency-20260916` reports
  `[complete] (3/3)` and the delivery step reports `[done]` with artifact
  `docs/task-receipts/unblock-skill-no-human-dependency-delivery-20260916.md`.
- Result: no operator action or resend was needed; the previously typed machine-internal
  ledger contention was recovered and the parent task settled.
