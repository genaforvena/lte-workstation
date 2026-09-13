# Health observation analysis: 2026-09-13 16:00–18:00Z

Task: `20260913T160000Z-180000Z/analyze-observation`  
Source: `observation-window:20260913T160000Z-180000Z`  
Interval: `[2026-09-13T16:00:00Z, 2026-09-13T18:00:00Z)`

## Coverage and findings

The generated admission report declares complete bounded coverage: 574 unique events, no exact
duplicates, from `chat.log` (442 rows), `witness.log` (60), and `sensors.log` (72). I checked the
source rows and the associated structured task states.

- **High kernel device-event counts remain only partly attributed.** The full 24-pass
  `device-churn.log` tape has eight CHURN verdicts (deltas 30, 141, 144, 284, 701, 278, 284, and
  130 per ~5-minute interval), eight TICK verdicts at or under the learned floor of 24, and eight
  zero-delta QUIET verdicts. Every CHURN row says `candidates=none`; this scan names only surviving
  USB devices and cannot name removals or non-USB devices. The simultaneous `udev-stream.log` has
  1,002 rows from 16:26:33Z to 17:51:44Z; 980 mention virtual `veth` paths, predominantly `net`
  and `queues`, while the remaining logged rows are `hwmon` or `module`. This is direct evidence
  that virtual-network-device lifecycle events contributed during the interval, but it does not
  establish the creating process/container or explain all seqnum growth. The stream also has
  `sgap` values whose documented meaning is an outstanding gauge, not a per-window loss count.
  Exact creator and residual-event attribution remain open. I found no active exact-owner ledger
  task for this new interval (the earlier churn-board tasks are done), so I created
  `device-churn-attribution-20260913/correlate-high-uevent-bursts`, owned by `senses`, to correlate
  the named paths with contemporaneous workload evidence and quantify the remaining gap. No
  network, USB, container, or service setting was changed.
- **Three health-warning tasks in the window are settled.** The 16:24 direct→relay warning for
  `phaedra` was triaged as recovered by 16:29Z with UDP true; its exact task and receipt are
  complete. The 16:51 witness-task-autonomy warning named a real stale interval, then the referenced
  genome task progressed 55 seconds after the alert; the listener checks were UP and the remaining
  stale-count correction stayed with genome. The 17:27 warning likewise named an unchanged claim;
  `haunt` recorded progress 20 seconds later and completed that step two minutes later. Both
  warning receipts and both task chains are complete, so no duplicate recovery task was opened.
- **Peer relay fallback recurred without a demonstrated UDP cause.** `path-watch` reported
  `imac-rozalia` direct→relay at 16:54Z and again at 17:54Z; the 16:24 `phaedra` episode had already
  recovered. No paired event in this window establishes that local UDP failed, and relay is not
  proof of a LAN or router fault. The 18:19 one-shot pane still showed a degraded path summary
  (8 peers, 1 direct, 1 relay) and warned that high local load made reachability probes unreliable.
- **Historical sensor samples are intermittent, not continuous-state evidence.** The 24 five-minute
  `cpu_load1` readings ranged 8.30–103.77 (mean 25.82); 24 memory readings ranged 19.0–33.9%; room
  sensing was PRESENT 10 times and UNCERTAIN 14 times, with no OFFLINE samples. The 60 witness
  samples reported reflex OK throughout and 4/11 reachable nodes throughout; mind counts were
  UNKNOWN in 7 samples and ask metrics were UNKNOWN in 10. Known stale-ask p90 rose from 151.3h to
  153.3h while resolve ratio stayed 0.746. These records do not prove values between sample times.
- **The household router incident remains externally gated.** The existing
  `wifi-router-periodic-outage-20260913` chain has actuator audit and outage correlation complete,
  with no direct GL-MT3000 writer or temporal actuator match established. Its root-cause-access step
  remains blocked because the router is offline and there is no authorized read-only router path or
  timestamped WAN/uptime/radio/log export. The exact operator-owned prerequisite remains
  `wifi-router-router-access-20260913/establish-router-readonly-access`; the present window supplies
  no new router-side evidence.

## Live health state and disposition

The direct `mesh-dash --once check` read completed at 18:20:11Z. It showed local load at
115.07/16 cores, temperature 72°C, and a warning that the high load made reachability probes
unreliable; the dashboard's doctor section was cached from 17:32:12Z (FAIL=3, WARN=34), so I treat
those doctor values as cached evidence. Its visible detail included egress on `tailscale0`, a
configured exit node, and one recent `room-sense.log` error. A separate live `mesh-health` run at
18:20:21Z returned PASS for mesh-home, imac-rozalia, and phaedra, and OFFLINE for six named peers.
No routing/DNS/VPN or router change is justified from these mixed, load-limited observations.

The warranted new action is the bounded `senses` correlation task above. Router evidence remains
blocked on the operator-owned prerequisite; peer relay remains an attribution uncertainty pending
a contemporaneous paired UDP/path observation. No other follow-up is opened from this interval.

## Verification

- Confirmed the generated report metadata and re-read all three bounded source tapes; source counts
  sum to 574 and deduplication is zero.
- Reviewed all 24 device-churn passes and the corresponding udev-stream rows; ran
  `mesh-device-churn --test` (exit 0), including its real local counter and USB scan path.
- Checked structured task status: both witness-autonomy warning chains are complete; the path
  warning chain is complete; the router chain remains blocked at `root-cause-access`; the new
  attribution task is open and owned by `senses`.
- Read `mesh-dash --once check` and ran `mesh-health`; these are separate live snapshots from the
  historical observation interval.
