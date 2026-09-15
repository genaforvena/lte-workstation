# Health self-state time series — 2026-09-14

Task: `tg-self-review-timeseries-20260914/self-state-timeseries-health`  
Observation interval: 2026-09-13 10:21:30Z through 2026-09-14 10:21:30Z (half-open).  
Scope: Health-owned task-ledger transitions and retained, timestamped Health reports, plus the
live `mesh-dash --once check` frame at 2026-09-14 10:21Z. This measures activity and observed
state, not labor hours.

## Measured task activity

Canonical `mesh-task replay --json` contained 338 Health-owned steps overall. In the interval,
89 steps were queued and 97 reached `done`. These are transition counts, not a fixed cohort:
some completed steps were queued before the interval, while some steps queued inside it remain
open or blocked. Completions do not imply 97 distinct successful fleet repairs.

| Six-hour UTC window | Health queue events | Health completions | What shifted |
|---|---:|---:|---|
| Sep 13 10:21–16:21 | 6 | 23 | Several earlier warning and room-recovery claims closed; the apparent completion excess includes work queued before this window. |
| Sep 13 16:21–22:21 | 30 | 28 | Warning and resolver activity rose; observation reviews began recurring every two hours. |
| Sep 13 22:21–Sep 14 04:21 | 23 | 24 | Observation reviews continued; doctor-run tracing and iMac reachability work appeared. |
| Sep 14 04:21–10:21 | 30 | 22 | Multiple resolvers remained blocked on a reliable path; a brief iMac recovery was followed by renewed probe uncertainty. |

Of the 97 completions, 53 were `health-warning/*` triages, 17 were `unblock/*` resolutions,
and 17 were two-hour observation analyses. The remaining ten were other scoped repair,
investigation, and reconciliation tasks. This concentration reflects Health's incident and
observation duties; counts alone do not establish avoidable routing or comparable effort.

## State over time

| Time (UTC) | Observed Health work or blocker state | Evidence |
|---|---|---|
| Sep 13 11:43 | iMac tailnet/SSH reachability was confirmed unreliable; physical state and cause remained unknown. | `mesh-task` replay: `health-warning/f3d16e4bf8dfa5116b63/triage` |
| Sep 13 13:06–14:38 | Probe identity mapping was corrected; a later receipt records the iMac room-eye restored via its Tailscale endpoint with a real frame and active watcher. | `docs/task-receipts/health-warning-347d70b4b3f9fd0e738e-triage-20260913.md`; `docs/task-receipts/unblock-health-d2d6ef7f613f5532-resolve-20260913.md` |
| Sep 13 17:56–Sep 14 02:21 | Two-hour reports repeatedly found uevent bursts without stable process attribution; the 18:00–20:00Z report did confirm Docker/veth overlap for one burst, and later windows did not consistently reproduce that discriminator. | `task-receipts/health-observation-analysis-20260913T180000Z-200000Z.md`; `task-receipts/health-observation-analysis-20260913T200000Z-220000Z.md`; `task-receipts/health-observation-analysis-20260914T000000Z-020000Z.md`; `task-receipts/health-observation-analysis-20260914T020000Z-040000Z.md` |
| Sep 14 03:36–04:21 | Natural doctor run completed in 9m08s with 2 FAIL / 34 WARN; the sampled process overlap did not establish ownership of historical load peaks. The iMac reachability fault was again recorded active. | `task-receipts/health-doctor-next-slot-20260914-observation.md`; `task-receipts/health-doctor-node-aware-stall-20260914-progress.md`; `task-receipts/health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md` |
| Sep 14 04:45–04:59 | Three resolver attempts for parent `health-warning/8dc5571ba68f5efaacc4/triage` retained a blocked result: no verified iMac or alternate LAN path. The middle attempt reused the first receipt; replay and journal provide its timestamp and task identity. | `task-receipts/unblock-health-a4e98e93cbf0b327-resolve-20260914.md`; `task-receipts/unblock-health-f64d9703ac99cec6-resolve-20260914.md`; `/home/mesh-home/.mesh/tasks.journal` |
| Sep 14 06:42 | A live CGNAT route repair verification completed with source/deployed parity; this is a scoped route result, not proof that the current fleet egress warning cleared. | `exit-node-lan-cgnat-live-repair-20260914.md` |
| Sep 14 08:51–09:17 | The iMac parent was blocked again at 08:51. A resolver then verified Tailscale ping and read-only SSH at 09:01, and the parent triage closed at 09:02. By 09:17, high local load made reachability probes unreliable again, so the parent was re-blocked pending a reliable sample. | `task-receipts/unblock-health-82aa91e1927db604-resolve-20260914.md`; `task-receipts/unblock-health-807797d851d3d242-resolve-20260914.md`; `task-receipts/health-warning-2ca0e1c7ec6377531951-triage-20260914.md`; `task-receipts/unblock-health-d049a3d635775070-resolve-20260914.md` |
| Sep 14 10:18–10:21 | The Telegram wedge triage closed as transient after full input delivery and a TG reply; its autoland follow-through remains active. The current check pane still marks reachability probes unreliable under high local load. | `health-warning-b50955f6b4e8ff44c615-triage-20260914.md`; live `mesh-dash --once check` at 10:21:09Z |

