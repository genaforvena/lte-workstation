# Ideas queue coverage — 2026-09-07

Ask: `tg-operator-ledger-coverage-20260907`  
Owner: `genome`  
Source: `~/.mesh/ideas-queue` read at 2026-09-07T15:00Z (live count: 28 `[~]` rows; the witness snapshot said 29, so one row had already changed before this pass).

## Disposition rule

Every live `[~]` row is listed below by its source line and a short SHA-256 prefix of the complete
queue line. `retire` is an explicit negative design decision, not a silent drop. `bounded-task` is
ledgered in `~/.mesh/task-chains/ideas-queue-escalations.json`, with owner, artifact, and verification
fields supplied by `mesh-task`.

| # | queue line | key | class | disposition / ledger |
|---:|---:|---|---|---|
| 1 | 6 | 7f539d134974e2e3 | retire | stale speculative UUID-link experiment; no current bounded consumer |
| 2 | 7 | fc83d6befa1834e8 | retire | JIT worker inference proposal lacks a target compiler path and current owner |
| 3 | 9 | dd4546ea4f84195b | retire | Forall-link parsing has no identified proof consumer |
| 4 | 12 | 9dc1a7b903b69ad4 | retire | tmux-wide failure broadcast duplicates existing mesh routing and is underspecified |
| 5 | 16 | 2e101bfc68d845c2 | retire | superoptimizer expansion is broad, unbounded, and has no current optimizer artifact |
| 6 | 17 | 5d106483e6a0e272 | retire | Opbox text sync would add a second substrate and lacks a bounded acceptance test |
| 7 | 18 | 138510a40a4cd37d | retire | distributed metadata query language has no current reader or schema |
| 8 | 19 | 88fdec3878f14f42 | retire | chaos emulator is already represented by existing `scripts/mesh-chaos` coverage |
| 9 | 53 | 804986bc686f1f8b | retire | log workflow parser has no current consumer; keep as future design only |
| 10 | 1130 | 29bb944d7254c355 | retire | correlation is a one-window hypothesis with no invariance evidence |
| 11 | 1186 | 1587b489af7880cc | retire | correlation is a one-window hypothesis with no invariance evidence |
| 12 | 1252 | 16574b5519342c8a | retire | correlation is a one-window hypothesis with no invariance evidence |
| 13 | 1391 | 7924c0f3d658d952 | retire | marginal lift and no durable causal evidence; do not promote to reflex |
| 14 | 1396 | 0ad0e40b2e035fa6 | retire | marginal lift and no durable causal evidence; do not promote to reflex |
| 15 | 1475 | c49c4d87cb54f414 | bounded-task | diagnose/decay/expiring-mute decision; chain step `mesh-series-stats-disposition` |
| 16 | 1483 | 33ed0f4e1d928adf | retire | unstable environment-specific correlation; no generalized reflex |
| 17 | 1508 | 25e934169d30e315 | retire | correlation is observational and lacks a stable blanket |
| 18 | 1518 | c2f47b2c51c3135b | retire | generated pairing has no demonstrated value or acceptance artifact |
| 19 | 1619 | f08d107f445dddfa | retire | unstable environment-specific correlation; no generalized reflex |
| 20 | 1764 | bd320f38383e781a | retire | unstable environment-specific correlation; no generalized reflex |
| 21 | 1848 | cc75f1ee0b84f622 | bounded-task | diagnose/decay/expiring-mute decision; chain step `wifi-rf-disposition` |
| 22 | 1853 | 5c45f5345e12e7c6 | bounded-task | diagnose/decay/expiring-mute decision; chain step `social-context-disposition` |
| 23 | 1854 | 7008824fff025ac8 | bounded-task | diagnose/decay/expiring-mute decision; chain step `lan-newdevice-disposition` |
| 24 | 1856 | 7f1f256010de0e72 | retire | explicitly marked unstable across environments; no generalized action |
| 25 | 1857 | 5ef0e1f1314b038d | retire | explicitly marked unstable across environments; no generalized action |
| 26 | 1858 | 548bc606421ec74e | retire | explicitly marked unstable across environments; no generalized action |
| 27 | 1859 | f3e76e87b390d0f3 | retire | explicitly marked unstable across environments; no generalized action |
| 28 | 1860 | b1e1419e41ddc650 | retire | explicitly marked unstable across environments; no generalized action |

## Verification

- `rg -c '^\[~\]' ~/.mesh/ideas-queue` returned `28` at snapshot time.
- `scripts/mesh-ideate --test` passed: inventory and novelty-space checks completed without queue mutation.
- The four non-retired rows are ledgered as bounded steps in `mesh-task` chain
  `ideas-queue-escalations`; the remaining 24 rows have explicit retire/design reasons above.
- Queue closure receipts are posted to the mesh board with the exact source keys; this artifact is the
  mapping and remains the evidence until the four bounded decisions themselves close.
- The requested receipt text `[ack] ack:126c293785b392e5` was posted on the board. The targeted
  `mesh-chat --to witness ...` path rejected `witness` because no live target was registered at that
  instant; the broadcast receipt is present and searchable in the board archive.

## Honest remaining work

The four escalation steps were classified and owned, not silently dropped. Their branch-specific
decisions and closure evidence are recorded below.

## Escalation dispositions — 2026-09-07T15:01Z

| step | decision | evidence | verification / expiry |
|---|---|---|---|
| `wifi-rf-disposition` | expiring mute | `mesh-reflex-health` reports `wifi-rf` as `organ-absent`; its `--test` exits 2 because the RF organ is absent on this node | `mesh-needs --rule reflex:wifi-rf 7 ...`; visible until `2026-09-14T15:01:12Z`, then re-files if still warranted |
| `mesh-series-stats-disposition` | diagnose: no current repair or decay | `mesh-series-stats --test` passes; `--claims` reads the live 2093-row records artifact; `mesh-dash` is its live reader | no mute or retirement; the prior stale decay verdict is not evidence against the current wired organ |
| `social-context-disposition` | expiring mute | `mesh-reflex-health` reports stale/power-off `UNKNOWN`; phone and BLE are unavailable, so this is not a repairable local reflex failure | `mesh-needs --rule reflex:social-context 7 ...`; visible until `2026-09-14T15:01:21Z`, then re-files if still warranted |
| `lan-newdevice-disposition` | expiring mute | `mesh-reflex-health` reports the LAN organ as absent/blind; `mesh-lan-newdevice --test` exits 2 because the organ is absent on this node | `mesh-needs --rule reflex:lan-newdevice 7 ...`; visible until `2026-09-14T15:01:22Z`, then re-files if still warranted |

The three mutes are visible, bounded, and per-reflex; they are not permanent suppression. The
`ideas-queue-escalations` chain is complete, with each step closed against this artifact. A fresh
`mesh-needs --check` after the rulings must render the accepted deficits as `MUTED`, while
`mesh-reflex-decay --candidates` remains empty.
