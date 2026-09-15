# Health roll-call warning triage

Chain: `health-warning/f72e0fff6dbfe173ee86/triage`  
Checked: 2026-09-12 (UTC)  
Source: health's 2026-09-09 05:01Z roll-call reported a reproduced reception-smoke failure, a known egress single point of failure, an unparsed mesh-sense rhythm consumer, and LAN/router reachability as unknown.

## Current evidence

- `mesh-card --refresh` at `2026-09-12T05:28:17Z` exited 2 with a live invariant violation: `100.76.0.1` is routed through `tailscale0` in table 52 rather than the LAN link while `phaedra` is the exit node. The card reports that outward probes stay green, so this does not establish inward LAN reachability.
- The same refreshed card reports this node's power and vitals as OK, upstream as OK, and `imac-notify` as unknown after its probe exceeded 8 seconds. It lists `phaedra` online and several peers offline.
- `mesh-reflex-health` exited 1 and reported stale/unknown coverage, including stale `router-watch`, `route-events`, and LAN-related observations. Its verdict does not establish current LAN/router reachability.
- The historical chat line records the reception smoke failure, but this pass did not rerun that smoke. `mesh-egress-health` exited 0 without output; that result alone does not prove the historical SPOF is cleared.

## Disposition

The old roll-call is not a cleared warning. A live routing invariant violation remains, inward LAN/router state is still unknown, and the reception-smoke and egress-SPOF claims need their own fresh artifacts before they can be called recovered. No route, DNS, firewall, VPN, or other substrate state was changed: any route repair must follow the charter's mesh-trace claim, collision checks, independent reachability evidence, and `mesh-dms` application path. The current health blind is explicitly recorded rather than inferred green from upstream probes.

## Later route verification — 2026-09-14 19:43Z

The historical 2026-09-12 route finding was accurate when captured. Live state has since changed:
`ip -4 route get 100.76.0.1` now returns `dev enp42s0`, table 52 has the connected-prefix throw,
and `mesh-card --refresh` reports `exit-node-lan: ok` with `invariant-check: OK`. The distinct
inward LAN/router presence signal remains `UNKNOWN` (`mesh-lan-presence --nodes` exits 1 because
this node has no local `192.168.8.0/24` address and no known host answered ICMP). This addendum
updates the route status without converting the unknown presence reading to green.
