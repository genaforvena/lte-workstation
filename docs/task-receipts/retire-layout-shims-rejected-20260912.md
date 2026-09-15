# Layout shim retirement gate — rejected 2026-09-12

Task: `tg-scripts-layout-migration-20260912/retire-layout-shims` (owner: `genome`).

## Disposition

Rejected for now: the instruction's required safety gates are not satisfied, and removing the old
UXN path now would regress current callers. No shim or source path was removed.

## Current evidence

- `mesh-task status tg-scripts-layout-migration-20260912` reports this final step `open`.
- The preceding `tests-and-ux-classification` receipt says the move is awaiting mesh-land review;
  `git status --short` shows its UXN source, fixtures, tests, manifest, and receipt still staged or
  added in this checkout. There is no post-move landed deployment cycle in the available artifacts.
- A fresh `rg -l` census over `scripts/`, `tests/`, `job/`, and `~/.mesh/reflexes.cron` found 57
  source/test files with `scripts/uxn` or `/uxn/` references. Runtime consumers include
  `scripts/mesh-tick`, `mesh-airtime`, `mesh-stress`, `mesh-dispatch`, `mesh-thermal-zone`,
  `mesh-therm-watch`, `mesh-series-stats`, `mesh-doctor`, `mesh-load-gate`, `mesh-clear-log`,
  `mesh-battery`, `mesh-hw-health`, `mesh-swap`, `mesh-body-thermal`, `mesh-diary`, and
  `mesh-resource-guard`; several directly resolve `scripts/uxn/threshold-ledger` and
  `scripts/uxn/mesh-sexpr-gate`.
- Current `scripts/uxn` and `scripts/tests/uxn` are directories in the working tree. Their removal
  or conversion to a compatibility path would not be safe while the above references remain.
- Current checks: `mesh-sync-tools --test` PASS; `mesh-autowire --test` PASS;
  `mesh-land --test` PASS; `mesh-doctor --test` FAIL (`a twice-red tool did not reach fail: got
  'na'`). The doctor failure is also recorded by the UXN classification receipt.

## Exact next action

Keep the old paths. First land the scoped UXN migration, complete a post-land deploy/autowire/doctor
cycle with `mesh-doctor --test` passing, then migrate every remaining old-path caller and repeat a
fresh census. Rehearse restoration from the preceding manifest before considering any shim removal.
