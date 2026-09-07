# TG scripts layout audit — inventory and map

Chain: `tg-scripts-layout-audit-20260907/inventory-and-map`  
Owner: `genome`  
Captured: 2026-09-07T15:56Z  
Scope input: [audit design](tg-scripts-layout-audit-design-20260907.md)

## Finding

`scripts/` is not one runtime corpus. It is a flat executable surface containing mesh command
primitives, communication adapters, hardware/network/phone sensors, reflexes and watchers,
deployment/service files, test drivers, and a nested UXN implementation with compiled assets. The
separate `job/` lane is already a deliberate boundary and must remain separate during any future
layout work.

The highest-risk dependency is path-based enumeration: bootstrap installs every direct child of
`scripts/`; setup has a small explicit legacy install list; `mesh-sync-tools`, `mesh-land`,
`mesh-doctor`, `mesh-autowire`, and `mesh-vitality` have their own source/deployed/reflex scans.
Moving a tool therefore requires changing the enumerators and proving both repository and deployed
resolution. A directory can otherwise disappear from the live mesh without an error.

## Corpus inventory

The following counts are from the working tree at capture time, not a claim about only committed
files:

| surface | evidence |
|---|---:|
| all regular files below `scripts/` | 1,058 |
| executable files below `scripts/` | 801 |
| non-executable files below `scripts/` | 257 |
| direct children of `scripts/` | 1,002 |
| nested files below `scripts/uxn/` | 56 |
| files with no extension | 789 |
| Python files (`.py`) | 6 |
| shell files (`.sh`) | 18 |
| C/header/Objective-C/Swift source (`.c`, `.h`, `.m`, `.swift`) | 60 |
| service/timer units | 17 |
| UXN source/assets (`.tal`, `.rom`, `.sym`) | 76 |
| files declaring `# reflex-cadence:` | 345 |
| files declaring `# orphan-ok:` | 186 |

The executable count includes nested UXN binaries and fixtures. The corpus is therefore not a
safe input to a future `scripts/*` → one target directory move without a file-kind policy.

## Runtime-role map

Classification is by observed name, headers, and call sites. These are audit domains, not proposed
directories yet; ambiguous items stay marked for the layout step.

| role | representative sources | observed contract / risk |
|---|---|---|
| core primitives | `mesh-task`, `mesh-land`, `mesh-board`, `mesh-ledger`, `mesh-promises`, `mesh-claim`, `mesh-handoff`, `mesh-context` | Shared state and coordination. High fan-in; move only with compatibility shims and chain/tool tests. |
| communication | `mesh-chat`, `mesh-chat-deliver`, `mesh-tg`, `mesh-channel*`, `mesh-room*`, `mesh-relay`, `mesh-tell`, `mesh-notify` | Telegram, board, room, relay and delivery paths. Single-writer and credential boundaries apply. |
| sensors / integrations | `mesh-phone-*`, `mesh-note3-*`, `mesh-camera`, `mesh-cam-*`, `mesh-wifi-*`, `mesh-bt-*`, `mesh-cell-*`, `mesh-lan-*`, `mesh-vpn-*`, `mesh-weather`, `mesh-gmail-note3` | Hardware, network, phone and external adapters. Many are cadence-wired and depend on live artifacts. |
| operations / reflexes | `mesh-doctor`, `mesh-autowire`, `mesh-vitality`, `mesh-sync-tools`, `mesh-watch*`, `mesh-*watch`, `mesh-clear`, `mesh-restore`, `mesh-window-*`, `mesh-mind-*` | Liveness, deployment, recovery, and watchers. Their scanners are themselves migration gates. |
| tests / fixtures / drivers | `test-*`, `mesh-chaos-*`, `mesh-child-sim`, `mesh-verify*`, `mesh-selftest`, UXN `test-*`, `scripts/uxn/*-fixtures` | Some are executable tools; some are test-only. Do not deploy fixtures as production tools. |
| compiled / source subtrees | `scripts/uxn/`, `macmic.swift`, `mesh-imac-cam.m`, `tiny_fleet_pool.py`, `vpn-health.py` | Build/runtime language and platform exceptions. UXN has its own `README`, build script, binaries and assets. |
| legacy/explicit install surface | `ngrok-notify.sh`, `bore-mtg.sh`, `ngrok.service`, `bore-mtg.service`, `mtg-watchdog.*` | `setup.sh` handles only selected legacy files and systemd units; this is not equivalent to mesh tool deployment. |

Ambiguous families needing an owner decision in the target-layout step include `mesh-*watch`
(sensor versus operations), `mesh-verify*` (test driver versus core gate), and platform-specific
`mesh-imac-*` / `mesh-note3-*` tools (integration versus sensor).

## Callers, wiring, and installed copies

