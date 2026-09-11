# Idle-turn cost follow-through correction — 2026-09-11

## Root cause

`task_aware_gate_decision` previously suppressed only `WAKE:deaf`. When prediction TTL was
absent or expired, an unchanged pane therefore returned `WAKE:plain` even with no exact-owner
candidate. The loop also treated both directions of a task-candidate signature change as a wake.

## Change

`scripts/mesh-pane-consume` now:

- holds an unchanged pane with no exact-owner candidate as `HOLD:no-eligible`, including absent
  and expired expectations;
- reclassifies a changed pane delta against the stored pattern for the no-candidate cost gate even
  after TTL expiry: fully predicted delta holds, while an unpredicted line wakes;
- retains fail-toward-waking for a real pane surprise when expectation is absent or expired;
- wakes on empty→eligible task state;
- routes eligible→empty through the pane gate, so taking work does not buy a follow-up owner turn
  while a real pane surprise remains visible;
- keeps the previous candidate value alongside the signature so the directional decision is made
  from the actual transition.

## Red/green evidence

The focused regression was extended red-first and reproduced both former failures: absent
expectation plus unchanged no-candidate state returned `WAKE:plain`, and an expired expectation
with a changed-but-fully-predicted pane delta returned `WAKE:plain`. It now passes these arms:
absent expectation hold, expired expectation hold, expired predicted changed-delta hold, expired
unpredicted delta wake, empty→eligible wake, eligible→empty hold, and real unpredicted pane wake.

## Verification

- `bash -n scripts/mesh-pane-consume tests/test-mesh-pane-consume-task-aware-idle-gate.sh` — PASS
- `bash tests/test-mesh-pane-consume-task-aware-idle-gate.sh` — PASS
- `bash scripts/mesh-pane-consume --test` — PASS
- `mesh-sync-tools --apply` — PASS; source and deployed executable match at SHA-256
  `44a44dd490c31a44dda3bed0ca681d61be638f26a222b063a33778647dd20c3a`.

The task-aware comments and smoke summary are aligned with this exception: expired fully-predicted
deltas hold only for no-candidate work; absent/no-pattern, malformed-pattern, and genuinely
unpredicted deltas still wake.

The corrected source is deployed at the SHA above and must be landed after the 600-second settle
window.

## Landing scope blocker

`mesh-land` does not enumerate `tests/`; its exact `MESH_LAND_PATHS` filter cannot admit an untracked
focused test that enumeration never returns. A temporary global `tests/` enumerator was removed after
scope review because this worktree contains unrelated untracked tests. The correction remains
RUNNING and unlanded. Separate task `mesh-land-test-artifact-support-20260911/exact-test-artifact-allowlist`
is open for a narrowly scoped artifact mechanism; no correction landing is claimed until `git show
--name-status` proves code, focused test, correction receipt, and relevant review artifacts are in the
landed commit scope.
