# VPN current layer check — 2026-09-14

Task: `vpn-current-layer-20260914/refresh-current-layer`.

## Finding

At 00:21Z the cached service verdict remains DEGRADED only on WireGuard peer
freshness/activity: SS, Trojan, and WG services are up, but the 16 provisioned
peers have 0 active, 0 idle, 12 stale, and 4 never-handshaken; newest handshake
age is 1,271,553 seconds. The end-to-end Shadowsocks port-8444 test passed at
00:19:10Z and local egress health was OK at 00:21:02Z. Current local Tailscale
state and Ethernet carrier are healthy. Client demand/failure and uninterrupted
uplink continuity since boot remain UNKNOWN. No service, peer, route, or firewall
state was changed.

## Evidence and freshness

- `mesh-dash --once vpn` — exit 0; pane snapshot 00:21:16Z. It reports
  `MESH_EGRESS_TUNNEL=off` by design, phaedra Online, SS/Trojan/WG services up,
  WG freshness degraded, and end-to-end port 8444 PASS. The source timestamps
  shown were VPN health 00:20:12Z and SS test 00:19:10Z.
- `tailscale status --json | jq ...` — exit 0 at about 00:21Z;
  `BackendState=Running`, self Online, phaedra present and Online at
  `38.49.216.141:41641`, marked as exit node. This is point-in-time peer/control
  plane proof, not continuity proof.
- `cat /proc/uptime` — exit 0 at about 00:21Z; uptime 46,065.09s (12h47m).
- Read-only `ip -o link` and sysfs carrier/operstate for `enp42s0` — exit 0 at
  about 00:21Z; `UP,LOWER_UP`, carrier 1, operstate `up`. This establishes only
  current link state; no retained artifact proves it stayed up for the whole
  12h47m boot interval.
- Latest `~/.mesh/egress-health.log` rows: route egress `38.49.216.141`,
  `cause=OK`, and quality `OK`, both at 00:21:02Z. The quality row reports
  `loss=0%`, host `1.1.1.1`; this is a recent sample, not continuous uptime.
- Latest `~/.mesh/vpn-health.log` row at 00:20:12Z: `DEGRADED`,
  `SS:up trojan:up wg:up`, no WG client handshake in >24h, 16 provisioned,
  0 active/idle, 12 stale, 4 never; newest handshake age 1,271,553s.
- Latest `~/.mesh/ss-test.log` row at 00:19:10Z: port 8444 PASS, egress
  `38.49.216.141`, Montréal.

## Disposition

The evidence localizes the current degraded label to WG peer activity/freshness;
it does not show an SS/Trojan tunnel failure or active client failure. No
one-line remedy is justified: there is no demonstrated fault to repair and no
missing re-applier established by this observation. Keep client demand/failure
and since-boot uplink continuity UNKNOWN. No actuation is warranted.
