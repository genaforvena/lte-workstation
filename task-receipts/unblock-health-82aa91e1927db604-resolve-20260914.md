# Dependency resolver: iMac path remains unavailable

Resolver: `unblock/health/82aa91e1927db604/resolve`
Parent: `health-warning/2ca0e1c7ec6377531951/triage`
Checked: `2026-09-14T08:47–08:49Z` UTC on `mesh-home`.

The exact-owner dispatch check exited 0 and `health` claimed this resolver. The parent is still
live and dependency-blocked. Fresh read-only evidence confirms neither prerequisite is available:

- `tailscale status --json` reports `imac-rozalia` (`100.121.88.110`) as
  `Online=false`, `Active=true`, `CurAddr=""`, last seen at `08:17:22Z`. `GL-MT3000` is also
  offline; `phaedra` is online, but no LAN subnet route is installed here.
- This node has `enp42s0=100.74.146.19/16`. `ip route` has no `192.168.8.0/24` route, and
  `ip route get 192.168.8.214` selects the default gateway `100.74.0.1` via `enp42s0`, not a
  LAN interface. A bounded SSH attempt to `ilya@192.168.8.214` timed out.
- The runtime config lists `imac:192.168.8.214` under `MESH_LAN_DEVICES` for LAN-device
  monitoring, and separately maps `mac:ilya@192.168.8.214` in `MESH_NODES`. Those entries do not
  provide a reachable SSH fallback: `mesh-peer-addr` reads `MESH_LAN_FALLBACK` (plus the phone
  list), and that map contains only `GL-MT3000:192.168.8.1` and `router:192.168.8.1`. Live
  `mesh-peer-addr imac-rozalia` confirms there is no fallback entry and returns the Tailscale
  address only as a guess. `mesh-peer-addr mac` likewise finds no fallback.
- The one-shot pane warned that high local load makes reachability probes unreliable; current
  load averages were `35.21/51.79/42.11` on 16 cores. Therefore the SSH timeout does not establish
  the Mac's power state or cause. The absent route and absent configured fallback do establish
  that this node has no verified LAN path. No reachable owner path was found.
- The newest `roll-call@mesh-home` digest in the canonical log is `05:08:24Z`; there is no later
  roll-call delta by the current `08:49Z` log tail. The requested retry event has not occurred.

No safe local code or config change can create the missing external route or make the Mac answer.
Adding `192.168.8.214` as an SSH fallback here would only encode an unreachable guess. No routing,
DNS, firewall, VPN, Tailscale, or remote-node state was changed. The task's “no LAN fallback” is
accurate for the SSH resolver contract, though a monitoring address and a second MESH_NODES label
do exist; neither is an independently available path from this node.

Disposition: finish this resolver with the evidence-backed blocked result; keep parent
`health-warning/2ca0e1c7ec6377531951/triage` blocked. Do not resume it until a roll-call/path change
establishes a reachable iMac owner or verified independent LAN path. Retry edge:
`event:roll-call-delta`.

Verification: `mesh-task status health-warning/2ca0e1c7ec6377531951`; exact-owner
`mesh-task check dispatch unblock/health/82aa91e1927db604/resolve health` (exit 0); live Tailscale
peer status; interface/route and route lookup; `mesh-peer-addr` for both iMac labels; bounded SSH
probe; and canonical `chat.log` roll-call chronology.
