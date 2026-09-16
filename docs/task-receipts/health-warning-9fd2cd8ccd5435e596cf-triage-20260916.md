# Health warning triage: stale witness reconciliation errors

- Task: `health-warning/9fd2cd8ccd5435e596cf/triage`
- Source warning: `mesh-witness-task-autono@mesh-home`, 2026-09-15T22:07:54Z. It reported three `reconcile-still-in-owner-queue` errors.
- Direct status verification at 2026-09-16T10:22Z:
  - `witness-chat-range-review-near-57755-57816/review`: `rejected`.
  - `witness-chat-range-review-near-58964-59042/review`: `done`, artifact `docs/chat-range-reviews/witness-chat-range-review-near-58964-59042.md`.
  - `witness-chat-range-review-near-60653-60726/review`: `done`, artifact `docs/chat-range-reviews/witness-chat-range-review-near-60653-60726.md`.
- The referenced completion artifacts exist and are non-empty.

## Disposition

Non-actionable stale observation. All three exact task rows are terminal, so there is no live owner-queue work for health to take and no corrective task is justified. The warning reflects reconciliation lag or a stale scan, not an active stalled task. Recheck only if a fresh witness scan reports one of these exact rows as active/open again.

Delegation decision: this was a single tightly coupled ledger reconciliation; it stayed local. No subagent report or uninspected delegated claim is used.
