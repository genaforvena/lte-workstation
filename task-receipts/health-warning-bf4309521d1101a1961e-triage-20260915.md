# Health warning triage — 2026-09-15

Task: `health-warning/bf4309521d1101a1961e/triage`
Owner: `health`
Observed: 2026-09-15T22:58Z–22:59Z UTC

## Finding

The warning reported a change from Tailscale table 52 to the LAN gateway for
public egress. The live state now corroborates the LAN path:

- `ip route get 1.1.1.1` → `via 192.168.8.1 dev enp42s0 src 192.168.8.197`.
- `ip route show table 52` contains Tailscale peer routes, but no public
  default route; `mesh-card --refresh` reports `default-egress: dev enp42s0`,
  `exit-node: none`, and `invariant-check: OK`.
- `getent ahosts api.anthropic.com` resolves to `160.79.104.10` (plus IPv6
  `2607:6bc0::10`), matching the warning's unchanged DNS observation.
- `mesh-lan-presence` reports router reachability unavailable and uses local
  ARP fallback; GL-MT3000, Redmi, and other LAN devices are still observed.
- A live `mesh-egress-health` run exited 0 with no alarm output.

## Decision

This is a reconciled historical route-change warning, not a current substrate
failure. The current route is clean and the node invariant is satisfied. No
route, DNS, firewall, VPN, or other substrate change was safe or necessary.
The remaining router-reachability warning is a known observation blind spot,
not evidence that the current public egress is misrouted.

