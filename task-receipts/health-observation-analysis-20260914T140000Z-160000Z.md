# Health observation analysis: 2026-09-14 14:00–16:00Z

Task: `20260914T140000Z-160000Z/analyze-observation`  
Source: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T140000Z-160000Z.md`  
Interval: `[2026-09-14T14:00:00Z, 2026-09-14T16:00:00Z)`

## Admission and recount

The complete report declares 517 unique rows: 385 from `chat.log`, 60 from `witness.log`, and 72
from `sensors.log`. I independently recounted those half-open timestamp ranges and found zero exact
duplicate lines in any source. The 14:00–15:00 overlap is covered by
`health-observation-analysis-20260914T130000Z-150000Z.md`; new interpretation below focuses on
15:00–16:00Z.

## Findings

- **Local load was mostly ordinary in the new hour.** The 12 five-minute samples show CPU load1
  median 10.8 (range 8.13–37.49), memory median 44.5% (27.1–51.2%), and room sense `UNCERTAIN`
  in all 12 samples. No sustained load or occupancy claim follows from these sparse readings.
  Across the full two-hour interval, three of 24 CPU samples exceeded 64 and one memory sample
  exceeded 64%; those isolated samples do not identify a process or establish sustained pressure.
- **Witness coverage remained partial.** All 60 rows report `nodes=4/11` and `reflex=OK`; senses
  coverage ranged from 4/21 to 7/21. The 15:00–16:00 samples show `ask_resolve=0.741` whenever
  present, while `ask_stale_h` rises to about 176 hours. Treat the fleet and sense gaps as unknown,
  not green; the stable reflex signal does not establish whole-fleet coverage.
- **The 15:05–15:10 mesh-home churn has the known namespace-visibility limit.** At 15:05 the
  global sequence counter advanced by six, with no matching rows in the bounded `udev-stream.log`.
  At 15:10 it advanced by 18; the listener retained seqnums 11717 and 11721–11725, all hwmon
  changes (three source-signed probes and three unsigned rows), leaving 12 sequence values absent
  from that listener. A bounded Docker events query for 15:04–15:11Z returned no rows. The exact
  source remains unknown: the completed `udev-stream-sgap-population-unresolved` investigation
  established that the counter is global while the netlink listener is namespace-scoped, so these
  gaps cannot be called dropped events, Docker activity, or external enumeration. The earlier
  same-day read-only join (`device-churn-attribution-20260914-correlate-14h-mesh-home-bursts.md`)
  already names the smallest missing evidence: a source-side event/lifecycle join across relevant
  namespaces. No duplicate retrospective join task is warranted. Churn was `QUIET` from 15:15
  through 15:50; the 15:55 delta of 3 was below the learned floor and correctly classified `TICK`.
- **Phaedra's 15:05 and 15:35 delta=6 postings remain unattributed.** The exact prior parity task
  covered earlier intervals and completed with missing sequence values left unknown. Phaedra is
  online as compute but currently off-mesh for minds; the 15:00–16:00 posts alone do not provide
  event identities or justify generic reassignment. Keep its exact-owner work visible and do not
  infer a physical device event from the global counter.
- **Explicit-owner task holds are not safe to substitute.** The board repeated “owner window
  ABSENT” for `fail2ban-repeat-offender-20260914/triage-repeat-offender`; the canonical task remains
  open under `phaedra`. Its owner is absent from the mind mesh, so preserve the hold and existing
  retry rather than assigning it to health or creating a duplicate.
- **The scheduled doctor cache missed a refresh.** The 15:29 board FYI records that the 15:23 cron
  was deferred under memory pressure; the one-shot pane at 16:23 still displayed the 13:32 cached
  doctor result. A later 16:23:01 doctor-log summary (outside this observation interval) recorded
  1 FAIL/33 WARN and only 6/164 serial confirmations assessed. This is a cache/freshness defect,
  not evidence that the older three-failure snapshot is current. The fresh egress-integrity section
  in the direct doctor run passed the LAN-prefix FIB exclusion and configured consumer route.

## Current live health check after the interval

The post-window `mesh-ble-heal --test` failed its live-read gate: `bluetoothctl show` returned
`No default controller available`. Read-only `mesh-ble-heal --status` reports
`DAEMON-SICK`, `wedges=1093`, and `last_outcome=cooldown`; its last-heal epoch is 2026-09-14T15:51:01Z,
so the configured 90-minute cooldown ends at 17:21:01Z. No adapter power-cycle or service restart
was attempted. Treat Bluetooth as currently unavailable; after the next eligible reflex cadence
past 17:21:01Z, inspect `mesh-ble-heal --status` and repeat `mesh-ble-heal --test` to verify recovery.

## Decision

No new attribution task or owner substitution is warranted from this window. Preserve the known
namespace-visibility blind, partial fleet coverage, Phaedra's exact-owner holds, and stale doctor
cache as named states. The post-window Bluetooth failure is a confirmed current limitation under
the healer's cooldown; the exact next check is after 17:21:01Z. No routing, DNS, firewall, VPN,
container, or hardware configuration was changed.

## Verification

- Recounted 385/60/72 timestamped rows in the half-open window; each source had zero exact duplicate
  lines.
- Aggregated all 24 sensor rows and all 60 witness rows; used the prior health receipt for the
  overlapping 14:00–15:00 hour.
- Joined the 15:05 and 15:10 device-churn ranges to exact seqnums in `udev-stream.log`; ran a
  bounded, read-only Docker events query (exit 0, no rows).
- Checked existing completed namespace-gap and 14:00–15:00 attribution receipts, exact owner task
  status for Phaedra/F2B, and live mind inventory.
- `mesh-ble-heal --test` reproduced the missing-controller failure; `bluetoothctl show` and
  `mesh-ble-heal --status` confirmed `DAEMON-SICK` with cooldown active.
