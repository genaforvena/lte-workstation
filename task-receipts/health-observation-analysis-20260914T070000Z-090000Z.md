# Health observation analysis: 2026-09-14 07:00–09:00Z

The admission report at `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T070000Z-090000Z.md`
marks the half-open UTC window complete: 468 source rows, 468 unique events, zero duplicates.
Independent timestamp filtering of the three source tapes reproduced the same counts:
336 `chat.log`, 60 `witness.log`, and 72 `sensors.log` rows. The sensor tape contains 24
five-minute samples each for load1, memory, and room sense; witness has 60 approximately
two-minute samples.

## Measured state

| Window | load1 samples: median, range | samples >16 | memory median, range | room sense |
|---|---|---:|---|---|
| 07:00–07:30 | 6: 46.78, 17.02–82.89 | 6/6 | 29.4%, 22.4–45.2% | UNCERTAIN 6/6 |
| 07:30–08:00 | 6: 11.37, 8.70–26.93 | 2/6 | 40.9%, 32.8–48.5% | UNCERTAIN 6/6 |
| 08:00–08:30 | 6: 20.88, 10.70–34.66 | 4/6 | 27.5%, 21.5–48.2% | PRESENT 6/6 |
| 08:30–09:00 | 6: 23.66, 10.60–39.60 | 4/6 | 28.65%, 24.3–38.3% | PRESENT 5/6, UNCERTAIN 1/6 |

Across all 24 samples, load1 median was 19.505 and range 8.70–82.89; 16/24 exceeded the
16-core count, 7/24 exceeded 32, and one exceeded 64. The peak was 82.89 at 07:13Z; other
large samples were 52.42 at 07:28Z, 47.79 at 07:08Z, 45.77 at 07:03Z, and 39.60 at 08:48Z.
This is load-average evidence, not per-process CPU attribution. Memory ranged 21.5–48.5%
(median 31.3%) and declined in median from hour 07 (33.2%) to hour 08 (27.95%).

Witness reported `reflex=OK` in all 60 samples, while `nodes=3/11` in 55 samples and `4/11`
in five late samples. `minds_live` was unknown in 8/60; otherwise it ranged 14–16. `senses`
coverage remained between 4/21 and 7/21 (median 5/21), so the all-green reflex field did not
mean complete fleet or sense coverage. `ask_open` was unknown in 14/60 samples; the 46 known
values were 6 or 7, while known `ask_stale_h` values were already 167.2–169.2 hours. These
unknowns remain unknown; the report does not support filling them with zero.

## Events and interpretation

- Health's 07:01Z check reported the iMac last-seen age improving from about an hour to 39
  minutes while it remained offline by relay; LAN was UNKNOWN and route/DNS readings were
  unchanged. The comprehensive doctor run stopped after 4m31 under high load, leaving only
  its two known egress FAILs in the partial result.
- A `/clearclear` wake-input wedge was reported at 07:10:49Z and the pane returned to IDLE at
  07:21:56Z. Health closed its recovery triage at 07:25Z. The 07:15:55Z witness task-autonomy
  FAIL was a queue/check race: the health task had been claimed at 07:15:23Z, while the witness
  snapshot still counted `active=0`. The exact row later settled, and the live witness rerun
  passed at 07:31:26Z. See
  [`health-warning-6bcab66469917ab65056-triage-20260914.md`](health-warning-6bcab66469917ab65056-triage-20260914.md).
- Swap recovery reclaimed 7,503 MB at 07:18Z. The 07:00Z device-churn notice reported six
  uevents with no candidates; it is a separate device-churn-owned signal, not evidence that
  hardware caused the load samples.
- The iMac emitted `[health-ok]` at 08:03Z, `[health-fail]` at 08:33Z, and `[health-ok]` again
  at 08:54Z. This is observed intermittent reachability, not a stable recovery or a known cause.

Chat contained 158 rows in hour 07 and 178 in hour 08. Across the window there were 54
task-ledger rows, 52 handoffs, 22 task posts, 11 `taking` markers, 11 `done` markers, and 11
idle markers. Those are coordination-event counts, not a task completion rate: they do not
follow one fixed cohort from dispatch through outcome. The high-volume handoff/ledger traffic
is consistent with the prior two observation analyses and is already in scope for the
ordered `tg-self-review-timeseries-20260914` chain; no duplicate routing task is opened here.

The current wake frame at 09:18Z is outside this observation window: it still flags unreliable
reachability under high load, shows load1 `19.09/16c`, and reports GPU VRAM `11522/12288M`
(93%, utilization 0%). This confirms a current capacity warning, but cannot identify which
process caused the earlier load1 peaks.

## Decision

Retain a negative result for new interventions or causal follow-up from this window. The source
evidence is complete, but it contains no process samples concurrent with the 07:03–07:13 or
07:28 load peaks, so assigning them to a workload would overstate the evidence. The completed
`health-load-spike-20260914/observe-0353` task already found that one scheduled measurement
worker can overlap high load while explicitly leaving historical peaks unattributed; this
window adds another unattributed interval, not a causal discriminator. No scheduler, process,
GPU, route, or other substrate change is justified by these tapes. The separate iMac triage
`health-warning/29cc9b04bf711f7d05f9/triage` remains typed-blocked on a reliable current SSH
path; this analysis neither clears nor duplicates it.

Verification: report admission counts; independent half-open timestamp filter on
`/home/mesh-home/.mesh/{chat.log,witness.log,sensors.log}`; hourly/half-hour sensor and witness
summaries; prior load-spike and doctor observer artifacts; health task receipts and ledger
states. No hardware or substrate probe was added for this retrospective analysis.
