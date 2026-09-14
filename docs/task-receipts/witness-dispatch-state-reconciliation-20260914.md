# Witness dispatch-state reconciliation — 2026-09-14

Task: `witness-dispatch-state-reconciliation-20260914/reconcile-dispatch-state-after-check-refusal`  
Owner: `genome`

## Finding

The witness reads its global dispatch queue and later checks each candidate against canonical task
eligibility. A task can be taken between those reads, so the exact-owner check returns 2 after the
earlier snapshot counted it as claimable. A second legitimate refusal occurs when the requested
owner already has another active task; the candidate can remain open while `mesh-task check` refuses
to let that owner take more work. The original witness treated both cases as failures and retained
the earlier `active=0` count when its first audit missed a pre-existing active task.

Historical evidence:

- On 2026-09-13, the `health-warning/3558bdcb65a553510b2a/triage` receipt records the
  18:40:41Z refusal for
  `tinyfleet-confirmatory-v1-arm-gates-20260913/register-confirmatory-generative-inputs`.
  The source check snapshot was at 18:40:11Z, Haunt claimed the task at 18:40:30Z, and the
  structured active row landed at 18:40:34Z. The queue-to-claim race is inferred from those
  timestamps; the original check stderr was not retained.
- The 2026-09-14 06:21:13Z observation for
  `20260914T040000Z-060000Z/analyze-observation` is documented in
  `docs/task-receipts/health-warning-302a03775c847ac58e96-triage-20260914.md`. The owner-authored
  take and active ledger row appeared at 06:20:50Z and 06:20:54Z; the following observer run passed.
- The 07:15:55Z refusal for
  `health-warning/eb433dcbffedb86f3aa7/triage` is documented in
  `task-receipts/health-warning-6bcab66469917ab65056-triage-20260914.md`: the take was recorded at
  07:15:23Z and the active ledger row at 07:15:30Z.
- `docs/task-receipts/health-warning-555c7b0a355c13873389-triage-20260914.md` records another
  owner-busy instance: Health's active task caused exact checks of other Health candidates to return
  2 while those candidates were absent from the Health-scoped queue.

## Change

`scripts/mesh-witness-task-autonomy` now retries canonical audit, replay, global dispatch queue, and
exact-owner queue reads only after check code 2. It suppresses the refusal only when the fresh,
strictly parsed views prove that the row is no longer claimable: the task became active or terminal,
the owner is busy on another audited active task, or another explicit canonical gate now blocks the
row. It rejects unreadable or contradictory snapshots, malformed rows, candidates still visible in
the owner's queue, and rows that remain eligible. Other check exit codes remain failures. The
refreshed active view updates both the summary and saved stall-age cursor. The observer does not take,
reassign, complete, or otherwise transition a task.

## Verification

- `rtk python3 tests/test-mesh-witness-task-autonomy.py` — exit 0. Fixtures cover the concurrent
  take, a stale audit/replay missing an already-active task (including preservation of its prior
  observation age), an owner-busy refusal, persistent and still-eligible refusals, check exits 1 and
  3, malformed replay, and an unreadable audit. The suite also exercises the scheduled wrapper's
  invocation order.
- `rtk python3 scripts/mesh-witness-task-autonomy --test` — exit 0.
- `rtk /home/mesh-home/.local/bin/mesh-witness-task-autonomy --test` — exit 0.
- `rtk python3 -m py_compile scripts/mesh-witness-task-autonomy tests/test-mesh-witness-task-autonomy.py`
  and the targeted `git diff --check` — exit 0.
- Wiring remains active: live crontab line 352 runs `~/.local/bin/mesh-task-unblock-sweep --run`
  every five minutes; the wrapper invokes `mesh-witness-task-autonomy --once` after the unblock
  sweep. The repository and installed wrapper SHA-256 values match
  (`bcb76d90312ae28f9fc64394e6109a180c710ba5dc54e8db9dc58d337544126a`), and its installed
  `--test` exits 0.
- MeshLand landed the source as `b8765d89` with subject
  `mesh-land: update scripts/mesh-witness-task-autonomy: reconcile refused dispatch checks against fresh canonical state`.
  The regression fixtures, including direct code-1/code-3 refusal checks, were landed as
  `464903640e35089a3118646935e3ebedba352990` with subject
  `mesh-land: update tests/test-mesh-witness-task-autonomy.py: keep exit 1 and 3 check refusals failed without reconciliation`.
  At verification, `HEAD` and `origin/main` were both
  `464903640e35089a3118646935e3ebedba352990`.
  The repository and installed tool SHA-256 values match:
  `1fbd4c770c64bafa9490dbc180b3ed0589e860dd0823ad47048789f1e51b90ac`. The shared
  `mesh_task_log.py` source and installed SHA-256 values also match:
  `35dea1228820d29fbeea231c8cb80e1dc8a63db80fec0a5a670a674d598720ac`.
- The installed tool's guarded live one-shot at 2026-09-14T13:20:29Z returned exit 0:
  `health=PASS source=PASS unfinished=101 blocked=57 idle_minds=12 dispatchable=3 ownerless=0 ownerless_visible=0 active=2 active_recovery_wakes=0 dispatch_repairs=0 checks=3 errors=none`.
  It read live task state while directing its journal, tape, state, followthrough, and lock outputs to
  `/tmp/genome-witness-installed.CGmk2YH4`. A temporary task-command wrapper allowed only `audit`,
  `replay`, `queue`, and `check`; alert and tell sinks were disabled. The exact task status output
  before and after was byte-identical (SHA-256
  `e14cea3c3c5040c08c576b4ea4eab03ca3b9a0f1e9ccd3054967f2de2613693b`), and the run reported zero
  dispatch repairs and zero active recovery wakes. No live refusal occurred in that sample; the
  queue-to-claim reconciliation is exercised by deterministic fixtures.

No routing, DNS, firewall, VPN, or exit-node state was touched. MeshLand also surfaced an unrelated
untracked `scripts/mesh-witness-stall-sweep` autowire skip; that separate candidate was left outside
this task's path scope.
