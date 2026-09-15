# Health warning triage: imac-rozalia path delta

Chain: `health-warning/b10bf9df69ac2293ba14/triage`
Owner: `health`
Observed: 2026-09-15T12:24Z–12:25Z

The warning described `imac-rozalia` changing from active relay to offline, an
unmarked `win-q6gl9fir3qi`, unknown LAN/router presence, and unchanged egress/DNS.

Evidence from the live re-check:

- `mesh-health`: `imac-rozalia PASS`; this node and `phaedra` also PASS.
- `tailscale status --json`: `imac-rozalia Online=true Active=true`, relay `hel`,
  last seen `2026-09-15T11:44:48Z`.
- `tailscale ping --c 2 100.121.88.110`: pong via `192.168.8.214:56461` in 1ms (exit 0).
- `mesh-path-watch --status`: peers=8, direct=2, relay=0, offline=6; iMac reported direct.
- `mesh-lan-presence --nodes`: router unreachable; only GL-MT3000 and Redmi are
  visible through local ARP fallback. This is an existing inward-LAN blind spot,
  not evidence that the warning's LAN state is repaired.
- `api.anthropic.com` still resolves to `160.79.104.10`.
- No routing, DNS, firewall, VPN, or other substrate state was changed.

Disposition: the iMac offline transition is not present in this sample and the
peer is reachable, but its path is volatile (relay in Tailscale status versus
direct in the path-watch sample). The `win-q6gl9fir3qi` no-marker condition was
not independently resolved because no live peer row was available. Keep this
condition observable; do not declare the underlying path/LAN issue fixed.
