# Mind recycler policy reconciliation — 2026-09-12

Completed `mind-recycle-policy-reconcile-20260912/measure-stop-outcome-policy` on `genome`.

## Evidence

- `mesh-clear-loss --report` returned `N_ALL=12`, `COST_ALL=+0.42`, last sample
  `2026-09-11T04:17:02Z`. Its four task-type groups each have three cases; `naming` and `schema`
  each report `+1.00`. The meter does not currently label task completion outcome.
- The node's `clear-log.jsonl` contained 10,736 valid JSON rows and one malformed line at inspection.
  The records have no done/unfinished outcome field; 7,894 valid rows have `engine="?"`. Existing
  `task-boundary (handoff written)` entries describe the clear invocation, not the task's outcome.
- Claude's Stop hook list runs `mesh-stop-check` then `mesh-mind-recycle --hook`. The hook rejects
  re-entrant Stop events and pins the recycler to `LIVE=0`, so it collects shadow observations only.
- Codex uses SessionStart/SessionEnd lifecycle hooks plus the configured completion notification.
  `mesh-codex-lifecycle` persists the turn artifact/handoff and checks for a board receipt, but its
  pre-handoff gate accepts active tasks with `[taking]` or `[progress]` receipts. Such unfinished
  turns can reach `mesh-clear`, which conflicts with the mesh-wide task-boundary-only doctrine. This
  separate implementation mismatch must be resolved before treating Codex behavior as support for a
  shared trigger policy.
- `mesh-clear` writes a deterministic handoff snapshot before clearing. Its safety backstop blocks
  detached `running` and `done-undelivered` work; it does not classify done/unfinished outcomes or
  assess semantic handoff coverage.

## Decision

The aggregate canary score cannot select every-stop versus task-boundary clearing. The design spec
now keeps the Claude Stop hook shadow-only and requires prospective evidence stratified by engine
and actual task outcome. `done` must be backed by a completed task receipt; `unfinished` must be an
open/active task at the stop; ambiguous events do not enter either cohort. Compare paired
recycled/control loss by cohort over at least seven consecutive days, with sample counts and
uncertainty. Do not enable a live trigger until the unfinished cohort's one-sided 95% upper confidence
bound fits an explicit loss budget. No such budget is currently defined, so no automatic live trigger
is eligible.

## Verification

- `mesh-clear-loss --test` — passed.
- `python3 scripts/mesh-codex-lifecycle --test` — passed.
- `mesh-mind-recycle --test` — passed, including forced-shadow Stop path and unsafe-gate refusal.
- `mesh-clear --test` — passed during the prior shadow-wiring verification.
- `mesh-clear --gate genome` — `OK`, no running or undelivered background task.
- `mesh-mind-recycle --status` — header only; no live shadow verdict was available.

No live clear, continuation injection, or hook-triggered sample was performed for this reconciliation.

## Next action

Add prospective `engine` and done/unfinished outcome labels to the clear-loss evidence path, resolve
the Codex lifecycle/task-boundary mismatch, and collect the stratified seven-day sample. Keep the
Claude Stop hook shadow-only until an explicit loss budget and the required evidence support a trigger.
