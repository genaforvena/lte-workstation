# Health warning triage: `imac-rozalia` unreachable

Task: `health-warning/8dc5571ba68f5efaacc4/triage`

The 04:36:16Z watchdog warning says `imac-rozalia` (`100.121.88.110`) was not on tailnet and had
no LAN fallback. This is the recurring reachability fault, not the stale GPU sample described in
the older health handoff.

Fresh live evidence at 04:41Z:

- `tailscale status --json` reports `imac-rozalia` `Online=false`, `Active=true`,
  `LastSeen=2026-09-14T04:16:06.1Z`, `LastHandshake=0001-01-01T00:00:00Z`, and no current endpoint.
- `tailscale ping --timeout=3s 100.121.88.110` timed out. The health pane also warns that high
  local load makes reachability probes unreliable, so the timeout is corroborating evidence, not a
  diagnosis of physical power or the Mac's cause of failure.
- `~/.mesh/nodes` has an SSH `MESH_NODES` entry for the iMac, but `MESH_LAN_FALLBACK` lists only
  `GL-MT3000` and `router`; no fallback path is configured for this peer.
- Existing task `health-warning/0ac2476a343fdde6c790/triage` remains blocked on the same dependency:
  a currently reachable owner/path for the offline iMac. Its retry edge is `event:roll-call-delta`.

Disposition: active tailnet reachability failure; physical state and root cause remain unknown.
There is no safe local correction while the peer and an alternate path are unavailable. Reuse the
existing external dependency and retry on `event:roll-call-delta`; keep this task blocked meanwhile.
No route, DNS, firewall, VPN, Tailscale, or remote-node state was changed.
