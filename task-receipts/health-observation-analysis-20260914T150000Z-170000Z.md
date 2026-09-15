# Health observation analysis: 2026-09-14 15:00–17:00Z

Task: `20260914T150000Z-170000Z/analyze-observation`
Source: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T150000Z-170000Z.md`
Interval: `[2026-09-14T15:00:00Z, 2026-09-14T17:00:00Z)`

## Admission and overlap

The complete admission report declares 411 unique events: 279 from `chat.log`, 60 from
`witness.log`, and 72 from `sensors.log`. I independently recounted the half-open interval in all
three tapes; each count matched and there were zero exact duplicate normalized rows per source. The
15:00–16:00 hour overlaps
[`health-observation-analysis-20260914T140000Z-160000Z.md`](health-observation-analysis-20260914T140000Z-160000Z.md);
new interpretation below focuses on 16:00–17:00Z.

## Findings

- **The witness view remained partial.** All 30 witness rows reported `nodes=4/11` and
  `reflex=OK`; sense coverage ranged from 4/21 to 7/21. Seven rows marked ask-resolution metrics
  `UNKNOWN`, with `ask_unknown=1`; when present, `ask_resolve=0.741` and `ask_stale_h` rose from
  176.2 to 177.2 hours. The reflex signal does not establish full fleet or sense coverage.
- **Local load samples were intermittent and room sensing stayed uncertain.** The 12 five-minute
  samples reported CPU `load1` median 14.93 (range 8.74–146.64), memory median 29.6% (24.2–48.0%),
  and room sense `UNCERTAIN` in all 12. The two CPU samples above 64 are isolated samples with no
  process attribution; they do not establish sustained resource pressure or occupancy.
- **Four above-floor device-churn bursts left 78 counter values unknown.** In 16:20, 16:30, 16:50,
  and 16:55Z, `device-churn.log` recorded deltas 18, 34, 20, and 22 (94 total). Exact interval
  joins against `udev-stream.log` found 16 observed rows: eight source-signed probes and eight
  unsigned `change/hwmon` rows, all for the same hwmon device path. The remaining 78 sequence
  values have no row in this namespace-scoped listener. A 16:15 TICK added six more absent values;
  the 16:35 TICK's four values were all observed (two signed, two unsigned). Across all nonzero
  intervals, 20/104 values were retained and 84 remain absent/unknown. These are global counter
  gaps, not evidence of dropped broadcasts or external enumeration.
- **The existing exact-join capability did not provide retrospective source attribution.** The
  bounded `docker events` query for 16:00–17:00Z returned no rows and `docker ps -a` showed no
  containers. The completed `device-churn-live-join-20260913/capture-veth-container-join` receipt
  documents `scripts/mesh-docker-veth-join` as a manual, bounded observer; its prior live capture
  was empty and it is not scheduled. The completed 14:25–14:55Z mesh-home join receipt already
  states the namespace-visibility limitation, but there was no active task for this new interval.
  I registered `health-device-churn-cross-namespace-join-20260914/investigate-cross-namespace-uevent-join`
  to Senses for a narrowly scoped read-only investigation; its exact-owner dispatch check exited 0
  and it is dispatched/open. I did not take or claim the Senses-owned row.

## Current live health after the interval

Compared with the 17:25Z `[check]`, the 17:38Z one-shot pane showed the doctor cache refreshed at
17:32Z with 0 FAIL / 33 WARN (the earlier full default run reported 0/34; the one-WARN difference
has no new WARN category identified here). LAN remains UNKNOWN. Fleet view reports 10 nodes, 3 SSH,
0 LAN, and 7 down; egress is currently OK. The pane still shows GPU VRAM critical at 93% and
Bluetooth sensors offline.

The live BLE failure persisted: `mesh-ble-heal --status` at 17:36Z reported `DAEMON-SICK`, 1098
wedges, and `last_outcome=cooldown`; `mesh-ble-heal --test` exited 1 because `bluetoothctl show`
had no parseable Powered flag. No power-cycle or service restart was attempted. The prior
90-minute cooldown ended at 17:21Z, so recovery is not established by the current test.

## Decision

Retain the 78 missing values in the four CHURN intervals as unknown; the new intervals justify one
Senses follow-up because the previous event-aligned source join was completed for a different time
range and no active task covered these bursts. Keep local CPU spikes unattributed, witness coverage
partial, LAN UNKNOWN, and Bluetooth DAEMON-SICK. No routing, DNS, firewall, VPN, container, device,
or service configuration changed.

## Verification

- Re-read the complete admission report and independently recounted 279/60/72 source rows with zero
  duplicates in `[15:00,17:00)`.
- Aggregated all 12 sensor triples and all 30 witness rows for 16:00–17:00Z.
- Joined every nonzero 16:00–17:00 `device-churn.log` interval to exact `udev-stream.log` seqnums;
  the missing ranges total 84 across all nonzero intervals, including 78 in four CHURN reports.
- Queried bounded Docker events for 16:00–17:00Z (no rows) and read `docker ps -a` (no containers).
- Checked the completed prior source-join task, prior mesh-home interval receipt, and Senses dispatch
  eligibility; the new exact-owner check exited 0. Did not claim the Senses-owned row.
- Re-ran `mesh-ble-heal --status` and `--test`, and consumed `mesh-dash --once check` twice; the
  latter was the required one-shot mode.
