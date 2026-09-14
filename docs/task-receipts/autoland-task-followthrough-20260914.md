# Autoland and task followthrough closure — 2026-09-14

Operator request: stop recurring autoland failures and ensure unfinished tasks remain visible with a concrete reason and next action.

## Findings

- `mesh-land --check` exceeded 60 seconds on the live dirty tree. The test pool bounded only child `--test` calls; candidate parse, rollback-history checks, and per-path state processing were unbounded in aggregate.
- The live tree presented 932 landing obligations. The old path expanded them into hundreds of repeated refusal lines and could reach the caller timeout before leaving a usable inventory.
- Autoland had no process-wide writer lock. A long run could cross the next cadence and let two runs touch the same git index/worktree.
- The scheduled task witness counted 100+ unfinished rows but did not leave a per-task human-readable reason/age/action artifact. A generic `PASS` therefore did not prove followthrough for each obligation.

## Changes

- `mesh-land --check` now admits large enumerations directly to a bounded bulk path before parse/test/history work. It atomically writes every path with age, reason, and next action to `~/.mesh/mesh-land-backlog.tsv`, posts one board task keyed by the stable path/reason/action set, reports the current artifact SHA-256, and exits nonzero.
- Small checks have independent test and whole-classification budgets. Unclassified paths are retained with an explicit `classification unrun` reason.
- `mesh-land --autoland` now takes a nonblocking process lock before enumeration. An overlap is refused with a precise `[health-fail]` board event.
- Large autoland queues are processed as a rotating 40-path batch. The full ordered queue and next cursor are written before any test or commit, so a killed pass continues at the next slice instead of repeating the same prefix.
- `mesh-witness-task-autonomy` now atomically rewrites `~/.mesh/task-followthrough.tsv` on every scheduled sweep. Every unfinished audit row carries observation time, state, owner, task id, age, reason, and next action.

## Verification

- `tests/test-mesh-land-check-budget.sh`: PASS. The large-tree fixture writes one full backlog artifact, a concurrent autoland is refused loudly, and repeated autoland work advances a persisted bounded-batch cursor.
- `tests/test-mesh-witness-task-autonomy.py`: PASS. The fixture proves task age/reason/action rows, stalled-owner recovery, dispatch repair, and scheduled wiring.
- `bash -n scripts/mesh-land tests/test-mesh-land-check-budget.sh`: PASS.
- `python3 -m py_compile scripts/mesh-witness-task-autonomy tests/test-mesh-witness-task-autonomy.py`: PASS.
- Live `mesh-land --check`: 932 rows admitted to the bulk path in 5.238 seconds; artifact SHA-256 `e95f8c737bc80c1dfe8595b7527dd1d88e7ec66e5912289b90f78a093e19bd0c`.
- Live task witness: wrote 109 unfinished rows plus header to `~/.mesh/task-followthrough.tsv`; it failed honestly on `unblock/adint/4cfa94719609e92e/resolve` because the advertised dispatch row's exact check returned rc=2.

The exact refused dispatch remains an open ledger obligation for its owner/coordinator; it is now visible in the followthrough artifact and health signal rather than hidden by an aggregate pass.
