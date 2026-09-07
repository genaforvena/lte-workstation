# TG scripts layout audit — target layout and migration slices

Chain: `tg-scripts-layout-audit-20260907/propose-layout-and-tasks`  
Owner: `genome`  
Produced: 2026-09-07T16:52Z  
Inputs: [design](tg-scripts-layout-audit-design-20260907.md), [inventory map](tg-scripts-layout-audit-map-20260907.md)

## Decision

`scripts/` should become a compatibility-preserving source tree with four runtime domains and
two explicit non-runtime domains:

```text
scripts/
  core/                 shared mesh/task/ledger/claim/context primitives
  communication/        Telegram, board, room, relay, notify and delivery adapters
  integrations/         phone, body, camera, network and external-system adapters
  operations/           reflexes, watchers, recovery, deployment and migration tools
  tests/                test drivers and fixtures that are not installed as tools
  ux/                   UXN source, ROM/SYM assets and its build manifest
job/                    unchanged, self-contained job lane (tools + docs + funnel)
```

These are target boundaries, not a bulk-move instruction. A source file belongs in the domain that
owns its runtime contract; a wrapper stays with the contract it exposes, and a launcher/unit pair
is one deployment unit. Ambiguous families remain decisions at slice time:
`mesh-*watch` (sensor or operations), `mesh-verify*` (gate or test driver), and platform-specific
`mesh-imac-*`/`mesh-note3-*` (integration or sensor).

Generated Python cache files and compiled UXN output must not be deleted or excluded by naming
intuition. First establish tracked/generated status and a UXN build manifest. `job/` is already a
deliberate boundary and is not folded into `scripts/`.

## Why this shape is safe

The repository currently has 1,059 regular files below `scripts/`, 802 executable and 257
non-executable. The earlier map captured 1,058/801/257; the one-file increase is working-tree
state and is retained as an explicit observation, not silently rewritten into history. The map's
later nested UXN count is also not a guarantee that all current nested material is UXN: the live
tree contains `scripts/reticulum/` and `scripts/uxn-packet-gate/` candidates, so the first migration
must use a manifest rather than a blanket directory glob.

The dangerous dependency is enumeration, not the directory name itself. Evidence from the current
tree:

| consumer | current behavior | required target behavior |
|---|---|---|
| `bootstrap.sh` | installs every direct `scripts/*` child; nested tools disappear | consume the typed manifest/recursive enumerator and skip tests/assets/units |
| `setup.sh` | explicit legacy copies plus systemd units | resolve legacy source paths through the manifest; verify unit `ExecStart`/source parity |
| `mesh-sync-tools` | scans direct `scripts/mesh-*`, `job/mesh-*`, and selected `scripts/*/mesh-*`; top-level shim owns basename collisions | scan the manifest and retain one owner per installed basename |
| `mesh-doctor` | independently scans repo, deployed tools, reflex headers and `job/*` | use the same manifest and report an unclassified/unlandable path loudly |
| `mesh-autowire` | derives reflex candidates from cadence headers in repo/deployed paths | wire only manifest-listed deployable entries and compare source/deployed cadence |
| `mesh-land` | validates candidates and deploys the existing tool corpus | land manifest changes before moving a live reflex; retain rollback shims |
| `mesh-vitality` | several analyses hard-code `scripts/mesh-*` and `job/mesh-*` cohorts | consume the manifest or explicitly publish a compatibility cohort during migration |

The manifest is the single source of enumeration truth. It must record source path, installed
basename, domain, kind (`tool`, `unit`, `asset`, `fixture`, `library`), deploy policy, cadence
policy, and compatibility owner. No scanner may silently fall back to a partial glob.

## Reversible migration slices

Each slice is independently landable. Before a slice, record the current source/deployed mapping;
after it, run the slice gates. Rollback is the inverse move, restoration of the old shim and
installed copy, followed by the same parity and wiring checks.

1. **Manifest and enumerator contract (no moves).** Add a checked-in manifest schema and one
   library/command that emits the complete typed inventory, including `job/` and nested lanes.
   Change each enumerator to consume it while preserving today's top-level paths. Gate: fixture
   entries for a top-level tool, nested tool, unit, fixture, generated cache and `job` tool;
   assert no silent omission and stable installed basenames. Roll back by removing only the
   manifest reader and its tests.

