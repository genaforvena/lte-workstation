# Health warning triage: iMac reachability delta

Task: `health-warning/04cb202a853c5a65ada5/triage`

The warning (2026-09-14T07:01:37Z) reported `imac-rozalia` advancing from roughly one hour to
39 minutes last-seen while offline via relay, and `win-q6gl9fir3qi` having no status marker. It
also recorded unreliable reachability probes during high local load and an incomplete comprehensive
doctor run.

Fresh read-only evidence at 2026-09-15T17:08Z:

- `mesh-health` exits 0 and reports `PASS imac-rozalia 100.121.88.110`.
- `tailscale status --json` reports the iMac `Online=true`, `Active=true`, current handshake
  `2026-09-15T17:08:04Z`, and current LAN endpoint `192.168.8.214:56461`.
- `tailscale ping --timeout=3s 100.121.88.110` succeeds: `pong ... via 192.168.8.214:56461 in 1ms`.
- Plain `tailscale status` shows the iMac `active; direct`; `win-q6gl9fir3qi` still renders `-`
  with no connection marker. The Windows state remains unknown, not proven powered off.
- `mesh-net-triage` exits 0 but reports `DEGRADED ... path=MARGINAL ... tcp=LOSSY`; LAN gateway
  and WAN anchors are reachable.
- `mesh-card --refresh` exits 0, records clean default egress via `enp42s0`, no exit node, and
  invariant-check `OK`.
- A bounded `timeout ... 20 mesh-doctor --quiet` returns 124 under current load; the only emitted
  line is the known `mic DEFAULT device broken/busy` warning. Comprehensive totals were not claimed.

Disposition: the iMac reachability warning is resolved at this observation; the Windows missing
status marker and marginal/lossy path remain known visibility/health issues. No route, DNS, firewall,
VPN, Tailscale, or remote-node state was changed.
