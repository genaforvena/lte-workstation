# Coordination hledger end-to-end acceptance — 2026-09-12

- Task: coordination-hledger-plan-20260908/end-to-end-acceptance
- Owner: witness
- Captured: 2026-09-12T03:10–03:50Z
- Plan: docs/superpowers/plans/2026-09-08-coordination-hledger.md, Task 7
- Canary artifact: docs/task-receipts/witness-canary-20260912.log

## Prior receipts (all six verified by reading, 2026-09-12)

| Step | State | Receipt |
|---|---|---|
| identity-routing | REJECTED (exact-owner impossible for retained mesh-land/genome alias; IDs preserved) | coordination-hledger-identity-20260908.md |
| background-recovery | DONE | coordination-hledger-background-20260908.md |
| communication-receipts | DONE | coordination-hledger-communication-acceptance-20260912.md |
| accounting-coverage | DONE | coordination-hledger-accounting-20260908.md |
| fyi-useful-view | DONE | coordination-hledger-fyi-20260908.md |
| health-dependencies | DONE | coordination-hledger-health-20260908.md |

Linked obligations kept, no duplicates launched: operator-status-model-20260908 is
complete (2/2, design-careful-lane DONE with artifact
docs/design-operator-status-careful-lane-20260909.md); the hire lane runs its own
ba260907-* chains (DONE + one BLOCKED), untouched.

## Bounded canary: witness-canary-20260912 (2 steps, owner witness, now complete)

Exercised the full lifecycle on the live ledger, every transition observed:

- create → take (exact-owner) → progress → block (dependency) → wait-for behind
  witness-canary-20260912/canary-deliver → take canary probe work.
- WAIT backed by a real process handle, not a lease: `sleep 25` pid 580487,
  start_ticks 22099952, `wait` returned rc=0; completion gated on its exit.
- done (artifact exists, sha recorded) → successor dispatch → take/progress/done
  with delivery artifact → chain complete (2/2).
- The acceptance step itself rode the same loop: blocked → wait-for behind
  canary-deliver → auto-resumed on completion
  (`released_by: witness-canary-20260912/canary-deliver`, waiting_for cleared,
  dispatch sent) — release_waiters verified on a real task, not a fixture.
- `mesh-task replay --json` reconstructs the canary chain including the queued
  successor; idempotent re-done with the same artifact returns "already done".

Failure arms (all refused, rc=2, nothing applied):

- done with a nonexistent artifact ("a claim is not complete without evidence").
- take and block as actor tg on a witness-owned step (exact-owner enforcement).
- re-done of a settled step with a different artifact.

Required tests, run 2026-09-12:

- tests/test-mesh-task-audit-complete.sh: PASS.
- tests/test-mesh-task-source-coverage.sh: PASS.
- mesh-task --test: smoke-test ok.
- tests/test-mesh-hledger-mind-load.sh: PASS.

## Cross-view agreement (cutoff 2026-09-12T03:17:39Z)

- Obligations: `mesh-task audit` DONE=516 == `mesh-task replay --json` DONE=516 —
  two independent computations agree at the same cutoff.
- FYI: `mesh-fyi-ledger --dash` replay=pass, coverage complete,
  source_cutoff 2026-09-12T03:09:52Z; repeated groups keep counts
  (path-watch 278, mind-control 257, devcd-catch 141, charter-watch 125).
- Scheduled observation, two cycles and more: `~/.mesh/fyi-ledger.log` shows five
  consecutive `*/10` builds (02:29→03:09Z), repeats=0 throughout, linked stable
  at 44 — repeated input does not multiply claims, deliveries or spend records.
  `~/.mesh/task-journal.log` shows the `*/5` rebuild backstop publishing, plus
  one failed cycle that preserved the last valid view and recovered on the next
  pass (fail-safe toward the last good state, not toward silence).

## Per-axis verdicts

- Coordination (plan reconstruction, dispatch, successors): PASS.
- Execution (canary lifecycle incl. process-backed wait): PASS.
- Background completion (terminal, idempotent, swept): PASS.
- Operator communication (per tg acceptance receipt): PASS.
- Obligation coverage (audit↔replay agreement, explicit unknowns): PASS.
- Labor attribution (accounting receipt checks + mind-load test): PASS.
- FYI usefulness (repeats with counts, no task creation from prose): PASS.

No global-health claim beyond these axes.

## Unresolved obligations (kept explicit, not forced)

1. Accounting receipt's two missing source rows (Sep 8 wake window, Sep 11
   health window, 1 TURN each, no correction found) remain real reconciliation
   failures with unknown attribution.
2. The `mesh-promises --check` live FAIL recorded in the accounting receipt
   (replay vs journal on the default path) belongs to a separate lane.
3. The rejected mesh-land/genome autostash alias still needs a code-level
   owner-identity repair before supported rejection/supersession.
4. This receipt and the canary log are worktree files until genome lands them
   (autoland tasks auto-post on settle).
