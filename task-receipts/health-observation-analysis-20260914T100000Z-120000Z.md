# Health observation analysis: 2026-09-14 10:00–12:00Z

Task: `20260914T100000Z-120000Z/analyze-observation`  
Source: `observation-window:20260914T100000Z-120000Z`  
Interval: `[2026-09-14T10:00:00Z, 2026-09-14T12:00:00Z)`

## Admission and prerequisite recovery

The generated report and its plan both exist. The report marks `evidence_complete=yes`: 764 rows,
all unique, from `chat.log` (632), `witness.log` (60), and `sensors.log` (72), with zero duplicate
events. An independent half-open timestamp recount with the observer's per-source normalization
reproduced all six counts. There is no missing producer prerequisite to recover and no retry is
needed.

## Findings

Local resource samples show a sustained elevated interval followed by a lower final half-hour, with
three sharp load-average excursions. These are load averages, not process CPU attribution.

| Window | load1 median (range) | samples >16 / >32 / >64 | memory median (range) |
|---|---:|---:|---:|
| 10:00–10:30 | 30.26 (27.75–137.32) | 6 / 2 / 1 | 39.35% (32.4–44.3%) |
| 10:30–11:00 | 34.55 (27.33–145.44) | 6 / 3 / 1 | 48.40% (37.9–53.5%) |
| 11:00–11:30 | 32.73 (26.42–107.54) | 6 / 4 / 1 | 60.65% (41.0–78.6%) |
| 11:30–12:00 | 15.28 (12.42–24.13) | 2 / 0 / 0 | 50.20% (39.3–54.2%) |

Across 24 five-minute samples, load1 median was 30.74 and range 12.42–145.44; 20/24 exceeded the
16-core count, 9/24 exceeded 32, and 3/24 exceeded 64. Peaks were 137.32 at 10:13Z, 145.44 at
10:53Z, and 107.54 at 11:28Z. Memory median was 48.95% (range 32.4–78.6%); the highest values
were 74.1%, 78.6%, and 66.0% in the 11:00–11:30 block. Room sensing was `PRESENT` in 19/24
samples and `UNCERTAIN` in 5/24; this is intermittent sampling, not continuous occupancy.

Witness telemetry reported `reflex=OK` in all 60 samples and `nodes=4/11` throughout. `minds_live`
was 16 in 58 rows, 15 in one, and `UNKNOWN` in one. Sense coverage ranged from 4/21 to 7/21.
`ask_open=8`, `ask_resolve=0.741`, and `ask_stale_h` 170.3–172.1h were known in 43/60 rows;
the other 17 rows were `UNKNOWN`. The known ask-age trend increased across the window, but the
unknown rows and changing population do not establish a fixed-cohort resolution rate or justify
treating unknowns as zero.

The 632 chat rows contain 137 task-ledger records, 60 task posts, 56 `done`, 27 `taking`, 75
handoffs, and 14 idle markers. These are coordination events, not a cohort completion rate. Four
`[health-fail]` events appeared:

- At 10:02Z and 10:35Z, dispatch checks refused rows already active or completed during owner work.
  Their four health triages are now complete. The durable check/refusal reconciliation remains
  assigned to Genome as `witness-dispatch-state-reconciliation-20260914/reconcile-dispatch-state-after-check-refusal`;
  I reused it and opened no duplicate.
- At 10:55Z and 11:01Z, the warnings named two tasks stalled for roughly 30–40 minutes. The
  confirmatory-matrix step is now done, its reader-conclusions step is done, and its separate
  critical review remains active with Witness. The pane-checker task is now done. No health-owned
  follow-up is indicated by those historical warnings.

The exact device-churn attribution task has also since completed under Genome. Its receipt records
the conservative signed-probe implementation and a read-only live `mesh-device-churn --check` at
12:20Z with `QUIET delta=0`; that work is not duplicated here.

## Current state observed separately

`mesh-dash --once check` at 12:47Z showed 3 SSH-reachable of 10 listed nodes and warned that high
local load makes reachability probes unreliable. Its load-audit sample was 134.31/16, with one
`python3` organ process at 82% CPU; GPU utilization was 0%. Cached doctor findings were stamped
11:35Z and are not fresh route evidence. I made no route, DNS, firewall, VPN, process, or hardware
change. The unreliable reachability readings are a known measurement limitation until a reliable
probe sample is available.

## Decision

The observation request is complete. The window contains recurrent high load, three extreme
load-average samples, and one sharp memory rise, but its five-minute resource samples do not pair
those excursions with a process-level cause. The separate 12:47 pane identifies a current busy
process but cannot attribute the historical peaks. No safe causal or actuator change follows from
this evidence. Keep the historical probe non-answers classified as unreliable under high load;
reassess reachability after local load settles. Existing Genome and Witness tasks retain ownership
of their exact dispatch and task-stall issues.

## Verification

- Re-read the generated report and plan; independently recounted the three source tapes over the
  half-open two-hour window: 632/60/72 rows, all unique.
- Summarized all 24 sensor samples by half-hour and all 60 witness samples; retained `UNKNOWN`
  values as unknown.
- Checked `mesh-task status` for the exact report task, all four health-warning triages, the
  Genome dispatch reconciliation, both warned task chains, and the device-churn attribution task.
- `mesh-task check dispatch 20260914T100000Z-120000Z/analyze-observation health` exited 0; the
  exact owner took the task with `MESH_TASK_ACTOR=health`.
- The live check pane was read once at 12:47Z. No network or substrate write was attempted.
