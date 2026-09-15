# VPN current-state follow-up — 2026-09-13

Task: `vpn-verdict-transition-20260913/reconcile-down-to-degraded-transition`.

## Current verdict

The fresh 12:38–12:46Z observation confirms the earlier health-owned triage remains current:
the brief SS/TLS probe failure from 11:50Z was not reproduced in later health samples, and
the port-8444 end-to-end tunnel fetch continues to pass. Phaedra's current cached verdict is
still DEGRADED solely for stale WireGuard client handshakes: 16 configured peers, 0 active,
0 idle, 12 stale, and 4 never; newest handshake age 1,229,554 seconds at 12:40:13Z. This
does not establish a server outage or an attempted-but-failed client connection.

The original event and its immediate reconciliation are already recorded by health's completed
`health-warning/a6cd61d4957263666c1b/triage` receipt. This follow-up adds only the later
12:38–12:46Z state and local-vantage evidence; it does not reopen that transient-probe episode.

## Evidence

- `mesh-dash --once vpn`, cached pane timestamp 12:38:14Z: this node has no consumer tunnel
  by design (`MESH_EGRESS_TUNNEL=off`); phaedra is listed Online; the 12:30:18Z health row
  is DEGRADED for WireGuard handshake staleness; the port-8444 fetch passed at 12:29:21Z.
- Direct local check at 12:46:25Z: Tailscale `BackendState=Running`, self
  `mesh-home Online=true`, and phaedra `Online=true` at `100.94.116.17`. Local
  `/proc/uptime` was 4245.28 seconds. The 12:42:01Z egress-health rows report egress
  `38.49.216.141` and QUALITY OK. These are point observations; continuous uplink age since
  boot remains UNKNOWN.
- `~/.mesh/vpn-health.log`: 11:50:48Z reported SS :443 and trojan :8443 probe failures;
  11:52:54Z returned to DEGRADED on WG staleness alone; 12:40:13Z remains DEGRADED with
  SS/trojan/WG up, 16 peers, 0 active/idle, 12 stale, 4 never, newest handshake 1,229,554s.
- `~/.mesh/ss-test.log`: port 8444 passed at 11:49:12Z, 11:59:11Z, 12:29:21Z, and
  12:39:23Z, each reporting egress `38.49.216.141`. These periodic samples do not prove
  uninterrupted service between checks and do not probe the same ports as the transient
  :443/:8443 failures.
- The existing completed health triage at
  `docs/task-receipts/health-warning-a6cd61d4957263666c1b-triage-20260913.md` records the
  11:52:54Z unreproduced-probe verdict and the same unresolved WG peer inactivity.

Source digests at observation time:

- `vpn-health.log`: `d7359a9151605406b1edda6436534e10a010decee62115c0e3c1a8367f57ba39`
- `ss-test.log`: `fb5187466b1d28c01b8aeb52d0d12bfd8f1d8020b03cfa462ccc865510c5f154`
- `egress-health.log`: `452779d2e9535b82a1449bc5ab2cdd6f7f1adf398d601db65bf0f31fd4f2f3d8`

## Disposition

No service restart, remote client attribution, peer edit, route, DNS, firewall, or WireGuard
change is justified by these readings. Keep the persistent WG client-activity verdict at
IDLE / UNPROVEN; the cached SS path is passing, while the continuous uplink interval and any
client-side failed attempt remain UNKNOWN.
