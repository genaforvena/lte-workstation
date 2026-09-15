# Health observation analysis: 2026-09-14 04:00–06:00Z

Task: `20260914T040000Z-060000Z/analyze-observation`  
Source: `observation-window:20260914T040000Z-060000Z`  
Interval: `[2026-09-14T04:00:00Z, 2026-09-14T06:00:00Z)`

## Coverage and bounded findings

The admission report declares complete readable coverage: 453 rows from `chat.log` (321),
`witness.log` (60), and `sensors.log` (72), with no duplicates. I independently recounted those
timestamp-bounded rows. The first hour overlaps the preceding `03:00–05:00Z` health receipt, so I
reused its iMac and current-route history and checked the new source rows rather than treating them
as fresh evidence.

- **A device-churn alert was dominated by signed self-probe events.** The mesh-home counter reported
  `delta=84` at 05:25:05Z, above its learned floor of 24, and boarded it as a real enumeration. The
  matching udev summary at 05:26:04Z has `events=84`, `seqdelta=84`, and `seq-total=10921`: 83 rows
  carry the source signature of a mesh-generated probe and one unsigned row names the PCI hwmon
  path. This does not support calling all 84 an external enumeration. The next counter interval
  ended at 05:30:02Z with `delta=102`; only 84 rows for seqnums 10922–11023 are retained in the
  listener log (81 signed probes and three unsigned rows), leaving 18 sequence events unobserved.
  I do not subtract a ratio or assign the gap. The exact complete-match and incomplete-stream cases
  are registered for genome as `device-churn-signed-probe-attribution-20260914`; its plan is
  `task-receipts/device-churn-signed-probe-attribution-20260914.plan.tsv`. Existing
  `device-churn-attribution-20260913` and `device-churn-live-join-20260913` are completed and do not
  address this signed-probe classification.
- **The iMac reachability issue remains externally blocked.** The window repeats an iMac
  direct-to-relay observation and watchdog SSH-unreachable reports. The exact health task
  `health-warning/8dc5571ba68f5efaacc4/triage` is already dependency-blocked on
  `event:roll-call-delta`; its prerequisite attempt is complete and found no reachable owner or
  alternate LAN path. I reused that task and did not duplicate probes or claim relay use identifies
  the fault. The current `mesh-health` read still marks `imac-rozalia` offline.
- **Witness telemetry is consistently sampled, with explicit unknowns.** All 60 rows say
  `reflex=OK` and `nodes=3/11`; `minds_live` is 15 in 49 rows and UNKNOWN in 11. Ask fields are
  UNKNOWN in 19 rows; among 41 known samples, `ask_p90_h` ranges from 163.3h to 165.3h and
  `ask_resolve` remains 0.746. These values do not show a new witness-health failure inside the
  interval. A later autonomy warning at 06:21Z is outside this window.
- **Historical room and resource readings are samples, not continuous state.** Of 24 room samples,
  15 were PRESENT, 7 UNCERTAIN, and 2 OFFLINE. The 24 `cpu_load1` samples range 10.24–133.73
  (median 20.64); 24 memory samples range 21.1–45.0% (median 33.5%). The 04:53 high-load sample
  was not sustained in these samples: 05:53 reads 28.09. The separate current pane still displayed
  high local load at 06:20, which is live state outside the historical interval.

## Current state observed separately

`mesh-dash --once check` completed at 06:20Z and showed a degraded fleet (2 SSH-reachable nodes,
8 down), local load around 118.65/16 cores, one visible Python process at about 72% CPU, and 24
alarm plus 27 stale organ states among 138. The pane's doctor section was cached, so its findings
are not fresh diagnosis. `mesh-health` at 06:21Z independently showed mesh-home and phaedra
reachable and the other listed peers offline.

At 06:29Z, read-only `mesh-card --exit-node-lan`, `ip route get 100.76.0.1`, `ip route show table
52`, and `ip rule show` agreed: the live DHCP address was `100.76.34.107/16` on `enp42s0`, the
gateway `100.76.0.1` resolved on `enp42s0`, and the exit-node card verdict was OK. Table 52 keeps
the local connected CIDR as a throw and the default on `tailscale0`. This differs from the
100.74/16 card reading seen during an earlier live poll in this turn, so route state was re-read
against the then-current interface and gateway. No route, rule, VPN, DNS, or remote-node state was
changed. The exact follow-up `exit-node-lan-cgnat-live-repair-20260914` is active: VPN owns its
dispatch-time re-derivation and application gate, and health's independent verifier remains open;
that verifier's dispatch check returned 2 while VPN's step was active, so I did not take it.

## Disposition

The bounded report is complete, so this task closes with evidence rather than retrying. The
mesh-home counter's 05:25 alert overstates external churn in the exact interval where 83/84 events
were signed self-probes; the following 102-count interval remains partly UNKNOWN because 18 events
are absent from the retained listener rows. I registered a narrow source-aware follow-up and left
implementation to genome. The iMac task remains blocked on its recorded external event. The current
gateway FIB is healthy on the live interface, and the existing route chain retains the next
dispatch-time check. No substrate action was safe or warranted from this read.

## Verification

- Re-read `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T040000Z-060000Z.md`;
  independently counted the bounded source rows as 321/60/72.
- Re-read bounded witness, sensor, device-churn, udev-stream, and path-watch logs; matched the
  05:25 counter total to the 05:26 udev summary and counted seqnums 10922–11023 directly.
- Checked the iMac health task and the active route-repair chain. The independent route-verifier
  dispatch check returned 2; it was not claimed.
- Read the one-shot pane, `mesh-health`, the current exit-node card, main/table-52 routes, and
  policy rules. No routing write was attempted.
- Registered `device-churn-signed-probe-attribution-20260914` to genome. Its task is open and
  owner-routed; no implementation is claimed here.
