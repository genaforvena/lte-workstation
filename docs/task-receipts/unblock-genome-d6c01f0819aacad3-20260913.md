# Genome unblock resolver — 2026-09-13

Task: `unblock/genome/d6c01f0819aacad3/resolve`  
Parent: `tg-scripts-layout-migration-20260912/retire-layout-shims`  
Owner: `genome`

## Finding

The recorded `mesh-doctor --test` failure is not reproducible in the current checkout. A fresh
`scripts/mesh-doctor --test` run passed at 2026-09-13 14:26 UTC. The doctor self-test's `na` return
path discards the fixture capture, so the earlier `got 'na'` result has no retained evidence that
distinguishes PSI pressure, swap exhaustion, or another transient condition. At this check, PSI
`some avg10` was 0.00, `MemAvailable` was 25,991,644 of 32,787,700 kB, and `SwapFree` was 2,091,772
of 8,388,604 kB. No doctor code change is justified by the available evidence.

Fresh prerequisite checks passed:

- `scripts/mesh-manifest --check`: PASS, 1,336 complete rows and no duplicate installed basenames.
- `scripts/mesh-sync-tools --test`: PASS.
- `scripts/mesh-autowire --test`: PASS.
- `scripts/mesh-doctor --test`: PASS.

The migration itself remains unlanded: at HEAD `fe7ee678`, 254 changed-path entries under
`scripts/uxn/`, `scripts/ux/`, and `scripts/tests/uxn/` are staged. A fresh `rg -l 'scripts/uxn'
scripts tests job` census still finds old-path references in runtime scripts and test drivers,
including `mesh-doctor`, `mesh-tick`, `mesh-dispatch`, `mesh-load-gate`, `mesh-resource-guard`,
`mesh-uxn-drift`, and `scripts/tests/uxn/test-chibicc`. No matching reference was present in the
current `~/.mesh/reflexes.cron`.

The repository's `mesh-land` contract centralizes genome commits in the steward and requires review
for `--apply`. Its current dry run reports 263 settled candidates across the shared worktree,
including unrelated files and an in-flight `gossip.rom`; applying that mixed batch from this genome
window is not a safe prerequisite. No landing, deploy, or shim removal was performed.

## Disposition and next action

The doctor's transient check is clear, but the parent cannot resume: the UXN migration is not landed,
old-path callers remain, and post-land deploy/autowire/doctor plus caller-census gates have not run.
Keep `retire-layout-shims` blocked. After the mesh-land steward lands the migration, rerun the real
post-land deploy/autowire/doctor and old-path caller-census gates, verify installed and reflex
resolution, then consider only individually qualified shims for retirement.
