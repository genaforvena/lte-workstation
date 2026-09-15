# Health observation analysis: 2026-09-15 18:00–20:00Z

Task: `20260915T180000Z-200000Z/analyze-observation`  
Source: `observation-window:20260915T180000Z-200000Z`  
Interval: `[2026-09-15T18:00:00Z, 2026-09-15T20:00:00Z)`

## Admission

The generated report is complete: 840 unique events, with 703 rows from
`chat.log`, 60 from `witness.log`, and 77 from `sensors.log`; exact
deduplication removed zero events. The report states `evidence_complete=yes`.

## Findings

- The strongest bounded signal is partial device-event attribution. `device-churn`
  recorded mesh-home bursts at 18:50:03Z (`delta=6`, observed `0/6`, unknown/missing
  `6`) and 19:40:03Z (`delta=22`, observed `1/22`, unknown/missing `21`), followed
  by 19:45–19:55 bursts (`delta=21`, `24`, and `8`). Phaedra also reported churn at
  18:30:05Z and 19:05:03Z/19:35:03Z. These are elevated events, not named-device
  or external-enumeration verdicts; no device or substrate action is justified.
- Witness sampling was bounded rather than continuous: 56 samples were `reflex=OK`
  and 4 were `STALE` in the interval. This is a liveness lapse in sampled evidence,
  not proof of continuous fleet failure.
- The 24 `cpu_load1` samples ranged from 9.74 to 155.53 (median 27.57, mean 48.85);
  24 `mem_used_pct` samples ranged from 17.9% to 61.2% (median 47.7%, mean 43.63%).
  The live pane independently warned that high local load makes reachability probes
  unreliable. Peer non-answers therefore remain uncertain, not confirmed down.
- The interval contains recurring coordination and health traffic: independent
  pattern counts found 60 `[health-fail]` rows, 117 `[health-warning]` rows, and
  8 device-churn rows. Witness autonomy also reported reconciliation errors and
  mesh-land reported an overlap refusal. These are existing owner-routed lanes;
  this observation does not justify duplicate substrate or task changes.
- The live state showed egress currently OK (0% loss, 1.334 ms average) while the
  VPN status remained degraded/observe-only. Historical path-quality warnings were
  already triaged as recovered; no routing, DNS, firewall, VPN, device, service,
  or privilege mutation is warranted from this window.

## Disposition

Complete bounded analysis. Retain the known blind spots: high-load reachability
probes and incomplete uevent attribution cannot establish continuous peer or
device state. Existing owner-routed device-attribution, witness-autonomy, and
mesh-land work remains the appropriate follow-up; no duplicate task was created.

## Verification

- Read the complete generated report and checked admission totals `840/840/0` and
  source split `703/60/77`.
- Independently counted the bounded rows in `/home/mesh-home/.mesh/chat.log`,
  `witness.log`, and `sensors.log`; recomputed sensor extrema and medians.
- Independently inspected matching bounded chat rows for device-churn, health-fail,
  health-warning, and coordination signals.
- No routing, DNS, firewall, VPN, device, service, or privilege state changed.
