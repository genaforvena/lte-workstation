# VPN WireGuard stale-handshake classification — 2026-09-15

Captured at 2026-09-15T16:47:59Z–16:51Z UTC from the VPN window.

## Evidence

| question | observation | result |
|---|---|---|
| local Tailscale backend | `tailscale status --json` → `BackendState=Running`, self `mesh-home` / `100.81.222.19` | local control plane present |
| peer presence | same netmap read → `phaedra` `Online=true`, `Active=true`, RX 337916504 / TX 36689184 | far peer is present and online |
| local uplink age | `uptime -s` → `2026-09-15 11:42:23` | node has not rebooted during observation |
| local route | `ip route get 1.1.1.1` → `via 192.168.8.1 dev enp42s0 src 192.168.8.197` | local egress path is currently concrete and direct |
| end-to-end tunnel | `mesh-dash --once vpn` → port 8444 `PASS`, egress `38.49.216.141`, Montréal | tunnel works |
| phaedra SSH read | `ssh phaedra` exit 0; host uptime since `2026-06-12 15:25:09`; no write/restart attempted | server vantage available |
| phaedra service state | `systemctl is-active wg-quick@wg0.service` → `active`; `shadowsocks-libev.service` → `active`; `trojan-go.service` and `xray.service` → `inactive` | WG/SS service layer is up; these guessed alternate trojan unit names are not the dash's cached trojan probe |
| WG peer activity | `wg show` → 16 provisioned peers: 12 with stale handshakes (16–90 days), 4 with no handshake; peer for `100.81.222.19` last handshake 16d 9h; no current handshakes | no current WG client demand observed |

## Verdict

This is not a server or end-to-end tunnel outage. Local BackendState, the named peer's Online state,
the server's `wg0`/SS services, and the real 8444 fetch are all available. The moved layer is the
WireGuard client-session/activity layer: the provisioned roster is idle/stale. Attribution is bounded
by the cached/reflex evidence; no client should be called down from this node's blindness.

No actuator was used. No routing, DNS, firewall, WireGuard, or service state was changed.

## Commands and exit codes

* `mesh-dash --once vpn`: 0; output captured in the consuming turn.
* `mesh-task create ...`: 0; canonical chain created.
* `MESH_TASK_ACTOR=vpn mesh-task take ...`: 0; task active.
* local Tailscale/route/uptime reads: 0.
* `timeout 15s ssh phaedra ...`: 0.

