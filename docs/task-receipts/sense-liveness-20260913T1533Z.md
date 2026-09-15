# Sense liveness audit — `lan-newdevice` — 2026-09-13T15:33Z

## Disposition

`lan-newdevice` remains **DECAYED on mesh-home**. `scripts/mesh-lan-newdevice` already carries a
`DECAYED 2026-09-13` annotation. I re-probed its real LAN inputs and found router DHCP and LAN ARP
both unreachable. Its scheduled perimeter caller remains in place to reveal recovery; the old value
is not read as current.

## Bounded evidence windows (UTC)

Windows end at 2026-09-13T15:33:00Z. Cron launches came from timestamped CRON rows in retained
`/var/log/syslog*`; the caller cadence is `9-59/15 * * * *`.

| Evidence | 24h: Sep 12 15:33–Sep 13 15:33 | 7d: Sep 6 15:33–Sep 13 15:33 |
|---|---:|---:|
| Nominal perimeter cron slots | 96 | 672 |
| Recorded `mesh-perimeter --edge` starts | 66 | 634 |
| Slots without a recorded start | 30 | 38 |
| Fresh real LAN beat | 0 | 0 |
| Fresh beats / recorded parent starts (upper bound) | 0/66 | 0/634 |
| Timestamped perimeter transition rows | 0 | 16 |
| Rows with `N=UNREACHABLE` | 0 | 16 |

The last real beat, `~/.mesh/.lan-newdevice.beat`, is zero bytes and dated 2026-09-02T20:24:22Z,
outside both windows. The blind marker was touched at 15:33:13Z; it records that an attempt could
not see the organ, not a LAN observation. `perimeter.log` is transition-only, so its 16 unreachable
rows in seven days do not count all unreachable attempts; no transition in the last 24 hours does
not mean the input recovered. The parent launch count is only an upper bound on completed child
reads. Exact child attempts and per-run empty/unreachable results are not retained. Missed cron
slots are UNKNOWN, not calm. Accordingly, 0/66 and 0/634 are upper-bound coverage ratios; exact
child-level coverage is UNKNOWN. Against nominal slots, fresh-read coverage is 0/96 and 0/672.

## Live probes and verification

- `mesh-reflex-health --check`: 36/36 per-run reflex artifacts fresh; `lan-newdevice` is explicitly
  **BLIND** because its last real beat is frozen and its blind marker is fresh. The reflex is running;
  its published LAN value is not live.
- `mesh-lan-newdevice --status` at 15:33Z: `router DHCP + LAN ARP both unreachable — can't assess
  (not an alarm)` (exit 0, UNKNOWN result).
- `mesh-lan-newdevice --test`: passed 67 fixture assertions. This gate does not make a live LAN read.
- `mesh-perimeter --edge` remains cron-wired at the 15-minute cadence and calls the LAN status axis.
- Supporting organ survey, `mesh-sensorium --compact` at 15:33Z: real local thermal read (max
  78°C) and audio-device enumeration; presence and Wi-Fi scan unavailable; router offline. This is
  not evidence of LAN health.
- Fresh real artifact after reaffirming decay: `mesh-note3-battery --edge` read the connected Note 3
  at 15:38:45Z (`present=true level=100/100 temperature=28.2°C power=USB status=5 voltage=4337mV`)
  and refreshed `~/.mesh/.note3-battery-state` (81 bytes).
- Secondary blind input: `mesh-wifi-link --test` and two bounded `--edge` probes returned exit 2;
  SSH to the phone did not connect. `.wifi-link.state` remains frozen at 2026-09-03T09:47:02Z while
  `.wifi-link-offline` refreshed at 15:37:33Z. No per-run quality/empty denominator is recorded.

No code or scheduler change was needed: this axis already has an honest decay label and a revival
probe. No commit was made. Recovery condition: router DHCP or LAN ARP becomes reachable and a new
real `.lan-newdevice.beat` is written; then re-run `mesh-reflex-health --check` and reassess decay.