2. **Operations pilot.** Move one low-fan-in operational wrapper into `scripts/operations/` and
   leave an executable top-level shim at the old path. Deploy the canonical source and ensure the
   shim resolves the canonical implementation without recursive self-resolution. Gate: source vs
   `~/.local/bin` hash/owner report, `--test`, `mesh-doctor --test`, `mesh-sync-tools --test`,
   `mesh-autowire --test`, and an actual cadence/reflex lookup. Roll back by restoring the source
   path and removing the new directory entry; do not delete the installed copy first.

3. **Core and communication families.** Migrate one family at a time, starting with a low-fan-in
   adapter and only then a primitive. Preserve old repository paths until all direct callers and
   tests use the manifest path. Gate every family on focused tests, syntax checks, deployed
   resolution, and Telegram/board credential boundaries where applicable. Core tools require a
   caller census because `mesh-task`, `mesh-claim`, `mesh-ledger`, and handoff tools have high
   fan-in.

4. **Integrations.** Migrate phone/body/network adapters in isolated batches grouped by device or
   protocol, not by filename prefix. Gate each live sensor with its real `--test` artifact,
   freshness/coverage evidence, and no duplicate reflex cadence. An unavailable sensor is an
   honest `n/a`/failure, never a successful fixture result.

5. **Tests, fixtures and UXN.** After runtime paths are stable, move only explicitly classified
   test drivers/fixtures and UXN source/assets. Add a UXN build manifest before relocating any
   ROM/SYM/bin output. Gate with repository test invocation from outside the repo root, build
   output validity, and proof that production deployment excludes fixtures/assets.

6. **Retire compatibility shims.** Only after one full deploy/autowire/doctor cycle and a clean
   caller census. Record the removal as a separate change. Gate with `rg` for old paths, installed
   basename parity, systemd resolution, and a rollback rehearsal from the prior manifest.

## Required acceptance evidence

The layout work is not complete when directories exist. For every slice, retain:

```text
manifest --check                         # all source kinds classified; no silent omissions
manifest --parity                         # source ↔ ~/.local/bin owner/basename report
mesh-sync-tools --test                    # deploy drift and collision behavior
mesh-doctor --test                        # executable/orphan/reflex/unit checks
mesh-autowire --test                      # cadence source/deployed wiring
<migrated-tool> --test                    # focused contract
shellcheck/syntax or language check       # according to the migrated file kind
systemctl --user cat <unit>               # for a moved launcher/unit pair
crontab -l / relevant reflex lookup       # for a moved cadence tool
```

The test harness must run from a temporary directory, not only the repository root. A passing
self-test is insufficient unless the corresponding installed copy and live reflex/service path
also resolve.

## Open decisions and next action

No files were moved, deleted, installed, or rewired by this audit. The next authorized slice is
the manifest/enumerator contract. Its first concrete task is to inventory all current enumerator
patterns and write the fixture matrix; only after that may a pilot family be selected. The queued
successor `propose-layout-and-tasks` is now represented by this artifact; it should be marked done
against this path, with the manifest slice opened separately rather than conflated with this audit.

## Verification captured for this artifact

```text
sha256sum docs/tg-scripts-layout-audit-map-20260907.md
  f7a5f01326715c46619bbfe1df043671a35b2d6a4f31cb11e7bb6313e94763ed
find scripts -type f                         => 1059
find scripts -type f -perm -111               => 802
find scripts -type f ! -perm -111             => 257
rg -l --glob 'scripts/*' 'reflex-cadence:' | wc -l => 345
rg -l --glob 'scripts/*' 'orphan-ok:' | wc -l      => 186
repo direct mesh tools                      => 723
deployed ~/.local/bin mesh tools             => 747
repo-only / deployed-only names              => 1 / 25
nested candidates observed                   => scripts/reticulum/, scripts/uxn-packet-gate/, __pycache__
```

The deployed comparison is a baseline only: the 25 deployed-only names are not removed here;
they require a separate drift classification. Likewise, the untracked working tree contains
unrelated changes and was preserved.