| producer / reader | observed evidence | implication for relocation |
|---|---|---|
| `bootstrap.sh` | loops over `"$REPO_DIR"/scripts/*`, skips only service/timer/backup suffixes, installs direct children to `~/.local/bin` | A nested target is invisible unless bootstrap gains a recursive, typed enumerator. |
| `setup.sh` | explicitly copies `scripts/ngrok-notify.sh` and `scripts/bore-mtg.sh`; copies two service units to `~/.config/systemd/user` | Legacy deployment must be migrated independently and service paths verified with systemd. |
| `mesh-sync-tools` | scans top-level `scripts/mesh-*`, `job/mesh-*`, and `scripts/*/mesh-*`; skips a nested copy when a top-level shim owns the basename | The current shim rule is intentional. A move needs source/deployed parity and collision tests. |
| `mesh-doctor` | checks installed `~/.local/bin/mesh-*`, repository tools, `job/*`, reflex headers, executable bits, and systemd unit filenames | Doctor must be updated with every new lane; otherwise orphan/deploy checks can go silent. |
| `mesh-autowire` | derives candidates from repository tools carrying cadence metadata and deployed tools | Cadence metadata and deployed path are coupled; moving a reflex without both breaks wiring. |
| `mesh-land` / `mesh-vitality` | referenced by charter and scanner comments as landing/liveness gates over the tool corpus | A passing tool self-test does not prove the moved reflex is wired or live. |
| `tests/` | tests invoke `$repo/scripts/<tool>` directly; job tests invoke `$root/job/<tool>` and sometimes `~/.local/bin/<tool>` | Keep compatibility paths during slices or update tests in the same change. |
| `job/` | job tools call sibling files and Python modules via `dirname`, imports, and `~/.local/bin` | Preserve the lane as a unit; do not classify it as ordinary `scripts/mesh-*`. |

Representative direct callers found outside `scripts/`: `tests/test-mesh-task-ledger-sync.sh`,
`tests/test-mesh-chat-deliver.sh`, `tests/test-mesh-witness-*`, `tests/test-job-*.sh`,
`job/mesh-job-funnel`, `job/mesh-job-confirm`, `job/mesh-job-apply-getmatch`, and the charters
for `genome`, `adint`, `health`, and `senses`. The test corpus is path-sensitive and is evidence
of real consumers, not merely documentation.

## Duplicate / dead-code candidates (not yet verdicts)

These are candidate families requiring focused review, not permission to delete or merge:

* `mesh-cam-watch` and `mesh-cam-watch.service`, `mesh-card-watchdog` and its service/timer,
  `mesh-liveness-loop` and its service, `mesh-textin` and its service, `mesh-tuner-eye` and its
  service, and `mesh-voice-rx` and its service: paired launcher/unit files are expected but must
  be treated as one deployment unit.
* `mesh-imac-cam`, `mesh-imac-cam-watch`, `mesh-imac-cam.m`, and `mesh-camera`: overlapping names
  indicate platform adapters, not proof of duplicate behavior; compare callers before moving.
* `mesh-body-*`, `mesh-phone-*`, and `mesh-note3-*`: overlapping sensor domains may be layered
  adapters, so semantic duplication cannot be inferred from prefixes.
* UXN compiled files under `scripts/uxn/bin/` and generated `.rom`/`.sym` files: possible generated
  artifacts, but they are currently adjacent to source and referenced by UXN tooling; establish a
  build manifest before excluding them.
* `scripts/__pycache__/` and `job/__pycache__/` are generated/dead deployment candidates. They
  should be excluded from a production layout only after checking tracked status and land/sync
  behavior.

No item is labelled dead solely because `rg` found no caller: on-demand tools, reflex candidates,
and installed copies have distinct consumers. The next step must use a per-file caller report and
live deployed comparison before removal or consolidation.

## Verification commands and captured evidence

```text
find scripts -type f | wc -l                         => 1058
find scripts -type f -perm -111 | wc -l             => 801
find scripts -type f ! -perm -111 | wc -l           => 257
rg -l --glob 'scripts/*' 'reflex-cadence:' | wc -l => 345
rg -l --glob 'scripts/*' 'orphan-ok:' | wc -l      => 186
rg ... '(scripts/|job/mesh-job|\.local/bin/mesh-)'  => callers in bootstrap.sh, setup.sh, job/, tests/, charters
rg ... '(systemd|\.service|\.timer|cron|reflex|mesh-autowire)' => deployment/reflex wiring in bootstrap.sh, setup.sh, scripts/, job/
```

The count changed from the frame artifact's 1,057/800 snapshot because the working tree contains
new or restored files; this map records the later observation and keeps the measurement explicit.
No files were moved, deleted, installed, or wired by this step.

## Handoff to the next chain step

Use this map to propose a target layout and migration slices. The first slice should be a
non-moving enumerator/manifest design or one isolated family with a top-level compatibility shim;
it must include source-vs-installed parity, syntax, focused `--test`, reflex/service resolution,
and rollback verification. Do not perform a bulk move from this artifact.
