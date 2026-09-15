# Health observation analysis: 2026-09-14 12:00–14:00Z

Task: `20260914T120000Z-140000Z/analyze-observation`  
Source: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T120000Z-140000Z.md`  
Interval: `[2026-09-14T12:00:00Z, 2026-09-14T14:00:00Z)`

## Admission and recount

The request report declares complete coverage: 666 unique rows from `chat.log` (534),
`witness.log` (60), and `sensors.log` (72), with no duplicates. I independently recounted the
half-open timestamp interval in all three source tapes and matched those counts. The prior
11:00–13:00 health receipt covers the overlapping hour; I treated its findings as context rather
than new evidence.

## Findings

- **Local resource and room samples were intermittent.** The 24 five-minute sensor rows report
  `cpu_load1` median 16.71, range 10.31–139.03, with two samples over 64 at 12:08Z and 12:28Z.
  Memory use ranged from 24.7% to 59.2% (median 36.0%). Room sensing was `PRESENT` in 15/24 rows
  and `UNCERTAIN` in 9/24. The historical load samples do not identify a process, and the room
  samples do not establish continuous occupancy.
- **Device-churn attribution remains incomplete on mesh-home.** The 24 five-minute accumulator
  readings were 13 `QUIET`, 6 `TICK`, and 5 `CHURN` (delta 0–24). Across partial-attribution rows,
  34 of 151 raw events were observed in the detailed stream; 117 remained missing/unknown. The
  bounded `udev-stream.log` holds 48 events, all `hwmon`, split evenly between 24 source-signed
  synthetic events and 24 unsigned events. These rows do not account for all accumulator deltas;
  missing sequence events stay unknown and are not evidence of external device enumeration.
- **Phaedra's repeated delta=6 reports still need a source join.** Its 12:05Z, 12:35Z, 13:05Z,
  and 13:35Z board summaries repeated the same six-event count. The exact open Genome task
  `health-observation-device-churn-phaedra-parity-20260914/verify-phaedra-attribution-parity`
  covers the 11:05Z through 12:35Z samples and remains open. The two later samples are outside its
  listed interval; I did not mutate another owner's task or create a duplicate parity task. Their
  source remains unjoined pending the exact host/tape comparison.
- **The local path-watch tape shows oscillation, not a demonstrated UDP fault.** In this interval,
  `imac-rozalia` changed direct→relay six times and relay→direct six times; Phaedra changed each way
  once. Both sampled `netweather` rows reported `udp=true`. The exact
  `mesh-path-watch-hourly-relay-repeat-20260912` diagnosis and independent verification task is
  complete; these samples do not justify a network change or a duplicate task.
- **The 12:16Z task-autonomy failure recovered through its exact owners.** The exact Genome
  device-churn task completed at 12:22Z, and health's
  `health-warning/160b72e1bdaf0ee01486/triage` closed after a fresh witness PASS at 13:02Z. The
  warning is historical, not a current failure; no duplicate was opened.

## Current health and cache disposition

The first live pane at 14:46Z showed 10 nodes, 3 SSH-reachable, 7 down, and a doctor snapshot dated
13:32Z with 3 FAIL/33 WARN. A direct `mesh-doctor --quiet` completed at 14:50:15Z with exit 0,
0 FAIL/33 WARN; only 3/162 serial confirmations fit its 60-second coverage budget, so this is not a
claim that all smoke tests were freshly assessed. The configured exit-node dependency and mic
default warning were among its findings.

This direct run did not refresh the pane cache. A second `mesh-dash --once check` at 15:00Z still
showed the 13:32Z 3 FAIL/33 WARN doctor snapshot and warned that local load made reachability probes
unreliable. `doctor.log` still has its last complete summary at 13:23Z (3 FAIL/33 WARN); its
14:23Z appended entry says the scheduled doctor skipped because another automated run held
`.doctor.lock`. `.doctor-cron-state` remains `3`. The writer is wired in `~/.mesh/reflexes.cron` as
`23 * * * * mesh-doctor --cron >> ~/.mesh/doctor.log`; an interactive `--quiet` run reports to its
caller but is not that cron snapshot. The next scheduled refresh is 15:23Z. Keep the pane result
stale until that writer produces a dated completed run; do not infer recovery from the fresh
interactive summary.

No routing, DNS, firewall, VPN, peer, hardware, or service state was changed. The fresh interactive
doctor result is retained as a separate measurement, with its limited serial-confirm coverage.

## Verification

- Re-read the complete admission report and independently recounted 534/60/72 source rows.
- Aggregated all 24 sensor and local device-churn rows, all 60 witness rows, and the 48 bounded
  udev events; compared device/path findings with the overlapping prior receipt and exact task
  ledger states.
- `mesh-task check dispatch 20260914T120000Z-140000Z/analyze-observation health` exited 0; the
  owner-authored take was recorded by `MESH_TASK_ACTOR=health`.
- `mesh-task status health-observation-device-churn-phaedra-parity-20260914` remains open under
  Genome; `mesh-task status mesh-path-watch-hourly-relay-repeat-20260912` is complete.
- `mesh-doctor --quiet` exited 0 at 14:50:15Z (0 FAIL/33 WARN; 3/162 serial confirmations).
- `mesh-dash --once check` completed at 15:00Z but retained the 13:32Z cached doctor result;
  inspected the 14:23Z skipped log entry, `.doctor-cron-state`, and the scheduled log writer.
