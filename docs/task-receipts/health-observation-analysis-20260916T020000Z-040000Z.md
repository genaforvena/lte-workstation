# Health observation analysis: 2026-09-16 02:00–04:00Z

Task: `20260916T020000Z-040000Z/analyze-observation`  
Source: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260916T020000Z-040000Z.md`  
Interval: `[2026-09-16T02:00:00Z, 2026-09-16T04:00:00Z)`

## Admission and live-state audit

The admission report is complete: 1,311 source rows, 1,311 unique events, and zero
deduplicated events (`chat.log` 1,107, `witness.log` 60, `sensors.log` 144).
The live `mesh-dash --once check` at 2026-09-16T04:33:40Z reported all 13 organs live,
egress OK, but local load high enough to make reachability probes unreliable; GPU was
idle and healthy at 6,295/12,288 MiB VRAM (51%).

## Findings

- **Witness/task-autonomy churn remained persistent but sampled.** The interval contains
  122 `[health-fail]` rows. Witness emitted 60 samples: all had `reflex=STALE`, 57 had
  `ask_unknown=1`, and 3 had `minds_live=UNKNOWN`. The samples also show dispatch counts
  changing materially, including one `unroutable=1` observation. These are ledger-observer
  limitations and task-flow churn, not evidence of a node outage by themselves.
- **CPU load recurred and explains probe uncertainty.** The 24 `cpu_load1` samples ranged
  from 16.57 to 160.35 on a 16-core node (mean 42.70). The live pane classified the node
  as `CPU=ORGAN-LOAD`, with a busy Python process, while GPU compute remained idle. Keep
  this as a bounded load/probe-reliability signal; no service kill or substrate change is
  justified by this report.
- **Memory was variable, not exhausted.** The 24 `mem_used_pct` samples ranged from
  33.60% to 80.60% (mean 52.35%). No memory intervention follows.
- **Device churn was not safely attributable.** Five chat rows contained `CHURN`, but no
  durable identity or safe actuator was established in this window. Preserve the signal
  as an attribution limitation rather than changing device or network state.
- **Note3 presence was healthy during the interval.** Thirteen `note3-battery` rows were
  present; the live USB read also showed device `4d00553d61ab90b7`. This does not repair
  unrelated stale senses, but it rules out Note3 absence as the cause of this window's
  task-flow warnings.
- **Autoland overlap was a local coordination warning.** Two health-fail rows identify an
  autoland overlap. That is a coordination/ownership condition; do not launch a second
  landing or alter substrate from this observation task.

## Disposition

The observation is complete. Record persistent stale/unknown witness sampling, dispatch
churn, recurrent high CPU load and probe unreliability, and unattributed device churn as
known signals. No safe substrate action follows: changing routing, DNS, VPN, firewall,
device state, or forcibly managing organ processes would exceed the evidence. The next
useful action is a fresh bounded observation after load contention changes, with exact
owner/task reconciliation retained.

## Verification

- Read the complete admission report and verified its source-row totals.
- Ran `mesh-dash --once check` (rc 0) and `mesh-wake-expect health
  'warning|health-warning|task-ledger|note3-battery|mesh-card|ollama|handoff'`.
- Independently counted the bounded source tapes with `awk`/`rg`: 1,107 chat, 60 witness,
  and 144 sensor rows; 24 CPU and 24 memory samples; 122 health-fail, 5 churn, and 13
  Note3 battery rows.
- Ran `mesh-task queue --dispatch --owner health`, checked the exact candidate with
  `mesh-task check dispatch ... health` (rc 0), and claimed it with
  `MESH_TASK_ACTOR=health mesh-task take ...`.
- Delegated one non-overlapping read-only audit to subagent `Anscombe`; no file mutation,
  board voice, substrate write, or landing was delegated. The subagent returned no artifact
  and reported a conflicting `mesh-dash` timeout; that report was not used as evidence.
  I personally inspected the canonical source report and task-chain state, and retained my
  successful `mesh-dash --once check` output as the live-state evidence. The pane read,
  ledger claim, source counting, artifact write, and final verification remained local
  because they are tightly coupled ownership and evidence operations.
