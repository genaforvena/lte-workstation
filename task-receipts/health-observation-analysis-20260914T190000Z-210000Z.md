# Health observation analysis: 2026-09-14 19:00–21:00Z

Task: `20260914T190000Z-210000Z/analyze-observation`  
Source: `observation-window:20260914T190000Z-210000Z`  
Interval: `[2026-09-14T19:00:00Z, 2026-09-14T21:00:00Z)`

## Admission and independent recount

The admission report is complete: 707 retained events, comprising 575 `chat.log`, 60
`witness.log`, and 72 `sensors.log` rows, with zero deduplications. Independent half-open
interval filtering of the three source tapes reproduced those counts.

## Findings

- **No bounded evidence justifies a substrate change.** The current one-shot health pane at
  2026-09-15T11:39Z reports supervised 4 up / 0 down and 13 live / 0 dark organs, but also
  reports one fleet node down, stale path data, cached doctor FAIL=2/WARN=35, and egress
  currently skipped because the interface is unreachable. These are current observations,
  not evidence that the historical window had a repairable local fault. No routing, DNS,
  firewall, VPN, device, container, service, or privilege state was changed.
- **The sampled iMac path alternated without a demonstrated cause.** `path-watch.log` has
  12 `imac-rozalia` transitions in the interval, alternating direct and relay every ten
  minutes. `netweather` at 19:54Z and 20:54Z reports UDP true, with DERP Helsinki latency
  33.4ms and 35.1ms. This establishes path churn, not continuous loss or a remote cause.
- **Room sensing is intermittent.** The 24 five-minute sensor samples contain 13 PRESENT,
  9 UNCERTAIN, and 2 OFFLINE values. CPU load1 ranged 9.35–113.47 and memory use
  22.4–69.9%; these samples show variability, not sustained memory exhaustion or a
  continuous occupancy state.
- **Uevent attribution remains partial.** In-window device-churn ticks include delta=18
  at 19:05Z (12 unknown/missing), delta=8 at 19:10Z (6 unknown/missing), and delta=24 at
  19:30Z (18 unknown/missing); the 19:15–19:25 and 19:35–19:55 ticks are quiet. The
  sequence counter is global while `mesh-udev-stream` observes only its own namespace, so
  the missing events cannot be named or attributed from this window.

## Disposition

Retain the negative result and known blindnesses: fleet reachability is probe-limited,
LAN/remote presence is incomplete, iMac route changes are unexplained samples, room sensing
is intermittent, and uevent sequence gaps are only partially attributed. The actionable
follow-up is to capture `scripts/mesh-docker-veth-join --seconds 300 --max-events 1000`
alongside `scripts/mesh-udev-stream --tail 1000` on the next comparable live CHURN or
positive-missing tick; preserve residuals as unknown. No prerequisite task was needed for
this complete report.

## Verification

- Read the complete admission report and independently recounted all three source tapes;
  counts matched (575/60/72) and exact duplicate removal remained zero.
- Correlated `path-watch.log`, `device-churn.log`, and `sensors.log` over the half-open
  interval; observed 12 path transitions, 24 room/CPU/memory samples, and the listed
  partially attributed churn ticks.
- Ran `mesh-dash --once check` at 2026-09-15T11:39Z for current state; it reported the
  current egress skip, cached doctor FAIL=2/WARN=35, and all organs live.
- No substrate mutation or external probe was required for this evidence classification.
