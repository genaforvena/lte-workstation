# Health unblock resolver: iMac path recovered

Resolver: `unblock/health/807797d851d3d242/resolve`
Parent: `health-warning/2ca0e1c7ec6377531951/triage`
Checked: 2026-09-14 08:54–09:01 UTC on `mesh-home`.

The exact-owner dispatch check exited 0 and `health` claimed this resolver. The one-shot
`mesh-dash --once check` stream showed the fleet degraded (10 nodes: 3 SSH, 0 LAN, 7 down),
with the iMac listed reachable and `NO-CARD`; its alarm summary included 24 alarms and 28 stale
states. The stream also showed this node's two cached doctor failures (egress via `tailscale0`
and exit-node SPOF risk), but those were outside this resolver's scope.

Fresh path evidence changed the previous blocker disposition:

- `chat.log` records `[health-ok] imac-rozalia — RECOVERED (100.121.88.110)` at 08:54:37Z.
- `tailscale status --json` reports `imac-rozalia` online and active at `100.121.88.110`, with
  current endpoint `5.227.24.249:42772` and handshake `2026-09-14T08:56:10.154899304Z`.
- `tailscale ping --timeout=8s imac-rozalia` returned `pong` via that endpoint in 4 ms.
- Normal SSH and `tailscale ssh` could not verify an SSH host key (`sshHostKeys` is null in the
  coordination status). To verify the already authenticated Tailscale peer without changing the
  durable SSH trust store, a read-only SSH probe used a temporary `UserKnownHostsFile` and
  `StrictHostKeyChecking=accept-new` against the Tailscale IP. It returned `iMac-Rozalia.lan`
  and `up 11 days, 12:06, 2 users`.
- `ip route` still has no `192.168.8.0/24` route; the independent LAN path remains unavailable.
  It is no longer needed to reach the Mac because the Tailscale owner path is working.

The reachable owner/path prerequisite is now satisfied. This is a new, directly measured
`imac-owner-path-recovered` event; no roll-call delta was observed. No routing, DNS, firewall,
VPN, Tailscale, or remote-node configuration was changed. The SSH trust file was confined to
`/tmp/health-imac-20260914.known_hosts`.

Disposition: complete this resolver as cleared and resume the parent with event
`imac-owner-path-recovered`. The parent can now close its unreachable warning using the verified
current path and the separate triage receipt.

Verification: `mesh-dash --once check`; watchdog recovery line in `~/.mesh/chat.log`; filtered
`tailscale status --json`; `tailscale ping`; bounded read-only SSH `hostname; uptime`; and
`ip route`. No substrate mutation was performed.