The current pane reports 3 SSH-reachable nodes, 7 down, and `PROBE-WARNING: LOCAL LOAD HIGH`;
those reachability counts are explicitly uncertain. Its doctor cache is 46 minutes old and
still shows the `tailscale0` egress and exit-node SPOF findings. The separate current parent
`health-warning/29cc9b04bf711f7d05f9/triage` remains blocked pending a reliable SSH path; the
current self-review is the only active Health-owned task in replay. These states should not be
merged into one causal story: the iMac did recover briefly, while the next attempted window made
the probe itself unreliable again.

## Self-correction signal

Use one event-gated resolver per blocked parent. When the required external condition has not
changed, append a timestamped check to the existing parent receipt instead of opening another
resolver; create/re-run a resolver only after its recorded retry edge occurs (here: a check pane
without `PROBE-WARNING`, or a verified independent LAN/owner path). The three blocked attempts in
14 minutes at 04:45–04:59 and the later block → successful path → renewed probe warning sequence
show why time-only retries create work without improving evidence. Keep the six-hour bounded
self-review cadence from the predecessor design as a maximum interval, with an earlier review
only on a material task-state or probe-reliability transition. Do not edit routing or retry SSH
while this pane says its reachability probe is unreliable.

## Gaps and limits

- The observation interval is exact, but task queue and completion counts are event totals, not a
  matched arrival/completion cohort or time-to-resolution series. They do not measure effort.
- The mesh board contains free-form messages; only canonical task replay was used for aggregate
  task counts. A `[done]` post is not a separate task completion.
- The two-hour observation reports have differing windows and fields; `unknown`, missing, and
  stale values remain unknown. The 08:00–10:00Z report was still open at capture, so it is not
  counted as an analyzed report.
- The current pane's fleet reachability counts are untrusted under its explicit probe warning, and
  its doctor cache is stale. No fresh fleet repair or causal attribution is claimed here.

## Reproduction and sources

- `mesh-task replay --json` captured at 2026-09-14 10:22Z; SHA-256 of captured JSON:
  `6d7690f22381658fa401c39ac0f04e9d9094ef678a828b1fbe7ab00aad6760be`.
- `/home/mesh-home/.mesh/chat.log` (Health-authored task-ledger transitions and timestamped board
  events in the observation interval).
- `/home/mesh-home/.mesh/tasks.journal` (canonical task state).
- `task-receipts/discover-self-review-timeseries-20260914.md` (24-hour distribution and cadence
  predecessor).
- The 17 completed two-hour analysis artifacts (activity-count cohort):
  `docs/task-receipts/health-observation-analysis-20260913T150000Z-170000Z.md`,
  `docs/task-receipts/health-observation-analysis-20260913T160000Z-180000Z.md`,
  `docs/task-receipts/health-observation-analysis-20260913T170000Z-190000Z.md`,
  `task-receipts/health-observation-analysis-20260913T180000Z-200000Z.md`,
  `docs/task-receipts/health-observation-analysis-20260913T190000Z-210000Z.md`,
  `task-receipts/health-observation-analysis-20260913T200000Z-220000Z.md`,
  `task-receipts/health-observation-analysis-20260913T210000Z-230000Z.md`,
  `task-receipts/health-observation-analysis-20260913T220000Z-000000Z.md`,
  `task-receipts/health-observation-analysis-20260913T230000Z-010000Z.md`,
  `task-receipts/health-observation-analysis-20260914T000000Z-020000Z.md`,
  `task-receipts/health-observation-analysis-20260914T010000Z-030000Z.md`,
  `task-receipts/health-observation-analysis-20260914T020000Z-040000Z.md`,
  `docs/task-receipts/health-observation-analysis-20260914T030000Z-050000Z.md`,
  `docs/task-receipts/health-observation-analysis-20260914T040000Z-060000Z.md`,
  `docs/task-receipts/health-observation-analysis-20260914T050000Z-070000Z.md`,
  `docs/task-receipts/health-observation-analysis-20260914T060000Z-080000Z.md`, and
  `task-receipts/health-observation-analysis-20260914T070000Z-090000Z.md`.
- The individual task receipts named in the state timeline above.

Verification: `mesh-task replay --json` parsed successfully; owner-filtered counts and four
six-hour bins were calculated from `queued_at` and `finished`; live pane state was read with
`mesh-dash --once check`. No substrate probe or change was made.
