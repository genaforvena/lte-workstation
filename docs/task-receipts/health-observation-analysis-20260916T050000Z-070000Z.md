# Health observation analysis: 2026-09-16 05:00–07:00Z

Task: `20260916T050000Z-070000Z/analyze-observation`  
Source: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260916T050000Z-070000Z.md`  
Interval: `[2026-09-16T05:00:00Z, 2026-09-16T07:00:00Z)`

## Admission and evidence

The canonical admission report is complete: 1,387 source rows and 1,387 unique
events, with zero deduplicated events (chat.log 1,183; witness.log 60;
sensors.log 144). The report was read directly. Independent bounded sensor
aggregation found 24 CPU-load samples ranging from 21.64 to 162.29 (mean
71.99), and 24 memory samples ranging from 26.1% to 72.1%. `room_sense` was
`PRESENT` 22 times and `UNCERTAIN` twice. All 60 bounded witness samples had
`reflex=STALE`; the node census varied from 3/10 to 5/10 (mean 3.98).

## Findings and disposition

- **High local load reduces probe confidence, but is not safely attributable to
  one victim.** A fresh `mesh-dash --once check` reported load 42.98/16 and
  `PROBE-WARNING: LOCAL LOAD HIGH`. A fresh process snapshot showed concurrent
  mesh-task queue workers and audio-analysis Python jobs consuming CPU. This is
  an attribution/coordination limitation, not evidence for killing a process or
  changing routing; no corrective task is created.
- **Fleet visibility is stale/partial.** The bounded witness tape consistently
  reports `reflex=STALE` and 3–5/10 nodes. Current `mesh-health` reports the
  local node and Phaedra reachable, two LAN devices reachable, and five peers
  offline. Preserve `UNKNOWN` for non-answers; no node repair follows from this
  bounded evidence. Existing health/witness task-flow work covers the relevant
  ledger and probe limitations.
- **Room sensing has two transient `UNCERTAIN` samples.** The surrounding
  samples are `PRESENT`; this does not establish an occupancy transition or a
  safe actuator.
- **The cached failed CUPS alarm is stale/nonexistent rather than an actionable
  mesh service failure.** `systemctl is-active` returned `failed` for
  `snap.cups.cupsd.service`, and `systemctl --failed` identified it as
  `not-found`; `mesh-roz-channel.path` and `mesh-operator-intake.path` were
  inactive. No service mutation is authorized by this observation alone.

## Verification

- Read the complete canonical report and matched admission totals 1,387/1,387/0.
- Independently inspected bounded `sensors.log`, `witness.log`, and relevant
  `chat.log` rows; computed the ranges above with `awk`.
- Reran `mesh-dash --once check`, `mesh-health`, `mesh-card --refresh`, and
  read-only systemd/process checks. `mesh-card` retained invariant-check `OK`
  and clean default egress; current egress was healthy.
- Confirmed `mesh-task check dispatch 20260916T050000Z-070000Z/analyze-observation health`
  exited 0 and the owner-authored take is active.
- Delegation decision: this single exact-owner analysis is tightly coupled to
  one bounded report and its ledger settlement, so it used the local exemption;
  no subagent report was used.
- No substrate or process mutation was taken. Retry on a fresh observation after
  contention/probe conditions change, or when an exact owner and safe corrective
  actuator are evidenced.
