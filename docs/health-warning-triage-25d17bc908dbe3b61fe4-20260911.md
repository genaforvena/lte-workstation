# Health-warning triage: 25d17bc908dbe3b61fe4

Date: 2026-09-11
Task: `health-warning/25d17bc908dbe3b61fe4/triage`

## Fresh read-only evidence

- `mesh-dash --once check` at 17:14Z: local vitals are OK; current egress is
  reachable, while cached doctor state still reports `egress rides tailscale0`
  and `exit-node set (n2sbt7yy6t11CNTRL)`; fleet path is degraded (`2 SSH, 0
  LAN, 8 down`) and the pane reports 27 alarm / 35 stale states.
- `mesh-health` at 17:14Z: `mesh-home` and `phaedra` PASS; Redmi 10, ilya,
  GL-MT3000, and other tagged nodes are offline; imac-rozalia is SSH
  unreachable.
- `mesh-egress-health` completed with exit 0. This validates the checker and
  current reachability, not a green verdict for the cached configuration
  warnings.
- `timeout 20 mesh-lan-presence --nodes` exited 124. LAN presence is therefore
  UNKNOWN, not DOWN.
- `tailscale status` at 17:14Z shows `phaedra` active as exit node and
  `imac-rozalia` active direct; Redmi 10 and ilya remain offline.
- `ip route get 192.168.8.1` resolves via `enp42s0` (source
  `100.74.203.87`). This is observation only.

## Disposition

The fresh delta confirms a reporting-only known degraded/observability
condition. Current egress is reachable, but the tailscale0/exit-node warnings
remain and LAN presence is UNKNOWN because its bounded probe timed out. No
routing, DNS, firewall, VPN, WireGuard, Tailscale, or service mutation was
made. Keep the condition visible; retry on a new health delta or a named
substrate owner for any corrective change.
