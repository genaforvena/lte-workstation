# Sense liveness audit — `lan-newdevice` — 2026-09-13T19:51Z

## Disposition

`lan-newdevice` remains **DECAYED on mesh-home**. `scripts/mesh-lan-newdevice` already carries a
`DECAYED 2026-09-13` annotation. Its scheduled caller is retained to expose recovery; the old
zero-byte LAN beat is not a current reading. This audit made no code, scheduler, or substrate
change and was not committed.

## Bounded evidence windows (UTC)

Windows end at 2026-09-13T19:47:15Z. The caller cadence is `9-59/15 * * * *` (96 nominal slots/day).
Parent starts are timestamped `CRON CMD` rows in `/var/log/syslog*`; they prove launch, not child
completion or a LAN read.

| Evidence | 24h: Sep 12 19:47–Sep 13 19:47 | 7d: Sep 6 19:47–Sep 13 19:47 |
|---|---:|---:|
| Nominal perimeter slots | 96 | 672 |
| Recorded `mesh-perimeter --edge` starts | 66 | 634 |
| Nominal slots without a recorded start | 30 | 38 |
| Fresh real `.lan-newdevice.beat` | 0 | 0 |
| Upper-bound coverage vs recorded parent starts | 0/66 | 0/634 |
| Coverage vs nominal slots | 0/96 | 0/672 |
| Timestamped perimeter transition rows | 4 | 20 |
| Transition rows with `N=UNREACHABLE` | 4 | 20 |

The last real beat remains zero bytes, mtime `2026-09-02T20:24:22Z`, outside both windows. The
blind marker is also zero bytes and was touched at `2026-09-13T19:50:53Z`; this records that a probe
ran without seeing the LAN organ, not a LAN observation. `perimeter.log` is transition-only, so the
4/20 unreachable rows do not count every child attempt. Exact child invocation counts and per-run
empty/unreachable outcomes are **UNKNOWN**. The 30/38 parent slots without a syslog start are also
UNKNOWN (power-off versus missed launch). No silence is treated as calm.

## Live probes and verification

- `mesh-reflex-health --check` at `19:47Z`: 36 per-run reflex artifacts fresh; `lan-newdevice` is
  explicitly **BLIND** because its real beat is frozen while its blind marker is fresh.
- `mesh-lan-newdevice --status` at `19:47Z`: `router DHCP + LAN ARP both unreachable — can't assess
  (not an alarm)` (exit 0, UNKNOWN result).
- `mesh-lan-newdevice --test`: passed 67 offline-fixture assertions; it did not produce a live LAN
  read.
- `mesh-perimeter --edge` remains wired at the 15-minute cadence and calls the LAN status axis.
- Full `mesh-sensorium` and `--compact` surveys: local thermal and audio hardware returned real
  readings; BLE returned no-adapter; Wi-Fi scan returned 0 APs. The LAN status probe independently
  found both DHCP and ARP unreachable.
- Fresh independent hardware artifact after reaffirming decay: `mesh-note3-battery --edge` read
  `present=true level=100/100 temperature=26.3°C power=USB status=5 voltage=4338mV`; the real-read
  state artifact `~/.mesh/.note3-battery-state` is 81 bytes, mtime `2026-09-13T19:51:25Z`.

No LAN read can be made fresh until router DHCP or LAN ARP becomes reachable. Recovery condition:
when either input is reachable, run `mesh-lan-newdevice --status` and require a non-empty,
newly-timestamped `.lan-newdevice.beat`; then rerun `mesh-reflex-health --check` and reassess decay.
