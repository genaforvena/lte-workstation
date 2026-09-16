# Health observation analysis: 2026-09-15 22:00–2026-09-16 00:00Z

Task: `20260915T220000Z-000000Z/analyze-observation`  
Source: `observation-window:20260915T220000Z-000000Z`  
Interval: `[2026-09-15T22:00:00Z, 2026-09-16T00:00:00Z)`

## Admission and live-state audit

The generated admission report is complete: 820 source rows, 820 unique events, and zero
deduplicated events (`chat.log` 688, `witness.log` 60, `sensors.log` 72). The live one-shot
dashboard at 2026-09-16T00:51:57Z reported all 15 organs live, but local reachability probes
were unreliable under high CPU load (load1 about 77/16 cores); fleet status was 4 SSH, 2 LAN,
and 4 down. The exact task was checked as dispatchable for owner `health` and claimed by
`health`.

## Findings

- **Task-autonomy warnings were persistent and state-shaped, not a demonstrated node outage.**
  The interval contains 84 `[health-fail]` rows and 315 task-ledger rows. Witness reported
  60 samples, with 45 `reflex=STALE`, 4 `minds_live=UNKNOWN`, and 59 `ask_unknown=1`.
  These are sampled/ledger signals; the unknown values remain unknown rather than being
  converted to failure. Existing warning chains and their owner-specific triage should be
  reused; no duplicate substrate repair is justified by this report.
- **The task ledger experienced dispatch churn.** Health-fail samples moved between
  `dispatchable=0, unroutable=2` and dispatchable counts as high as 100, while active and
  recovery-wake counts also changed. A later health-fail explicitly identified changing
  elapsed-second keying as promoting one owner-queue condition into new tasks. This is a
  ledger/autonomy follow-up signal, not evidence that routing, DNS, VPN, or firewall state
  should be changed here.
- **There was a concrete high-load event.** A 22:09 health verification recorded
  `llama-server` at 7.9 CPU-hours over 3.3 hours, averaging 238.8% of one core and 54.0%
  currently, above its stated burn floor. The current dashboard independently still shows
  CPU burn and unreliable reachability probes. This warrants continued observation and
  bounded load attribution, not killing or restarting a service from this health lane.
- **Device churn was real but unattributed.** At 22:10 and 22:15, mesh-home emitted CHURN
  deltas 40 and 20 with `candidates=none`, `joint=UNKNOWN_UNATTRIBUTED`; the companion
  udev reading showed 4 events, 2 unattributed, with 100% window coverage. No device identity
  or safe actuator is established.
- **Sensor readings show elevated variability without sustained memory exhaustion.** There
  were 24 samples each for room, CPU load, and memory. CPU load1 ranged 17.75–188.79
  (mean 54.81); memory ranged 44.0–76.3% (mean 58.68). Room was not treated as a binary
  health verdict because the stream includes uncertainty. This supports monitoring the load
  and probe reliability, not a memory or network intervention.
- **Some apparently alarming rows were already resolved work.** The interval contains
  completed receipts and stale/duplicate dispositions, including the completed Phaedra
  steward review and witness chat-range reviews. They were not reopened or duplicated.

## Disposition

The report is complete. Record the high-load/probe-reliability condition and the
unattributed-churn and witness-unknown limitations; retain existing exact follow-ups where
they exist. No safe substrate action follows from this bounded evidence: changing routing,
VPN, DNS, firewall, device state, or forcibly managing `llama-server` would exceed the
observation's proof. The next useful action is a fresh bounded load/probe observation after
contention changes, with the ledger keying issue kept on its existing owner path.

## Verification

- Read the admission report and independently counted the three source row totals shown above.
- Ran `mesh-dash --once check`; observed the live high-load/probe-warning state and organ/fleet
  summary.
- Ran `mesh-task queue --dispatch --owner health`, then
  `mesh-task check dispatch 20260915T220000Z-000000Z/analyze-observation health` (eligible),
  followed by the owner-authored take.
- Correlated bounded `chat.log`, `witness.log`, and `sensors.log`; no substrate mutation was
  performed.
