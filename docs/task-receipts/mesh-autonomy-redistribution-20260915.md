# Mesh autonomy blockers — analysis + two fixes (2026-09-15, opencode session)

## What was actually hindering full autonomy

Measured live 2026-09-15T20:46–21:02Z (`mesh-task audit`, `mesh-witness-task-autonomy --once`,
`mesh-mind-control`, `mesh-pace --refusals`, `mesh-health`):

1. **Metric inflation, not missing work.** Autonomy read `dispatchable=3` with 14 idle minds,
   but 2 of the 3 rows were owned by `operator` / `steward` — windows that do not exist, so no
   mind can ever claim them (exact-owner discipline). Idle minds looked supplied while real
   routable work was 1 row (a vpn audit, since taken: `active` 2→3).
2. **No way to shed queued load across minds.** Per-owner serial discipline
   (`scripts/mesh-task` dispatch queue suppresses an owner's rows while it holds an active
   claim) wedged witness's 97 legacy `witness-chat-range-review` rows behind its single active
   claim. The only mover was `reassign-owner` (whole-owner, coordinator-only) — no single-chain
   form. The review producer itself is already backlog-gated (bdb0f077, holding at 97/10) and
   draining (38 review receipts done), so this was the remaining structural gap.
3. **Not blockers (verified, left alone):** pace governor is SERVED on every lane
   (cadence holds, 1% from the spend cap); 59 BLOCKED rows are legitimate external waits;
   `mesh-minds` "Idle & ready: none" is by-design `WORKERS=genome` doctrine, not a bug.

## Changes (unlanded worktree — needs genome `mesh-land`)

- `scripts/mesh-witness-task-autonomy`: queue candidates partition into routable vs
  `unroutable` (owner staffs no live mind window, matched by post-slash key against
  `mesh-mind-state --stats`). Only routable rows are eligibility-checked; tape gains
  `unroutable=N`; `dispatchable=` now counts claimable work. Fail-open: a failed mind
  census keeps every candidate checkable.
- `scripts/mesh-task`: new coordinator-only `reassign <chain> <new-owner> <reason>`.
  Moves one queued chain (refuses active / non-open / prerequisite-gated steps, empty
  reason, same owner, and any new owner without a live mind window — so it cannot mint
  fresh unroutable rows), then re-dispatches. Hoisted the `_is_mind_window` roster filter
  to module level and reused it in `recovery_owner` (behavior unchanged).
- `tests/test-mesh-witness-task-autonomy.py`: fixture `carol` (no live window) now asserts
  `dispatchable=2`, `unroutable=1`, and that its row is never eligibility-checked.
- `tests/test-mesh-task-reassign.py` (new, 6 cases): move + redispatch, active/gated/
  non-coordinator/offline/shell-window/same-owner/empty-reason refusals.

## Verification (all seen green this turn)

- `tests/test-mesh-task-reassign.py` → OK (6 tests)
- `scripts/mesh-task --test` → smoke-test ok
- `tests/test-mesh-witness-task-autonomy.py` → PASS
- `scripts/mesh-chat-range-review --test` → PASS
- Live `mesh-witness-task-autonomy --once` → PASS, `unroutable=2 dispatchable=0`, errors=none
  (the 2 unroutable are exactly `wifi-router-router-access-20260913` and
  `phaedra-autostash-steward-disposition-20260913`)

## Next (for the owning minds, not taken here)

- genome: land via `mesh-land` (no commit made from this session; no board post made —
  this session staffs no mind window and must not write the substrate or impersonate one).
- witness (coordinator): can now shed queued review backlog to idle minds with
  `mesh-task reassign <chain> <idle-mind> <reason>`, one chain at a time.
- operator/steward rows still need hands: only their exact owners can typed-block them
  (`block` requires exact owner), so they remain visible `unroutable` until a human acts.
