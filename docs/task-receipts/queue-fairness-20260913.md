# Runnable task queue fairness — 2026-09-13

## Finding

The dispatcher ordered same-incident work by descending priority and then descending
`dispatched_at`, so newer work of the same priority continually moved ahead of older work. The
source explicitly named indefinite starvation as the tradeoff. `waiting_for` tasks were correctly
kept out of dispatch, but the queue policy did not guarantee eventual service to old runnable work.

## Tested change

The candidate fix was developed on shared Git branch `codex/queue-fairness-20260913`:

- `708accbfe08ab1787ed75d72666741ee3c2a622b` changes queue and audit ordering and adds focused
  fairness regressions.
- `8ec1c429fa7a04b1aea15f9ee395325ebe2aafd5` adds lifecycle guidance and verification evidence.

Runnable age advances in configurable bands (default one day). Older bands rank first, then
incidents and `unblock/` resolver tasks, numeric priority, and FIFO order. Thus newer arrivals
cannot bury an older runnable row in the dispatcher. Redelivery retains the first `queued_at`;
tasks released from `waiting_for` begin aging when their prerequisite completes. Audit and dispatch
share the same ordering. Queue output remains a full candidate list: the mind chooses work based on
context and what it unlocks; age ordering is a fairness backstop, not a fixed assignment.

The candidate commits were based on `53d9798c`, before independent pickup landed on `main`. A direct
cherry-pick would have removed owner-attested pickup behavior, so the fairness changes were
integrated onto current `main` while preserving that behavior. MeshLand landed the source,
operator guidance, and focused test as separate scoped commits:

- `93751c36` — Age runnable tasks to prevent starvation in dispatch.
- `337caab7` — Explain dependency frontier and queue aging for operators.
- `7d08bcc1` — Test task queue aging and redelivery fairness.

## Verification

- `rtk proxy python3 tests/test-mesh-task-dispatch-fairness.py -v` — 3 passed, covering age over a
  newer high-priority arrival, equal-band resolver preference, audit/dispatch order, and redelivery
  preserving queue age.
- `rtk proxy python3 scripts/mesh-task --test` — smoke test passed for canonical task records,
  exact-owner checks, lease/progress, typed block/resume, artifact hashing, and idempotent completion.
- `rtk proxy python3 tests/test-mesh-task-independent-pickup.py` — passed after integrating aging,
  confirming the current independent-pickup contract remains intact.
- `rtk proxy python3 -m py_compile scripts/mesh-task tests/test-mesh-task-dispatch-fairness.py` and
  `rtk git diff --check` — passed.
- `tests/test-mesh-task-no-expiry.py` failed 5 of 13 tests on clean base `53d9798c`, before this
  change; its legacy fixture expectations around resolver materialization and busy-owner filtering
  are recorded as pre-existing failures, not acceptance evidence for this change.

## Live status

The deployed source and `~/.local/bin/mesh-task` have the same SHA-256:
`fd29c694ba800f5c6b60dcf26150d24fdb2ea73b8852b68bd932d7a664cd8e55`. The live owner-scoped
dispatch queue currently emits `unblock/genome/95aa703598b7c325/resolve` as its only
claimable row; `mesh-task audit` lists the same row as `OPEN_UNOWNED` and lists this fairness step as
`RUNNING`. This live queue is narrow, so varied ordering is established by the isolated regression
cases rather than claimed from this one-row snapshot.

The `mesh-home:witness` pane is live (`bash`) and its captured `WITNESS TASKS` view reports this exact
fairness step `RUNNING` with the same lease as the audit. The witness view is an independent pane
observation, not a substitute for the installed hash or tests.

MeshLand initially refused its default unscoped scan because the pre-existing UXN migration contains
an unclassified `scripts/ux/chibicc/tests` candidate. Each of the three changes above was therefore
landed with an exact `MESH_LAND_PATHS` allowlist; unrelated staged UXN files remained staged and
outside those commits. A `mesh-land --test` invocation inherited that allowlist and failed its
unscoped-fixture assertion; the targeted dry run and actual scoped `--apply` runs succeeded.

One unrelated verification limitation remains: `mesh-task status autoland/task-queue-fairness-20260913`
raises `KeyError: 'tags'` when a task has `design_artifact` but no `tags`. The append-only task audit
and witness materialized view independently verify the active state; this formatting bug was not
changed as part of queue fairness.
