# Health observation analysis: 2026-09-13 23:00–2026-09-14 01:00Z

Task: `20260913T230000Z-010000Z/analyze-observation`  
Source: `observation-window:20260913T230000Z-010000Z`  
Interval: `[2026-09-13T23:00:00Z, 2026-09-14T01:00:00Z)`

## Coverage and findings

The admission report declares complete evidence: 345 rows, 345 unique events, and no duplicates.
Independent timestamp extraction from the retained tapes matched that count: 213 chat rows
(`chat.log:61230-61442`), 60 witness rows (`witness.log:4930-4989`), and 72 sensor rows
(`sensors.log:55790-55861`).

- **Local CPU load stayed highly variable and repeatedly exceeded core count.** The 24 five-minute
  samples ranged from 8.17 to 151.61 on a 16-core node (median 26.28; 16/24 above 16, 8 above 32,
  and 5 above 64). Memory ranged 21.3–33.6% (median 25.5%). Room sensing was `PRESENT` in 10,
  `UNCERTAIN` in 8, and `OFFLINE` in 6 samples. These point samples do not establish a continuous
  episode or its cause. The live check pane at 01:19Z showed load 108.14/16 with `llama-server`
  using 74.8% CPU; its fleet reachability warning explicitly said high local load made probes
  unreliable.
- **Global uevent increments again lacked a named source.** The complete five-minute
  `device-churn.log:5091-5114` interval has 13 `QUIET`, 7 `TICK`, and 4 `CHURN` rows, totaling 202
  seqnum increments. The four `CHURN` deltas were 37, 3, 24, and 26; the accumulator's learned
  floor changed during the interval, so the delta of 3 was also tagged `CHURN`. All 38 named rows
  in `udev-stream.log:5751-5788` are `change` events for the same `hwmon2` DEVPATH. None names a
  veth, container, USB device, or other endpoint. The global counter does not attribute the
  increments. Do not infer a Docker or physical-device cause from timing or count. The existing
  bounded veth/container observer remains appropriate only on a future *named* veth/container
  burst; this window does not warrant a duplicate observer or cleanup action.
- **Path to imac-rozalia repeatedly changed and then went offline.** The retained path tape
  (`path-watch.log:4017-4026`) records eight direct/relay/offline transitions between 23:09Z and
  00:19Z, with five consecutive direct-to-relay transitions and an offline state at 00:19Z. UDP
  was later reported true at 00:54Z, but that does not prove the peer recovered. No root cause is
  established. At 00:52Z health separately reported the peer offline after a relay interval;
  router/LAN presence remained unknown. Preserve this as observed path instability, not a cause
  claim.
- **Witness reflex stayed green while other observations remained incomplete.** Reflex was `OK`
  in all 60 rows, while node reachability varied only between 3/11 and 4/11. Live-mind counts were
  14–15 when known and `UNKNOWN` in 8 rows; ask resolution remained 0.746 when reported, while
  ask data was unknown in 14 rows. Stale-ask p90 rose from 158.3h to 160.3h where present. Missing
  values are not zeroes, and a green reflex does not establish complete fleet or ask health.
- **The completed aggregate-doctor fix did not resolve long-run observability.** The prior
  `health-doctor-aggregate-20260914/audit-help-recursion` receipt records the help fallthrough fix
  and a completed cron result of 2 FAIL/33 WARN at 00:31:43Z. At 00:52Z health observed a later
  comprehensive run still in node-aware smoke tests; at 00:57Z it was interrupted after about
  eight minutes without final totals. This is a new incomplete run after the CLI fix, not evidence
  that the help recursion remains. The earlier receipt says no phase-level timing cause was
  established and calls for bounded phase tracing if a later run again fails to finish. That
  condition has now recurred, so I registered linked follow-up
  `health-doctor-node-aware-stall-20260914/trace-node-aware-phase` to inspect the existing run/lock
  first and trace the slow phase without starting a competing aggregate.
- **A witness task-autonomy alert already has a receipt.** The 23:15Z `[health-fail]` about a
  stalled witness autoland task was triaged by the existing `health-warning/ff3ff85.../triage`
  work and closed at 23:29Z; that receipt says the original remains queued behind its exact
  steward prerequisite. No duplicate task was opened.

## Current pane and disposition

The consumed one-shot `check` pane footer was 01:19:56Z. It showed 2 SSH / 0 LAN / 8 down fleet
nodes, 8 overlay peers with 1 direct and 7 offline, and warned that high load made reachability
probes unreliable. The cached doctor result was stamped 00:31:43Z at 2 FAIL/33 WARN, not a fresh
aggregate. Current egress probed OK at 0% loss, but still used `tailscale0`; its 24-hour aggregate
remained BAD (0/412 with 59 unattributed), and the configured exit node remained a SPOF. The pane
showed 108.14/16 load, `llama-server` at 74.8% CPU, GPU healthy, and all organs live despite
24 alarm / 26 stale states. These are time-bounded pane readings, not diagnoses.

No routes, DNS, firewall, VPN, or service state changed. The report's safe operational action is
the linked bounded doctor follow-up; do not start another aggregate while an invocation holds the
doctor lock. The path, egress, and exit-node findings remain observed substrate alarms for the
designated substrate writer.

## Verification and sources

- Read `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260913T230000Z-010000Z.md`:
  `evidence_complete=yes`, 345 unique events, zero duplicates.
- Independently counted bounded chat, witness, and sensor rows; exact line spans are listed above.
- Summarized all 24 five-minute local device-churn rows, all 38 named udev rows, and the 10
  path-watch rows in the same interval.
- Read the completed doctor follow-up at
  `task-receipts/health-doctor-aggregate-20260914-audit-help-recursion.md` and the existing
  stalled-witness triage receipt before deciding whether to register another task.
- Ran `mesh-dash --once check`; its payload reported pane-live 01:19:56Z. The shell session did
  not return within the initial 10 seconds, so it was interrupted to retrieve the complete output.
- No code or substrate configuration changed.
