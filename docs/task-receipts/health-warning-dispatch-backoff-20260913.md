# Health warning dispatch backoff — 2026-09-13

Live evidence showed `health-warning/4ffcd9cbfa5307a1234e/triage` failing board
dispatch every roughly 20 seconds. Each retry took the global `mesh-task` lock while
the task ledger was replayed/appended, delaying unrelated Health reconciliation and
other owners' transitions.

`mesh-health-warning-task` now persists a retry record per exact chain. A failed
dispatch backs off from five minutes with bounded exponential growth to one hour;
the next watcher pass records and honors the deadline rather than repeatedly taking
the ledger lock. A successful or terminal disposition clears that retry record.
The source cursor stays before the unresolved warning, so no incident is dropped.

Verification:

- `python3 tests/test-mesh-health-warning-task.py` covers a future persisted retry
  deadline (no dispatch) followed by an eligible deadline (one dispatch).
- `python3 scripts/mesh-health-warning-task --test`
- `git diff --check`

Landing and live verification:

- The five requested commits were replayed in order onto `main` as `18eb2efd`,
  `e3e7c466`, `e90f2201`, `8e88d4d1`, and `e966fae5`, then published with
  `mesh-land --push-heal`. Remote and canonical `main` now point at
  `e966fae5` (`Back off failed health warning dispatch retries`).
- Installed copies of `mesh-task`, `mesh-pane-consume`, `mesh-health-warning-task`,
  `mesh-task-unblock-sweep`, and `mesh-witness-task-autonomy` match the landed
  source hashes. Previous copies are backed up in
  `~/.mesh/tools-backup/witness-followups-20260913`.
- Focused witness autonomy, ownerless pane candidate, and health-warning tests
  passed. The installed `--test` checks for those tools, `mesh-task`,
  `mesh-pane-consume`, and `mesh-task-unblock-sweep` also passed.
- Both `~/.mesh/reflexes.cron` and the live crontab contain the one-minute
  `mesh-health-warning-task` and five-minute `mesh-task-unblock-sweep --run`
  entries. The scheduled post-install run appended this fresh observer record
  to `~/.mesh/witness-task-autonomy.log` at `2026-09-13T15:15:09Z`:
  `RUN health=PASS source=PASS unfinished=91 blocked=54 idle_minds=9 dispatchable=0 ownerless=0 ownerless_visible=0 checks=0 errors=none`.
- The named `health-warning/4ffcd9cbfa5307a1234e` chain is already complete
  (dispatch failed at `14:51:31Z` and its triage receipt exists), so it no
  longer provides a live retry to observe. The focused health-warning test
  exercised both the persisted future deadline (hold) and eligible deadline
  (retry); the live retry map has no active entries. Task status and owner-scoped
  queue reads remained responsive after deployment.
- Resource decision: load average was `21.98, 22.86, 43.00` on 16 CPUs,
  available memory was `19,987,844 kB`, free swap `1,508,316 kB`, and GPU
  utilization `0%` with `11,127/12,288 MiB` allocated. The focused CPU-only
  checks were used; no GPU service or workload was changed.
