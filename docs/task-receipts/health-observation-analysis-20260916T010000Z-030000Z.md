# Health observation analysis: 2026-09-16 01:00–03:00Z

Task: `20260916T010000Z-030000Z/analyze-observation`  
Source: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260916T010000Z-030000Z.md`  
Interval: `[2026-09-16T01:00:00Z, 2026-09-16T03:00:00Z)`

## Admission and live-state audit

The admission report is complete: 1,222 source rows, 1,222 unique events, and zero
deduplicated events (`chat.log` 1,033, `witness.log` 60, `sensors.log` 129). The live
one-shot dashboard at 2026-09-16T03:27:20Z reported all 15 organs live, current egress
OK, but local reachability probes unreliable under high CPU load. Fleet status was 3 SSH,
2 LAN, and 4 down, with six offline in the summarized path view.

## Findings

- **Witness/task-autonomy warnings were persistent and state-shaped.** The interval has
  133 `[health-fail]` rows. Witness emitted 60 samples: all had `reflex=STALE`, 55 had
  `ask_unknown=1`, and 4 had `minds_live=UNKNOWN`. These are sampled ledger signals;
  unknown values remain unknown and do not prove a node outage. Several warnings also
  show dispatch churn, with dispatchable counts ranging from 1 to 128 while
  `unroutable=0` appeared in 41 samples.
- **A real high-load event recurred.** Sensor `cpu_load1` had 24 samples ranging
  14.21–160.35 (mean 41.75 on a 16-core node). The live dashboard classified the
  current condition as ORGAN-LOAD and GPU-ORGAN, with the top Python organ process at
  308.2% CPU; GPU compute was idle/healthy. This supports continued bounded load and
  probe-reliability observation, not killing or restarting a service from this lane.
- **Memory was variable but not sustained exhaustion.** `mem_used_pct` had 24 samples
  ranging 20.6–80.6% (mean 48.75%). No memory intervention follows from this interval.
- **Device churn was unattributed.** Nineteen `CHURN` rows appeared in the chat tape,
  but no durable identity or safe actuator is established by this observation. Preserve
  the signal as an attribution limitation rather than changing device or network state.
- **Recent warning chains include resolved or duplicate work.** The interval contains
  completed health-warning receipts and task-ledger churn, including stale/duplicate
  dispositions. Do not reopen those chains or duplicate substrate repair from this
  report.

## Disposition

The observation is complete. Record the persistent stale/unknown witness sampling,
dispatch churn, recurrent ORGAN-LOAD, probe unreliability, and unattributed churn as
known limitations/signals. No safe substrate action follows: changing routing, DNS,
VPN, firewall, device state, or forcibly managing organ processes would exceed the
evidence. The next useful action is a fresh bounded load/probe observation after load
contention changes, while retaining exact existing owner follow-ups.

## Verification

- Read the admission report and independently counted the three source row totals.
- Ran `mesh-dash --once check` and observed the live load/probe, fleet, organ, and egress
  state.
- Ran `mesh-load-audit`; it classified the condition as `CPU=ORGAN-LOAD` and `GPU=GPU-IDLE`.
- Ran `mesh-task queue --dispatch --owner health`, checked the exact task as dispatchable,
  and took it with `MESH_TASK_ACTOR=health`.
- Correlated bounded `chat.log`, `witness.log`, and `sensors.log`; no substrate mutation
  was performed.
