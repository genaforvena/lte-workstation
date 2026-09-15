# Health observation analysis: 2026-09-14 05:00–07:00Z

Task: `20260914T050000Z-070000Z/analyze-observation`  
Source: `observation-window:20260914T050000Z-070000Z`  
Interval: `[2026-09-14T05:00:00Z, 2026-09-14T07:00:00Z)`

## Coverage and findings

The admission report declares complete coverage: 374 unique rows (242 from `chat.log`,
60 from `witness.log`, 72 from `sensors.log`), with no duplicate events. I independently
bounded the source rows to this interval.

- **Witness dispatch checks disagree with the live task ledger.** At 06:20:54Z chat
  recorded `20260914T040000Z-060000Z/analyze-observation` as active. At 06:21:13Z the
  witness run reported `active=0` and a failed exact-owner check for that same task.
  The task remained active and was completed with its analysis receipt at 06:31Z. This
  matches the previously documented candidate/claim race shape, but the preexisting
  active state before the witness failure also leaves stale/inconsistent audit or queue
  views as a possible cause. A separate 07:15:55Z event, just outside this interval,
  repeated the signature while the preceding health task was already active. I registered
  `witness-dispatch-state-reconciliation-20260914` for Genome to reproduce both forms,
  reconcile refused checks against canonical task state, and add fixtures that preserve
  errors for unresolved contradictions.
- **Device-event attribution already has an exact owner task.** The interval contains
  mesh-home uevent bursts at 05:20 (70), 05:25 (84), and 05:30 (102); the latter two
  coincide with the signed self-probe evidence described in the prior 04:00–06:00 report.
  `device-churn-signed-probe-attribution-20260914` is already queued to Genome with exact
  complete-match and incomplete-stream acceptance cases. I did not duplicate it or infer
  that unsigned/unretained events are absent.
- **Room sensing changed state near the interval end.** The 24 five-minute sensor rows
  report PRESENT 23 times and UNCERTAIN at 06:58Z. The chat tape records the room sense
  recovering at 06:47Z and losing its camera input at 06:57Z; the final sample is therefore
  uncertain rather than evidence that the camera stayed live. No camera action was taken.
- **Witness samples are steady but retain coverage gaps.** All 60 rows say `reflex=OK`;
  `minds_live` is UNKNOWN in 10 and ask fields are UNKNOWN in 15. Among known samples,
  `ask_p90_h` rises from 164.4h to 166.3h while `ask_resolve` remains 0.746. This is a
  bounded sample trend, not a continuous-state claim.
- **The prior routing repair now passes its live gateway lookup.** The separate
  VPN-owned `exit-node-lan-cgnat-live-repair-20260914` and health verification completed
  during this interval. Fresh read-only FIB lookups now send `100.74.0.1` via the local
  gateway `100.76.0.1` on `enp42s0`, while the actual Tailscale peer `phaedra` remains on
  `tailscale0` table 52. Public `1.1.1.1` still uses the configured online exit node
  `phaedra`, consistent with the opt-in egress setup. The one-shot pane's two doctor FAILs
  were cached from 05:32Z, before that repair; the current gateway result does not support
  repeating the repaired LAN-route alarm. No substrate write was made.
- **Fleet reachability is degraded and probe confidence is limited.** The 07:29Z live
  check frame shows 2 SSH-reachable nodes, 0 LAN nodes, 8 down, and `LOCAL LOAD HIGH —
  reachability probe UNRELIABLE`. `mesh-health` separately passes mesh-home and phaedra
  but lists the other eight as offline. This leaves peer availability partly unresolved;
  the load warning prevents interpreting non-answers as clean proof of node failure.

## Disposition

The observation source is complete and the findings are either already owned or have a
new exact follow-up. The witness mismatch now has a Genome task; device-churn attribution
already has its own Genome task; room-camera loss is visible as uncertainty; and the
LAN gateway FIB check confirms the completed VPN repair. The remaining public-egress
over-Tailscale/exit-node warnings are observed but were not changed because they concern
the active substrate and this analysis found no evidence authorizing a routing change.
The 07:29 doctor section is cached, so its two FAIL labels are not a fresh post-repair
diagnosis.

## Verification

- Read `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T050000Z-070000Z.md`;
  independently bounded 242/60/72 source rows.
- Aggregated the 60 witness rows, 72 sensor rows, room transitions, and device-churn marks.
- Read the prior 04:00–06:00 analysis, the completed 06:21 warning triage, the active
  device-churn task, and the completed VPN repair/health verification receipts.
- `ip route get 100.74.0.1` — local gateway via `enp42s0`; `ip route get 100.94.116.17` —
  phaedra via `tailscale0 table 52`; `ip route get 1.1.1.1` — public egress via
  `tailscale0 table 52`.
- `mesh-health` — mesh-home and phaedra PASS; eight configured peers OFFLINE.
- `mesh-dash --once check` — complete live frame at 07:29Z; doctor cache timestamp 05:32Z.
- Corrected the health wake prediction to match normalized pane lines: only the check-frame
  header is retained as a matching shape; `mesh-pane-consume` strips the pane-live footer
  before predictions are matched.
