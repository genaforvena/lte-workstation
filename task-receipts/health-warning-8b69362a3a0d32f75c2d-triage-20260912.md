# Check-stream delta triage: imac-rozalia and local egress

Chain: `health-warning/8b69362a3a0d32f75c2d/triage`  
Checked: 2026-09-12 (UTC)  
Source: health's 2026-09-09 06:38Z check-stream delta reported imac-rozalia changing from offline to active/direct while `mesh-doctor` still failed egress integrity, and LAN/router reachability remained unknown.

## Current evidence

- `tailscale ping --c 2 100.121.88.110` returned `pong from imac-rozalia (100.121.88.110) via 5.227.25.156:55351 in 78ms`. The peer answers on the overlay now; this does not establish LAN reachability or SSH authorization.
- A bounded fresh `mesh-doctor` run printed the same two egress-integrity failures: egress rides `tailscale0`, and an exit node is set (`n2sbt7yy6t11CNTRL`), with Anthropic reachable (405). It then reached `all supervised loops UP` but did not finish within 20 seconds (timeout exit 124), so no complete doctor verdict is claimed.
- The live card refreshed at `2026-09-12T05:28:17Z` reports table 52 routing `100.76.0.1` through `tailscale0`, and explicitly says outward probes stay green while inward LAN sight is dead. `mesh-reflex-health` also marked `router-watch` and `route-events` stale.

## Disposition

The offline-to-active transition is no longer present as a reachability failure: imac-rozalia answers Tailscale ping. The persistent egress-integrity failures and unknown inward LAN/router state remain real. This triage did not test SSH or a LAN path, and did not modify routes, DNS, firewall, VPN, or other substrate state. Route remediation still requires the charter's mesh-trace claim, collision checks, independent reachability evidence, and `mesh-dms` application path.
