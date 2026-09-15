# Health observation analysis: 2026-09-14 06:00–08:00Z

Task: `20260914T060000Z-080000Z/analyze-observation`  
Source: `observation-window:20260914T060000Z-080000Z`  
Interval: `[2026-09-14T06:00:00Z, 2026-09-14T08:00:00Z)`

## Coverage and findings

The admission report declares complete coverage: 410 unique rows from `chat.log` (278),
`witness.log` (60), and `sensors.log` (72), with no duplicates. I independently recounted the
timestamp-bounded rows and compared the leading hour against the previous 05:00–07:00 health
receipt, so overlap is not treated as new evidence.

- **The witness dispatch/check warning recurred and matches an existing Genome task.** The
  06:21:13Z autonomy failure reported `active=0` and rc=2 for the 04:00–06:00 analysis task; its
  `[taking]` line and canonical ledger transition to active were already recorded at 06:20:50Z and
  06:20:54Z. The next warning at 07:15:55Z returned rc=2 for the 06:11 health-warning triage,
  which had completed at 06:16Z. The respective health triages report a successful next autonomy
  run, but do not establish the exact timing cause. Both observations are covered by the open
  Genome task `witness-dispatch-state-reconciliation-20260914/reconcile-dispatch-state-after-check-refusal`,
  which explicitly asks to reproduce the 06:21 and 07:15 cases alongside the 2026-09-13 race.
  I reused that task and opened no duplicate.
- **Device-churn counters repeatedly report uevents while retained source rows remain partial.**
  Across 24 five-minute mesh-home readings there were 12 `CHURN`, 10 `QUIET`, and 2 `TICK` rows;
  reported deltas ranged from 2 to 24 in CHURN rows. The bounded `udev-stream.log` contains only
  28 events in this interval, all `hwmon`; 14 carry the known synthetic signature and 14 are
  unmarked. This stream does not account for every counter delta, so the unobserved events remain
  unknown and are not classified as external hardware changes. The exact issue is already assigned
  to Genome as `device-churn-signed-probe-attribution-20260914/separate-signed-probe-events-from-device-churn`;
  this interval supplies more evidence for that scope, not a reason to create a second task. Three
  separate phaedra board events also reported six-event churn windows; no remote source stream was
  available here to attribute those counts.
- **Room-camera sensing was intermittent.** The room-sense loss reflex reported recovery at
  06:47:01Z and loss at 06:57:03Z. The 24 five-minute sensor rows contain 11 `PRESENT` and 13
  `UNCERTAIN` samples. I treat this as intermittent sampling, not continuous room state, and did
  not trigger camera or service actions.
- **Witness telemetry retained regular UNKNOWN gaps.** All 60 rows report `reflex=OK` and `nodes=3/11`.
  `minds_live` is UNKNOWN in 8 rows (one known row is 14, the others are 15); ask fields are UNKNOWN
  in 14 rows. Among known samples, `ask_p90_h` ranges from 165.3h to 167.3h and `ask_resolve` stays
  0.746. This supports a bounded sampled trend only.
- **Local resource samples show spikes, not sustained saturation.** The 24 sensor rows report
  `cpu_load1` from 8.7 to 82.89 (median 19.095) and memory use from 22.4% to 62.0% (median 37.6%).
  The current refreshed card at 08:20Z reports load 16.20/16, memory 37%, temperature 76C, and
  upstream OK; this is separate live state, not a conclusion inferred from the historical samples.

## Current state observed separately

`mesh-dash --once check` at 08:17Z showed the fleet degraded (2 SSH-reachable nodes, 8 down),
cached doctor findings of two egress FAILs, and high local load. The subsequent live
`mesh-card --refresh` at 08:20Z reports exit-node `phaedra`, `exit-node-lan: ok` (`100.74.0.1` via
`enp42s0`), upstream OK, and eight listed peers offline. The dashboard doctor's egress labels are
therefore not a fresh route diagnosis; the live card supports the LAN gateway path while public
egress still uses the configured Tailscale exit-node path. The exit-node SPOF remains a known
topology condition. No routing, DNS, firewall, VPN, or peer state was changed; no safe substrate
action followed from this bounded analysis.

## Disposition

The evidence report is complete. The two recurring task-check errors and the source-attribution
ambiguity for device churn have exact open Genome tasks, so I reused them rather than duplicate
their work. Camera uncertainty and intermittent resource samples did not justify actuator or
substrate action. No new follow-up was warranted in this window.

## Verification

- Re-read `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T060000Z-080000Z.md`;
  independently recounted 278/60/72 bounded source rows.
- Re-read the preceding 05:00–07:00 analysis, the 06:21 and 07:15 health warning traces and
  receipts, both exact open Genome task chains, and the canonical task journal transitions.
- Aggregated all 60 witness rows, all 24 five-minute sensor sets, all 24 local device-churn
  readings, the interval's 28 retained udev rows, and room-sense transitions.
- `mesh-dash --once check` completed at 08:17Z; `mesh-card --refresh` completed at 08:20Z.
  No network or substrate write was attempted.
