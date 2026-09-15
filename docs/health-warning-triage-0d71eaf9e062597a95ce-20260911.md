# Health-warning triage: 0d71eaf9e062597a95ce

Date: 2026-09-11
Task: `health-warning/0d71eaf9e062597a95ce/triage`

## Fresh read-only evidence

- `mesh-dash --once check` at 12:25Z: organs 14 live/0 dark; current egress OK,
  but cached doctor still records the known FAILs `egress rides tailscale0` and
  `exit-node set (n2sbt7yy6t11CNTRL)`; fleet path is degraded and LAN probe is
  warned unreliable under high local load.
- `mesh-egress-health`: exit 0.
- `timeout 20 mesh-lan-presence --nodes`: exit 124, therefore LAN presence is
  UNKNOWN, not DOWN.
- `tailscale status`: `imac-rozalia` is active via relay; `phaedra` is active,
  direct, and the exit node; several tagged peers are offline or relay-only.
- `ip route get 192.168.8.1`: route resolves via `enp42s0` (`100.76.0.1`,
  source `100.76.130.184`).

## Disposition

The warning is a reporting-only known degraded/observability condition. Current
egress is reachable, but the cached doctor failures and exit-node/tailscale0
configuration remain unresolved; LAN presence remains UNKNOWN because the probe
timed out. No routing, DNS, firewall, VPN, Tailscale, or service mutation was
made. Keep the condition visible and require the substrate owner/operator to
decide the routing and exit-node changes.
