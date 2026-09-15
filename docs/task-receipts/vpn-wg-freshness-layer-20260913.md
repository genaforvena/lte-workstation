# VPN WireGuard freshness layer check — 2026-09-13

Task: `vpn-wg-freshness-layer-20260913/classify-wg-freshness`.

## Finding

At 21:22–21:25Z the available evidence localizes the cached `DEGRADED` verdict to
WireGuard peer freshness/activity. It does not establish failed client access or a
phaedra-side service outage. Treat client fault and uninterrupted local uplink
continuity as UNKNOWN; do not restart services or edit peers/routes from this evidence.

## Evidence

- `mesh-dash --once vpn` at 21:18:50Z showed this node has no consumer tunnel by design
  (`MESH_EGRESS_TUNNEL=off`), the router carries VPN egress, phaedra is Online, and the
  cached health row is `DEGRADED` with SS/trojan/WG up. It reported 16 WG peers, 0 active,
  0 idle, 12 stale, 4 never, and newest handshake age 1,260,151s. Port 8444 had passed
  at 21:09Z.
- A read-only `mesh-vpn-health` invocation at 21:22:24Z returned exit 0 and refreshed
  `~/.mesh/vpn-health.log`: the same services-up verdict, 16 peers, 0 active/idle,
  12 stale, 4 never, newest handshake age 1,260,887s (about 14.59 days). This is a
  peer-activity signal, not a failed client attempt.
- `tailscale status --json` at about 21:22Z returned `BackendState=Running`,
  `Self.Online=true` for mesh-home, and phaedra present with `Online=true`,
  `CurAddr=38.49.216.141:41641`, `Relay=tor`, and `ExitNode=true`. This proves current
  local control-plane/peer visibility, not continuous uptime.
- `mesh-ss-test --edge` exited 0 and wrote `2026-09-13T21:23:24Z port 8444 — PASS`
  to `~/.mesh/ss-test.log` (egress `38.49.216.141`, Montréal). The result is a point
  fetch, not proof of uninterrupted service between samples.
- The latest `~/.mesh/egress-health.log` observation at 21:21:01Z returned egress
  `38.49.216.141`, `loss=0%`, and `path=route`; its separate quality row says
  `BAD where=hop1-unknown`, `streak=0/2`. This does not establish an egress outage.
- At 21:25Z `/proc/uptime` was 35,361.51s (about 9h49m). `mesh-usb --status` reported
  no USB-attached network interface, while `enp42s0` was currently `UP,LOWER_UP` with
  carrier 1. No observed artifact proves that the main Ethernet uplink stayed up for
  the full boot interval; uplink continuity since boot remains UNKNOWN.

## Verification record

Commands and outcomes:

- `mesh-dash --once vpn` — exit 0; cached pane timestamp 21:18:50Z.
- `tailscale status --json | jq ...` — exit 0; BackendState and peer fields above.
- `mesh-vpn-health --help` — exit 0; this installed script does not implement `--help`
  and ran its read-only health probe, producing the 21:22:24Z row above.
- `mesh-ss-test --edge` — exit 0; fresh PASS line at 21:23:24Z.
- `mesh-usb --status` — exit 0; no USB uplink; node uptime 9.8h.
- `ip -o link show dev enp42s0` plus carrier/operstate reads — exit 0; currently UP,
  LOWER_UP, carrier 1.

Source log SHA-256 values captured after the observations:

- `~/.mesh/vpn-health.log`: `35fb6a1a637445727990d36290e68b3a2524ec186f0a4c2826c5374275dcb095`
- `~/.mesh/ss-test.log`: `5306585bca0a0545737cf5915dfa3fa0abc7d8948636517354bcee8791143f4f`
- `~/.mesh/egress-health.log`: `5a560854a265f91559764bb5929104d9dfe1a61f69d3277f331f55d054871ae9`

Disposition: current evidence supports `[fyi]` naming WG peer freshness/activity as the
degraded layer. There is no evidence of an active client failure or a one-line repair
without a re-applier; no actuation is justified. The earlier state transition is recorded
in `docs/task-receipts/vpn-verdict-transition-20260913.md`.
