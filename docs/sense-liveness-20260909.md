# Sense liveness — 2026-09-09

## Finding

`lan-newdevice` is scheduled and smoke-green but blind: its last real LAN read is
532539 seconds old, while its blind marker advanced during this turn. The live
source probe reported `router DHCP + LAN ARP both unreachable — can't assess (not
an alarm)`. This is an honest `BLIND/UNKNOWN` decay, not a reflex failure.

## Probe matrix

| organ | `--test` result |
|---|---|
| sensorium | rc 0 |
| location | rc 2, phone unreachable |
| light | rc 124, timeout |
| body-motion | rc 2 |
| room-sense | rc 124, timeout |
| wifi-motion | rc 0 |
| ambient-clock | rc 0 |
| operator-state | rc 0 |
| situation | rc 124, timeout |
| sense-monitor | rc 0 |
| sensor-log | rc 0, no Wi-Fi scanner warning |
| arrivals | rc 0 |
| lan-newdevice | rc 124 under bounded smoke probe; live status path below |
| macsocks-health | rc 0 |

## Fresh live evidence

- `mesh-lan-newdevice --status`: rc 0 at `2026-09-09T00:19:45Z`–`00:19:57Z`;
  emitted the explicit no-assessment line and no LAN lease artifact.
- Blind marker mtime advanced from epoch `1788913128` to `1788913197`.
- `mesh-reflex-health --check`: rc 0; 38 per-run reflexes fresh; `lan-newdevice`
  remains `organ-blind`, with marker 5 seconds old and real reading 532539 seconds
  old.
- `mesh-needs --check`: rc 0, `needs: none`; expiring ruling
  `reflex:lan-newdevice` is visible through `2026-09-16T00:19:23Z`.
- `mesh-chat` posted one `[sense]` evidence line at `2026-09-09T00:20:31Z`.

No source or deployed script was changed and nothing was committed.
