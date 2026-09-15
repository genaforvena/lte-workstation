# Health observation analysis: 2026-09-15 11:00–13:00Z

Task: `20260915T110000Z-130000Z/analyze-observation`  
Source: `observation-window:20260915T110000Z-130000Z`  
Interval: `[2026-09-15T11:00:00Z, 2026-09-15T13:00:00Z)`

## Admission and live-task audit

The generated admission report is present and internally complete: 431 unique events,
with 300 rows from `chat.log`, 59 from `witness.log`, and 72 from `sensors.log`; exact
deduplication count is zero. The canonical task chain was re-read after dispatch and is
still `active`, owner `health`, with lease through 2026-09-15T16:34:29Z. `mesh-task check
pending 20260915T110000Z-130000Z/analyze-observation health` returned rc=2 because the
step is already claimed, which is the expected refusal for a second claim. The task and
its report are therefore live and correctly specified; no rejection or duplicate task
was warranted.

## Findings

- **Task-autonomy warnings were persistent but mostly state-management signals.** The
  interval contains 60 `[health-fail]` rows, 53 task-ledger rows, and repeated errors
  naming an `analyze-observation` step with changing elapsed seconds. These are not
  evidence of a new node outage by themselves: the same interval also contains regular
  ledger recovery/dispatch activity, and the current target chain is live and correctly
  owned. Existing warning chains should retain their own triage; this analysis does not
  create a duplicate.
- **The node had real peripheral/service incidents.** At 11:00 the user
  `mesh-phaedra-proxy.service` was restart-churning (+4 restarts in about five minutes,
  measured period about 74.75 s versus its 15 s floor). At 11:05 an OOM watcher recorded
  a Python process killed in the heavy-run cgroup, and USB disconnects were recorded at
  11:40 and 12:25. These are concrete peripheral/service faults, not inferred from
  reachability probes.
- **VPN and egress recovered during the window.** At 11:40 the phaedra VPN reported no
  WireGuard client handshake for over 24 hours, while SS/trojan/WG were up and all
  provisioned clients were stale or never seen. At 11:44 watchdog recorded mesh-home
  recovered and egress recorded restoration on its route leg. No VPN, routing, DNS, or
  firewall write is justified by this bounded evidence.
- **Peer path evidence is intermittent, not continuous failure.** `path-watch.log`
  records imac-rozalia offline at 11:49, direct at 12:04, and netweather UDP=false at
  11:44 and 12:49. The existing exact path-flap investigation is complete; these sparse
  transitions do not establish a new cause or authorize substrate action.
- **Device churn includes reboot boundaries and partial attribution.** The accumulator
  rendered `REBOOT`/`delta=na` at 11:30 and 11:45, correctly refusing to interpret a
  counter reset as calm. Post-reboot activity included CHURN 33 and 28 at 11:35/11:40,
  CHURN 19 and 24 at 12:25/12:30, and TICK intervals with missing events. The source
  stream was complete for some intervals but partial for others (for example 18 of 24
  events missing at 12:30); seqnums identify no device. The exact device-churn
  attribution and mesh-home correlation chains are already complete, so no duplicate
  follow-up was opened.
- **Historical sensor samples show spikes, not sustained exhaustion.** There are 24
  samples each for room, CPU load, and memory. Room was `PRESENT` in all 24. CPU load1
  ranged 5.38–144.90 (median 11.37); memory ranged 18.9–69.9% (median 37.7%). These
  samples do not support a sustained memory or load incident, although the separate
  live pane at 16:03Z independently warned that current reachability probes were
  unreliable under high load.
- **Witness telemetry has explicit gaps.** Of 59 witness rows, 56 were `reflex=OK`, 3
  `reflex=STALE`, 2 had `minds_live=UNKNOWN`, and 11 had `ask_unknown=1`. This is a
  bounded sampled signal, not continuous fleet state; unknowns remain unknown.

## Disposition

The report is complete and the task instruction is correct. Findings are recorded as
evidence, with existing exact follow-ups reused rather than duplicated. No safe
substrate action followed: changing routing, VPN, DNS, firewall, peer state, or hardware
service state would exceed what this bounded observation proves. The remaining known
blindness is reachability under high local load plus incomplete attribution across reboot
and retained uevent windows.

## Verification

- Read the admission report and independently counted `chat.log`/`witness.log`/`sensors.log`
  rows as 300/59/72; admission says 431 unique and zero duplicates.
- Re-read the canonical task with `mesh-task status 20260915T110000Z-130000Z`; it was
  active and owned by `health`. The second-claim guard returned rc=2.
- Correlated bounded `witness.log`, `sensors.log`, `device-churn.log`, `path-watch.log`,
  and matching chat events; no source or substrate mutation was performed.
- Checked exact existing chains: device-churn attribution, mesh-home churn correlation,
  and iMac path-flap investigation are complete with receipts.
