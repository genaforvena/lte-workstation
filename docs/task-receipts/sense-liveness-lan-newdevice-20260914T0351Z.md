# Sense liveness — `lan-newdevice` on mesh-home — 2026-09-14

## Disposition

Keep `mesh-lan-newdevice` marked **DECAYED** (existing source annotation dated 2026-09-13).
Its `--test` passes offline fixtures, while a current live probe cannot read either router DHCP
leases or the LAN ARP fallback. The last real LAN beat is from 2026-09-02 and is not a current
reading. The 15-minute `mesh-perimeter --edge` caller remains wired; do not read its `UNREACHABLE`
as an empty or calm LAN. Reconsider decay only after a real lease/ARP read refreshes the beat.

## Bounded evidence windows (UTC)

Measured at 2026-09-14T03:51:58Z. The installed schedule is
`9-59/15 * * * * mesh-perimeter --edge` (96 nominal slots/day). Syslog contains timestamped
CRON `CMD` launch records for the caller; its network path calls `mesh-lan-newdevice --status`.

| Evidence | 24h: Sep 13 03:51:58–Sep 14 03:51:58 | 7d: Sep 7 03:51:58–Sep 14 03:51:58 |
|---|---:|---:|
| Nominal caller slots | 96 | 672 |
| Timestamped caller launches | 66 | 634 |
| Slots without a recorded launch | 30 | 38 |
| Last real `.lan-newdevice.beat` | Sep 2 20:24:22 | Sep 2 20:24:22 |
| Fresh real beats in window | 0 | 0 |
| Fresh beats / recorded caller launches (upper bound) | 0/66 | 0/634 |
| Fresh beats / nominal slots | 0/96 | 0/672 |
| Child attempts completed / empty results / unreachable results | UNKNOWN | UNKNOWN |

Caller launches are an upper bound on completed child reads, not a fabricated child denominator.
The beat's mtime is the producer's real-read artifact; the `.lan-newdevice-blind` marker records
that the reflex ran but could not observe the LAN. At 03:51Z, the isolated live `--status` probe
returned `router DHCP + LAN ARP both unreachable — can't assess (not an alarm)`. This confirms the
current blind state only; it does not assign outcomes to earlier launches.

## What history is absent

- `/var/log/syslog` and `.1` retain caller `CMD` timestamps across both windows, but 30 and 38
  nominal slots respectively have no recorded launch. Those slots are UNKNOWN (including possible
  power-off); they are not clean observations.
- `mesh-perimeter` retains transition notices, not one row per child attempt. There is no
  timestamped child-attempt/outcome tape, so exact completed LAN reads and empty versus unreachable
  result counts are UNKNOWN in both windows.
- The live `--test` is fixture-only: it passes its classifier/keying gates but proves no current
  LAN read. Its green result is not counted as hardware coverage.

## Organ probes and fresh-artifact check

- `mesh-reflex-health --check`: 36 scheduled per-run artifacts fresh; `lan-newdevice` is explicitly
  BLIND (fresh blind marker, last real beat frozen). The report also names `wifi-link` as BLIND,
  `kbd-activity` and `wifi-rf` as organ-absent, and several overwrite-only artifacts; those are not
  reclassified as calm.
- `mesh-sensorium` at 03:48Z read local thermal sensors (CPU 72.5°C, GPU 47.0°C, NVMe temperatures),
  enumerated live audio devices, found no Bluetooth adapter, and completed a Wi-Fi scan with 0 APs.
  No adapter / no AP is not a positive proximity observation. `mesh-health` reported the router
  offline (last seen 86 days ago) and Redmi phone offline (10 days ago).
- Note3 direct real-read tests passed for ambient (996.74 hPa, 22.0423°C, 52.1695%), battery, phone
  orientation, proximity, and light. The motion read is not healthy: it repeatedly reports x/y
  accelerometer axes railed at int16 saturation; `mesh-note3-motion --test` says the lane is green
  but the organ is dead. This is a hardware fault report, not usable motion evidence.
- After confirming the LAN decay, a direct `mesh-note3-ambient` real read at 03:51:37Z wrote the
  fresh 41-byte `~/.mesh/.note3-ambient-state` (`996.525 hPa, 21.8908°C, 52.9605%`). This is a
  verified live artifact from a separate reachable organ; it does not imply LAN recovery.

No commit was made. No schedule or security baseline was edited.
