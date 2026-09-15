# Layout shim retirement gate — held 2026-09-12

Task: `tg-scripts-layout-migration-20260912/retire-layout-shims` (owner: `genome`).

## Disposition

No compatibility path was removed. The required gates are not satisfied in the current checkout,
so this task remains open for a later post-land audit.

## Current evidence

- `docs/task-receipts/tests-and-ux-classification-20260912.md` says the UXN family migration is
  ready for mesh-land review. The moved `scripts/ux/` and `scripts/tests/uxn/` files are still
  working-tree changes, and no post-land deploy/autowire/doctor cycle is evidenced.
- `stat` confirms `scripts/uxn/`, `scripts/ux/`, and `scripts/tests/uxn/` are real directories.
  A fresh `rg -l 'scripts/uxn|/uxn/' scripts tests job ~/.mesh/reflexes.cron` census still finds
  references in runtime tools including `mesh-tick`, `mesh-dispatch`, `mesh-doctor`,
  `mesh-load-gate`, `mesh-stress`, `mesh-airtime`, `mesh-thermal-zone`, `mesh-therm-watch`,
  `mesh-series-stats`, `mesh-clear-log`, `mesh-battery`, `mesh-body-thermal`, `mesh-hw-health`,
  `mesh-swap`, `mesh-diary`, `mesh-resource-guard`, `mesh-note3-uxn-sense`, and `mesh-uxn-drift`.
  The old-path caller census is not empty.
- `scripts/mesh-manifest --check` passes with 1,217 rows and no duplicate installed basenames.
  This inventory check does not establish that the old-path callers have migrated or that removing
  their source paths is safe.
- Current focused checks: `scripts/mesh-sync-tools --test` PASS;
  `scripts/mesh-autowire --test` PASS; `scripts/mesh-doctor --test` FAILS with
  `a twice-red tool did not reach fail: got 'na'` (exit 1).
- No live deploy was run against the dirty, not-yet-landed migration. Installed basename, service,
  and reflex resolution therefore have not been verified for a post-land cycle.

## Exact next action

After the UXN classification migration is landed, run a real deploy/autowire/doctor cycle and resolve
the doctor test failure. Then migrate every remaining active old-path caller, rerun the old-path
census, verify installed basenames plus service/reflex resolution, and rehearse restoration from the
previous manifest. Consider retiring only the individual shims whose gates all pass.
