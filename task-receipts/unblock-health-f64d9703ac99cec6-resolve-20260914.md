# Dependency resolver: iMac path remains unavailable

Resolver: `unblock/health/f64d9703ac99cec6/resolve`
Parent: `health-warning/8dc5571ba68f5efaacc4/triage`
Checked: `2026-09-14T04:57Z` UTC on `mesh-home`.

The exact-owner dispatch check for this resolver exited 0, and `health` claimed it. Fresh
read-only checks confirm that neither prerequisite is available:

- `tailscale status` reports `imac-rozalia` (`100.121.88.110`) offline, last seen 41 minutes ago;
  `tailscale ping --c 1 --timeout 3s imac-rozalia` timed out with no reply.
- The only recorded candidate LAN address is `192.168.8.214` (`mac` in `~/.mesh/nodes`).
  `ip route get 192.168.8.214` selects `via 100.74.0.1 dev enp42s0`, so it is routed through the
  overlay gateway rather than a verified LAN path. A bounded ping received no reply and a bounded
  TCP/22 connection was unavailable.
- `MESH_LAN_FALLBACK` has no iMac entry; its configured hosts are only the GL router aliases.
  `mesh-minds` did not finish its broad reachability scan within the observation window; it was
  stopped, so it provides no positive owner-reachability evidence.
- Prior receipt `task-receipts/unblock-health-a4e98e93cbf0b327-resolve-20260914.md` independently
  records the same missing Tailscale and LAN paths earlier this morning.

These observations do not distinguish a powered-off or sleeping Mac from a disconnected or
filtered path. They establish no safe way for this node to reach the iMac or a verified alternate
LAN route, and no reachable authorized owner was found. No substrate or remote-node state changed.

Keep parent `health-warning/8dc5571ba68f5efaacc4/triage` dependency-blocked; do not resume it until
a roll-call/path change establishes a reachable iMac owner or verified alternate LAN path.
Retry edge: `event:roll-call-delta`.
