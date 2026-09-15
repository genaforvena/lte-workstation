# Health warning triage: `health-warning/596d5628baeaa613c13f`

Checked: 2026-09-12 16:07 UTC on `mesh-home`  
Owner: `health`  
Task: `health-warning/596d5628baeaa613c13f/triage`

## Finding

The 2026-09-11 16:44:55Z warning records two real, still-visible health failures: this node's egress uses `tailscale0`, and the configured exit node is a single point of failure. The one-shot check pane consumed at 16:07:35Z again showed `egress tailscale0`, doctor failures for overlay egress and exit-node SPOF, and fleet reachability at 2 SSH / 0 LAN / 8 down. The doctor's displayed report is cached from 15:31:58Z, so its total is not a fresh comprehensive scan.

The warning also records LAN presence as `UNKNOWN` because the router was unreachable and the node had no local `192.168.8.x` address. This remains an unresolved visibility gap, not proof that the LAN is down. The most recent explicit read-only route and LAN inspection I found is documented in [the 11:27 triage receipt](../docs/task-receipts/health-warning-bb0a85a9646ebeeded21-triage-20260912.md): it observed `100.76.0.1` routed through Tailscale table 52, the exit node as `phaedra`, and router/LAN presence unknown. I did not repeat substrate probes in this pass.

These are persistent fleet/substrate risks, not a safe local repair inferred from this pane. No routing, DNS, firewall, VPN, or exit-node state was changed. The exact `2F/33W vs 0F/4W` comparison is the historical 16:44:55Z alert; the current pane only establishes that the two named failures remain displayed, not a fresh doctor count or a comparison against the June peer baseline.

## Evidence

- `mesh-dash --once check`, exit 0; pane data timestamp `2026-09-12T16:07:35Z`, live through `16:07:44Z`.
- Pane: `egress tailscale0`, doctor cached `2026-09-12T15:31:58Z` with `FAIL=2 WARN=33`, and the two visible failures are overlay egress and exit-node SPOF.
- Pane: 10 nodes, 2 SSH / 0 LAN / 8 down; no claim is made here that reachability probes are reliable.
- Prior read-only route/LAN evidence and its limits: [health-warning-bb0a85a9646ebeeded21-triage-20260912.md](../docs/task-receipts/health-warning-bb0a85a9646ebeeded21-triage-20260912.md).

Disposition: both egress/SPOF failures remain known and visible; LAN/router status remains a known observation gap. Keep them open for substrate-owner coordination and fresh LAN observation. No substrate mutation was warranted by this triage.
