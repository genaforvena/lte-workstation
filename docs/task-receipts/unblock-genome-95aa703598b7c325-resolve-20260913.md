# UXN layout migration blocker resolution

Date: 2026-09-13
Task: `unblock/genome/95aa703598b7c325/resolve`
Parent task: `tg-scripts-layout-migration-20260912/retire-layout-shims`

## Live-state audit

The blocker task was still active for `genome` when checked. The parent migration remains
unlanded, and step `retire-layout-shims` remains blocked on dependency. The blocker receipt
[`retire-layout-shims-gate-20260912.md`](retire-layout-shims-gate-20260912.md) correctly names the
missing prerequisite: land the UXN classification migration, then resolve the mesh-doctor test
failure and pass the post-land deploy, autowire, doctor, and caller-census gates before removing
any shim.

## Narrow prerequisite fixes landed

- `20667c5e` — Enumerate nondeployed compatibility symlinks. `mesh-manifest` now inventories file
  and directory symlinks and rejects broken links; the regression fixture covers a nested file
  symlink and a directory symlink.
- `cfc47700` — Route relocated UXN data through land-only classification. `mesh-land` recognizes
  the relocated UXN source, fixture, ledger, goal, gate, and license paths so the migration can be
  classified and landed without deploying those data files as tools.

Both commits were made with `mesh-land`; the deployed `mesh-land` content hash matched the wake's
revision `70efcdca6bd5139e130de3fcbd5dfa17bfa2bd0b58dc94ef591f8dc6be1f6a98`.

## Verification and remaining work

The focused UXN layout, build-manifest, lease-gate, band-gate, and ROM-binary-contract checks passed.
The source and deployed `mesh-manifest` hashes matched, and the deployed manifest check passed.
`mesh-doctor --test` passed on the source and deployed tool during this audit; the earlier reported
failure did not reproduce consistently, so the post-land doctor gate remains required.

The UXN migration itself is still staged and unlanded. A whole-migration manual apply was refused
safely because one subject cannot describe 257 semantic units. Do not remove shims or mark the
parent step complete until the migration is landed and the required post-land gates pass. The
deployed `mesh-land --check` ran against revision `70efcdca6bd5139e130de3fcbd5dfa17bfa2bd0b58dc94ef591f8dc6be1f6a98`, exited 1, and posted a `[strand]` report for 58 steward-required candidates. The report includes UXN paths whose checks are missing or failing (`test-arith32`, `test-arith64`, `test-sense-gate`, `test-series-stats`, `test-spearman`, and other relocated test/data paths). It also includes unrelated workspace candidates, so this is evidence to hold broad landing, not authorization to bundle the workspace. No broad apply was run.
