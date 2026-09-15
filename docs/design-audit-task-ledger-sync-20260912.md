# Task-ledger synchronization plan audit — 2026-09-12

## Verdict

The fail-closed lifecycle boundary and mesh-wide admission rule are present in the current source
and doctrine. The focused test and `mesh-task` smoke/regression checks pass. The live
`mesh-promises --check` is not currently green: the final run returned 1 after parity passed but
board replay and the materialized journal disagreed (`264` versus `0`). That live consistency
failure remains open; this audit did not rewrite the journal or alter another mind's work.

## Step-by-step audit

| Plan item | Current evidence | Result |
|---|---|---|
| Task 1, Step 1: failing command-boundary integration test | `tests/test-mesh-task-ledger-sync.sh` creates a private chain, switches `MESH_TASK_CHAT_CMD` from `/bin/true` to `/bin/false`, and checks that refused `take`, `done`, `progress`, `block`, and `resume` calls fail without advancing the asserted JSON state. | Present and exercised. The test passed in this audit. |
| Task 1, Step 2: observe the pre-fix failure | `docs/coordination-task-ledger-sync-20260907.md` preserves the historical red output: a refused `[taking]` event was reported as success. | Historical red evidence is recorded; it was not recreated by reverting shared source. |
| Task 1, Step 3: require the canonical event before state save | `scripts/mesh-task` defines `require_emit`, which exits with `board event failed` when `emit` returns false. The `take`, `done`, `progress`, `block`, and `resume` paths call it before `save`; `progress` and `resume` also update task context only after the save. | Source matches the fail-closed contract. |
| Task 1, Step 4: focused and regression checks | `bash tests/test-mesh-task-ledger-sync.sh`, `python3 -m py_compile scripts/mesh-task`, `python3 scripts/mesh-task --test`, and `bash tests/test-mesh-task-audit-complete.sh` all passed. `mesh-promises --feed` completed. The final `mesh-promises --check` returned 1: parity passed, but agreement failed with replay `264` versus hledger `0`. | Code checks pass; the live ledger agreement criterion does not. |
| Task 1, Step 5: implementation artifact | `docs/coordination-task-ledger-sync-20260907.md` records the incident, root cause, implementation, historical red output, earlier green evidence, and then-current limitations. | Existing artifact is present. This audit adds the current verification and ledger failure. |
| Task 2, Step 1: adoption measurement | `memory/multi-step-work-enters-the-promise-ledger-before-execution.md` records 85 TURN rows and 5 task-attributed rows (5.9%), explicitly treating idle/watch turns as an ambiguous denominator. | Evidence and caveat are recorded; the dated measurement was not recomputed from the current tape. |
| Task 2, Step 2: mesh-wide admission rule | `CLAUDE.md:548` requires multi-step or cross-turn work to enter the task ledger before execution, with a keyed task, next action, artifact, and closure criterion. Unassigned work may be routed by the dispatcher; an assigned owner must claim before execution. | Rule is loaded mesh-wide. Current wording allows dispatcher assignment rather than requiring an owner at creation. |
| Task 2, Step 3: case artifact | `memory/multi-step-work-enters-the-promise-ledger-before-execution.md` documents the board/ledger mismatch, adoption gap, fail-closed repair, and bounded-work exception. | Present and linked from doctrine. |
| Task 2, Step 4: doctrine and live ledger verification | The doctrine link resolves. `python3 scripts/mesh-task audit` ran and reported many existing `OPEN_UNOWNED` rows. The live promise feed completed, but the final consistency check failed as above. | Doctrine verified; exact current ledger agreement and clean ownership are unresolved. |

## Additional observations

During the first smoke-test attempt, a concurrent edit to the reassignment code briefly produced a
syntax error. No file was changed by this audit to address it. A subsequent source compilation,
focused integration test, and smoke test all passed. At audit time the source and deployed
`~/.local/bin/mesh-task` hashes differed, so the prior artifact's deployment-equality statement is
historical and was not re-established here.

## Remaining obligation

Re-run `mesh-promises --feed` followed immediately by `mesh-promises --check` after the live board
and journal writers settle. If replay still differs from hledger, trace that mismatch before
claiming ledger synchronization is currently healthy. The unrelated non-roster open owners and
`OPEN_UNOWNED` task findings also remain visible in the live audit output.
