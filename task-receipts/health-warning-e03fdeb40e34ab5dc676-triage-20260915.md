# Health warning triage — historical doctor recovery — 2026-09-15

Task: `health-warning/e03fdeb40e34ab5dc676/triage`

## Evidence

- Read the cited observation `/home/mesh-home/.mesh/observations/check-stream-20260914T1621Z/result.md`.
  It records a complete `mesh-doctor` run with exit 0 and `0 FAIL / 34 WARN`, down from
  `2 FAIL / 33 WARN`; the two egress failures were no longer failures and became an
  integrity PASS plus a single-node SPOF NOTE.
- The same observation records LAN presence still UNKNOWN/router unreachable, tracked
  Tailscale state with `imac-rozalia` active/direct and no status marker for
  `win-q6gl9fir3qi`, unchanged egress/DNS, and no substrate changes.
- Current `mesh-dash --once check` at 20:36Z shows PATH OK and egress OK, with local
  load high and broad reachability probes unreliable. It still shows router/LAN
  uncertainty and observe-only degraded VPN state, so those are not silently promoted
  to healthy substrate claims.
- A direct `mesh-egress-health` check completed with `rc=0`. The current pane reports
  `1 FAIL / 33 WARN` from a cached doctor view; the latest readable doctor log entry is
  19:23Z and includes a dispatch-log FAIL, so the older 16:21 `0/34` result is treated
  as historical evidence, not a current doctor verdict.

## Disposition

Superseded historical check-stream warning: the reported doctor/egress recovery was
real in its bounded observation, and current egress remains healthy enough. LAN/router
uncertainty, stale doctor cache, high-load probe unreliability, and the current
dispatch-log failure remain separate current observations. No routing, DNS, firewall,
VPN, device, service, or privilege mutation is justified.

## Verification

Read the complete cited observation, current pane state, doctor log, and live egress
check. No substrate state changed.
