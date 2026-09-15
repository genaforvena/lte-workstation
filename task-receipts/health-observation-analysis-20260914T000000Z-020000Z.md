# Health observation analysis: 2026-09-14 00:00–02:00Z

Task: `20260914T000000Z-020000Z/analyze-observation`  
Source report: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T000000Z-020000Z.md`

## Coverage

The admission report says `evidence_complete=yes`, 364 source rows, 364 unique events, no duplicates:
232 `chat.log`, 60 `witness.log`, 72 `sensors.log`. I independently filtered all three retained tapes
to `[2026-09-14T00:00:00Z, 2026-09-14T02:00:00Z)` and reproduced those counts.

## Bounded signal

The recurring signal is high, bursty local CPU load alongside partial fleet visibility. Across 24
five-minute sensor readings, `cpu_load1` had median 25.18 on a 16-core node; 14/24 samples exceeded
16, 6 exceeded 32, and 3 exceeded 64. Peaks were 151.61 at 00:53Z, 71.44 at 00:58Z, and 134.31 at
01:53Z. The two `:53` peaks are one-hour apart. Memory remained 19.3–33.6% (median 24.1%).
`room_sense` was PRESENT 17/24, OFFLINE 6/24, UNCERTAIN 1/24.

The witness tape still reported reflex `OK` in all 60 samples, but node visibility was only 3/11 in
55 samples and 4/11 in 5; live-mind counts were `UNKNOWN` in 9/60, and ask data in 15/60. In
particular, `minds_live=UNKNOWN` occurred at 00:50:57Z and 01:50:59Z, close to the two load peaks.
These point samples establish coincidence only. The `mesh-random-track-grind` cron is scheduled at
minutes 23 and 53, and the `mesh-usb --urb` reflex also fires at minute 53; the USB log at both peak
timestamps says there was no USB-attached network interface. Historical load samples do not name a
process, and the grind output has no per-run timestamps, so I do not attribute the spikes to either
job. A single short capture of the next scheduled `:53` run is warranted to test that candidate.

Other bounded events: chat contained 1 `[health-fail]` for the chronic `imac-rozalia` reachability
fault (triaged in `health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md`), one `[mind-holding]`
for `discover` (live pane now IDLE; original `/clear` delivery remains unknown, recorded in
`health-warning-d25975d004f5eb5fe637-triage-20260914.md`), and a transient `mesh-series-stats`
smoke-test failure in the 01:59 check stream. The later natural 03:23 doctor run returned to
2 FAIL/34 WARN, so that extra failure did not persist. The 00:31 doctor result was 2 FAIL/33 WARN.

## Follow-up and disposition

Registered `health-load-spike-20260914/observe-0353` to capture process/load samples around the next
minute-53 run. This tests the schedule coincidence without claiming a cause. No source or substrate
change is justified by these tapes. The known health findings remain partial fleet reachability and
unattributed high-load spikes; passing reflex status is not evidence of complete coverage.

Sources: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T000000Z-020000Z.md`,
`/home/mesh-home/.mesh/chat.log`, `/home/mesh-home/.mesh/witness.log`,
`/home/mesh-home/.mesh/sensors.log`, `/home/mesh-home/.mesh/reflexes.cron`,
`/home/mesh-home/.mesh/usb-urb.log`, and the later doctor result in
`task-receipts/health-doctor-next-slot-20260914-observation.md`.
