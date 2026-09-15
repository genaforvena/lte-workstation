# Health-warning triage: `health-warning/6ef9544142611009bda0/triage`

Date: 2026-09-11T19:49:00Z  
Task: `health-warning/6ef9544142611009bda0/triage`

## Fresh read-only evidence

- `mesh-dash --once check` at 19:48:02Z: current egress is OK, but the pane
  carries the persistent `egress rides tailscale0` and `exit-node set`
  failures; fleet path is degraded and LAN presence is not established.
- `mesh-doctor --once` reached the live checks: 2 FAILs remain (egress via
  `tailscale0`, exit-node SPOF); Anthropic, camera, microphone capture via
  `plughw:2,0`, and supervised loops passed. Default microphone is WARNed.
- `mesh-lan-presence --nodes` returned `UNKNOWN` (`rc=1`): router unreachable
  and no local address in `192.168.8.0/24`.
- `tailscale status` confirms `phaedra` is the active exit node and
  `imac-rozalia` is relay-connected; several peers remain offline/last-seen.
- `mesh-egress-health` completed successfully and reported the same two
  egress-integrity failures; this validates the checker, not the egress path.

## Disposition

KNOWN STALE WARNING / KNOWN BLINDNESS: the 2026-09-08 source warning's
historical-ledger failure was already cleared at 2026-09-08T15:35:31Z. Current
state is still degraded observability: LAN presence is UNKNOWN and egress
continues over `tailscale0` through an exit-node SPOF. No routing, DNS,
firewall, VPN, WireGuard, Tailscale, or service mutation was authorized or
made. Retry on a new health delta or a named substrate owner/operator decision.
