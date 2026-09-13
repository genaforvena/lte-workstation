# Self-pick for unowned runnable tasks — 2026-09-13

## Finding

`mesh-task take` already lets the first mind claim an unowned step and atomically records it as
owner. `mesh-task check dispatch` also accepts an ownerless row for an idle mind. The gap was in
`mesh-task queue --dispatch --owner <mind>`: its exact-owner filter discarded every ownerless row,
so the normal self-pick prompt never showed those tasks. A queued row could therefore remain
unnoticed even though any idle mind was allowed to take it.

## Landed change

Reviewed commit `abf0825ae4797c5a692fe5a2b55fe0913d54ca3b` on
`codex/unowned-task-pickup-20260913`. Its parent predates queue aging, so its whole-tree merge would
have removed that behavior. Integrated the ownerless-row filter change into the current aged
`dispatch_queue` instead, retaining age ordering and the existing serialized first-claim behavior.
The queue includes ownerless runnable rows only for idle requesting minds, still hides rows owned by
another mind, and hides unowned rows from a requester that already has active work.

MeshLand landed and pushed the implementation and focused tests to `main`:

- `6be4562d` — expose unowned runnable tasks to idle owner queues.
- `f8fd218a` — test owner-scoped visibility and exclusive task claims.
- `d4bc25bf` — test first-claim exclusivity for unowned queue work.

## Verification

- `rtk proxy python3 tests/test-mesh-task-unowned-pickup.py -v` — passed: two idle minds both see
  the unowned row, both pass pre-claim eligibility, the first `take` assigns it, and the other
  mind then sees and checks it as unavailable.
- `rtk proxy python3 tests/test-mesh-task-optional-owner.py` — passed, including failed-receipt
  rollback, first-owner assignment, exclusive claim, and unassigned successor handoff.
- `rtk proxy python3 tests/test-mesh-task-log.py` — 26 passed.
- `rtk proxy python3 scripts/mesh-task --test` — smoke test passed.
- `rtk proxy python3 tests/test-mesh-task-dispatch-fairness.py -v` — 3 passed, confirming age-based
  dispatch ordering remains intact.
- `rtk proxy python3 -m py_compile scripts/mesh-task tests/test-mesh-task-unowned-pickup.py` and
  `rtk git diff --check` — passed.
- Installed `/home/mesh-home/.local/bin/mesh-task --test` — smoke test passed after landing.
- Source and installed `mesh-task` SHA-256 both equal
  `ef32db98a97bad0770a9513a3c2de8a3202a3f0e8fb684fb2c8e73714e9d5ee3`.
- An isolated live fixture through the installed binary showed both idle owner queues, passed both
  pre-claim checks, assigned the task to Alice on first take, and refused Bob's later check/take.

## Task status

`autoland/unowned-task-self-pick-20260913/expose-unowned-runnable-work` is implemented, landed,
installed, and verified. The unrelated staged genome worktree changes remain staged and untouched.
