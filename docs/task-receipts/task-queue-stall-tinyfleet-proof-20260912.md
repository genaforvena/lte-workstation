# Task queue claimability repair

Date: 2026-09-12 (UTC)  
Owner: genome  
Task: `task-queue-stall-tinyfleet-proof-20260912/investigate-and-fix`

## Diagnosis

The structured queue exposed a mismatch between selection/checking and taking:

- `mesh-task queue --dispatch` included an open exact-owner row even when that owner already had
  another active/claimed task. `mesh-task check dispatch` also returned eligible. `mesh-task take`
  then refused the same row with “owner already has active task”. A live single-active-task owner
  could therefore receive/reselect work it could not claim.

The refusal in `take` is intentional: one active task per owner prevents parallel claims. The defect
was that queue selection and the dispatch check did not share that claimability rule. The genome
owner was already working a long-running layout claim when this task was repeatedly dispatched.

Direct live reproduction before landing: while Genome held this investigation claim, the installed
`mesh-task queue --dispatch --owner genome` still returned the open `tests-and-ux-classification`
successor, and its installed `mesh-task check dispatch ... genome` exited 0. The updated source
returns no owner-scoped claimable row and refuses that exact dispatch check with exit 2.

The queue's newest-first tie-break remains unchanged: the September 12 operator decision explicitly
preserves it and accepts visible starvation under continuous inflow
([ledger coordination review](../ledger-pull-coordination-review-20260912.md),
[newest-first verification](verify-newest-first-dispatch-20260912.md)). That ordering did not explain
the no-take refusals while Genome already held another active claim.

## Change and regression coverage

- Added an owner-active query inside the installable `mesh-task` command, normalizing legacy
  slash-qualified owners. The shared `mesh_task_log.py` library remains unchanged because its
  manifest policy is non-deploying.
- Made `check dispatch` refuse a task while its exact owner has another active/claimed task, while
  preserving the `unblock/` resolver exception already allowed by `take`.
- Removed owner-busy rows from the claimable dispatch queue.
- Added focused tests for assigned and unassigned busy-owner eligibility, queue/check agreement, and
  resolver eligibility.

## Verification

- `python3 tests/test-mesh-task-log.py` — PASS (26 tests; the ledger parser itself is unchanged).
- `python3 scripts/mesh-task --test` — PASS, including busy-owner refusal/queue cases and resolver
  claims.
- `bash scripts/mesh-dispatch --test` with `MESH_TASK_CMD=scripts/mesh-task` — PASS (structured
  queue smoke).
- Python syntax compilation — PASS.
- `mesh-task --test` — PASS after deployment; `mesh-sync-tools --test` — PASS, including manifest
  inventory, nested parity, and shim basename checks; `mesh-dispatch --test` with
  `MESH_TASK_CMD=/home/mesh-home/.local/bin/mesh-task` — PASS.
- MeshLand commit `1df09920 Align dispatch queues and eligibility with single-active-owner claims`
  landed and deployed `scripts/mesh-task`. Source and installed SHA-256 match:
  `9a6e23d30a78db5a77072771494aeba79ce515c71cc29f6abcbd7988839d7b67`.
- Post-deploy live check while Genome owns this active claim: the installed owner-scoped dispatch
  queue is empty, and `mesh-task check dispatch
  tg-scripts-layout-migration-20260912/tests-and-ux-classification genome` exits 2 (ineligible).
- Wiring evidence: cron invokes installed `mesh-dispatch` every five minutes at
  `crontab:33` (and on chat-log fsnotify at `crontab:182`). `scripts/mesh-pane-consume:247-250`
  checks each canonical dispatch row before owner-authored take, and
  `scripts/mesh-mind-control:1324-1325` rechecks dispatch eligibility before delivery.
