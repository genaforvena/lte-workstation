# TG scripts layout migration audit — current-state reconciliation

Audited: 2026-09-12  
Inputs: [scope/design](tg-scripts-layout-audit-design-20260907.md), [inventory map](tg-scripts-layout-audit-map-20260907.md), [target layout and slices](tg-scripts-layout-audit-result-20260907.md), and [manifest contract](tg-scripts-layout-manifest-contract-20260907.md).

## Disposition

The existing target layout remains sound: keep `job/` as its own lane and classify `scripts/` into `core/`, `communication/`, `integrations/`, `operations/`, `tests/`, and `ux/`. These are intended ownership boundaries, not directories to create in bulk. Do not move files until all live enumerators that would lose sight of them consume a checked manifest, and preserve old top-level entrypoints as compatibility shims during each family migration.

The task is still live as a migration-plan audit, even though the original `tg-scripts-layout-audit-20260907` chain is complete. Its result artifact already defines the layout and broad slices; the missing work was to reconcile them with the present tree and make the next migration slices executable task rows. No bulk move is authorized or performed here.

## Current code and state checked

* `scripts/mesh-manifest`, `manifest/mesh-manifest.schema.json`, `tests/test-mesh-manifest.sh`, and the manifest contract are present. `mesh-manifest --check` currently validates 1,188 rows and reports no duplicate installed basenames. The focused fixture/duplicate test passes.
* The manifest describes itself as a complete typed inventory for `scripts/` and `job/`, but it is not yet the shared enumeration source for consumers. `bootstrap.sh` still installs direct `scripts/*` children. `setup.sh` retains its explicit legacy copies. `mesh-sync-tools`, `mesh-doctor`, `mesh-autowire`, `mesh-land`, and `mesh-vitality` still have independent glob/path logic, confirmed by current source inspection.
* Therefore the existing no-move manifest prototype is a valid foundation, not evidence that the first deployment-enumerator migration is complete. A nested move now would still be liable to disappear from bootstrap, reflex, doctor, or landing coverage.
* The repository has extensive unrelated dirty and untracked work. This audit changed only its own new planning artifacts and task-ledger state; it did not touch the pre-existing working tree.

## Ordered migration slices opened

The rows in [the migration plan](plans/2026-09-12-tg-scripts-layout-migration.tsv) form one sequential chain. Each has normal priority, no tags, and no design artifact attached (`tags=- design_artifact=-`). Their shared gates are: run from outside the repository root where relevant; preserve current top-level callers; check source/deployed basename and owner parity; run focused tool tests and syntax checks; verify service/reflex resolution for affected entries; and record an inverse rollback. A slice is not complete on self-test alone.

| order | slice | move allowed? | completion evidence |
|---:|---|---|---|
| 1 | Route bootstrap and legacy setup installation through the manifest while preserving current top-level entrypoints and unit paths. | No | Isolated temp-repo installer test, `mesh-manifest --check`, source/deployed parity, and service `ExecStart` resolution. |
| 2 | Convert sync/deploy drift and doctor/orphan scanners to manifest rows without changing current paths. | No | Their focused `--test` runs; fixtures prove nested entries, duplicate owners, and unknown rows fail loudly; deployed parity. |
| 3 | Convert autowire, land, and vitality enumeration to the same manifest contract. | No | Focused tests plus a real cadence/reflex lookup and proof that no old partial glob is deciding inclusion. |
| 4 | Select and migrate one low-fan-in operations wrapper into `operations/` with a top-level executable shim. | One isolated move | Caller census, non-recursive shim resolution, source/deployed identity, focused `--test`, and actual wiring lookup. |
| 5 | Migrate communication and integration adapters one family at a time, retaining old paths until callers move. | One isolated family per subtask | Per-family caller/credential or hardware boundary review, syntax and focused tests, deployed identity, and real service/reflex/sensor evidence. |
| 6 | Migrate core primitives one at a time after a caller census; do not batch high-fan-in task, claim, ledger, or handoff tools. | One primitive per subtask | Caller census, focused chain/ledger tests, compatibility-path coverage, deployed parity, and rollback rehearsal. |
| 7 | Move test drivers/fixtures and UXN assets only after runtime paths stabilize; define a UXN build manifest before relocating generated outputs. | Classified items only | Test invocation from a temp directory; production manifest excludes fixtures/assets; UXN build output validation. |
| 8 | Retire compatibility shims as a distinct final change after a full deploy/autowire/doctor cycle. | Yes, after gates | Old-path caller census is empty, installed basename and unit/reflex resolution pass, and rollback is rehearsed from the prior manifest. |

The family migration rows are authorization to plan and execute only the named narrow slice when it is dispatched; they do not authorize a bulk relocation. Ambiguous `*watch`, `mesh-verify*`, and platform-specific camera/phone families remain classified per caller and runtime contract at their own slice, not by filename guess.

## Verification performed

```text
scripts/mesh-manifest --check
  mesh-manifest: PASS (1188 complete rows; no duplicate installed basenames)
bash tests/test-mesh-manifest.sh
  mesh manifest contract: fixture matrix and duplicate guard pass
```

Source review also confirmed that manifest use is not yet wired into the enumerators listed above. The outputs establish that the contract tool is healthy; they do not establish consumer wiring or deployed parity, which are gates in slices 1–3.

## Canonical task-ledger reconciliation — 2026-09-12T04:50Z

The nine rows in `plans/2026-09-12-tg-scripts-layout-migration.tsv` are already registered as the
canonical sequential chain `tg-scripts-layout-migration-20260912`; no duplicate chain was created.
`mesh-task status tg-scripts-layout-migration-20260912` reports `open (1/9)`: the first slice,
`manifest-bootstrap-setup`, is the current row and is owned by `genome`. Its exact-owner pending
check exits 0. The remaining eight rows are open behind the current chain position, so dispatch
cannot skip ahead. The plan SHA-256 is
`09a9a5bc83ea1f481187d5bcdd68244407e5bd86b486f53119a5c88b62fba7fd`.

Fresh verification at reconciliation time:

```text
scripts/mesh-manifest --check
  PASS (1190 complete rows; no duplicate installed basenames)
bash tests/test-mesh-manifest.sh
  fixture matrix and duplicate guard pass
mesh-task check pending tg-scripts-layout-migration-20260912/manifest-bootstrap-setup genome
  exit 0
```

These checks validate the current manifest contract and the first migration row's ledger eligibility.
They do not claim that bootstrap/setup consume the manifest or that any migration slice has started.
No source files, deployments, services, reflexes, or directories were moved or changed by this audit.
