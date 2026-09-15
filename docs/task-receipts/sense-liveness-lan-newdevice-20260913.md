# Sense liveness — `lan-newdevice` — 2026-09-13

Disposition: **DECAYED on this node**. `mesh-lan-newdevice` remains in the scheduled perimeter
path so it can detect recovery, but its current router DHCP and LAN ARP inputs are both unreachable.
Its green `--test` exercises offline fixtures; it does not establish a live LAN reading.

## Bounded evidence windows

Windows are UTC, bounded at 2026-09-13T00:45:18Z:

| Evidence | Last 24h: 2026-09-12T00:45:18Z–2026-09-13T00:45:18Z | Last 7d: 2026-09-06T00:45:18Z–2026-09-13T00:45:18Z |
|---|---:|---:|
| Nominal `mesh-perimeter` cron slots (`9-59/15`) | 96 | 672 |
| Timestamped CRON launches in `/var/log/syslog*` | 90 | 627 |
| Slots with no recorded CRON launch | 6 | 45 |
| Fresh real LAN reads | 0 | 0 |
| Timestamped `perimeter.log` transition notices | 0 | 16 |
| Those notices with `N=UNREACHABLE` | 0 | 16 |

The cron expression is `9-59/15 * * * *`; `mesh-perimeter --edge` invokes the LAN status leg.
The CRON rows establish parent launches, not a separately logged child completion. The six and 45
slots without a CRON row are UNKNOWN: silence may include power-off, and is not a healthy reading.
`perimeter.log` is edge/transition-only, not one row per run; its 16 notices in the 7-day window all
say `N=UNREACHABLE`, but absence of a notice cannot classify an individual scheduled attempt.

The last-good artifact `/home/mesh-home/.mesh/.lan-newdevice.beat` is empty by design and remains
mtime-frozen at 2026-09-02T20:24:22Z, outside both windows. The overwrite-only blind marker was
fresh at the live probe, but it records an unreachable attempt, not a LAN measurement. Thus there
were no fresh real artifacts in either window; coverage is zero of the recorded parent launches
(0/90 and 0/627). Per-run child outcomes and exact child-attempt counts are not retained.

## Live probe and disposition

- `mesh-reflex-health --check` separated the fresh blind marker from the frozen last-real-read
  artifact and classified `lan-newdevice` as BLIND, not healthy.
- `mesh-lan-newdevice --test` passed 67 fixture assertions. The live `--status` read returned
  `router DHCP + LAN ARP both unreachable — can't assess (not an alarm)`.
- Refreshed the source decay annotation in `scripts/mesh-lan-newdevice`; the scheduled revival probe
  remains wired. No scheduler behavior was changed.
- Cross-device inventory (`mesh-sense-map --refresh`) reached 3/11 devices: mesh-home and Note3 had
  listed organs; the other nodes with offline status remain UNKNOWN. `mesh-sensorium --compact`
  produced live thermal data, while presence and Wi-Fi scan were unavailable. The direct local light
  capture gate passed; the audio-level probe returned a timestamped shared-stream read.

## Fresh real artifacts after the disposition

- Note3 light sensor: `mesh-note3-light-raw --edge` read `STABLE (raw=2300 lux=0)` at
  2026-09-13T00:49:20Z and refreshed `/home/mesh-home/.mesh/.note3-light-raw-state` (44 bytes).
- Note3 climate: live result at 2026-09-13T00:39:57Z, `STABLE`, inputs 2/3; the light sub-input was
  honestly `OFFLINE`.
- Shared audio stream: `mesh-ambient-level --json` returned `MODERATE`, `rms_db=-29.9`,
  `coverage=0.984`, `age_s=0`, timestamp 2026-09-13T00:42:14Z.

No commit made. Recovery requires a reachable router/DHCP or LAN-ARP source and a new real
`lan-newdevice` beat; the old value stays decayed until then.
