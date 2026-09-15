# VPN pane wake prediction — 2026-09-14

Task: `vpn-wake-prediction-20260914/refresh-vpn-wake-prediction`.

## Current state at the consume

- `mesh-dash --once vpn` exited 0 at `2026-09-14T03:22:41Z`. The node has no consumer tunnel by design (`MESH_EGRESS_TUNNEL=off`); phaedra is Online. The cached server sample at `03:20:16Z` says `DEGRADED` only for no WireGuard client handshake in over 24h (`SS:up trojan:up wg:up`, 16 peers, 0 active/idle, 12 stale, 4 never). The end-to-end port-8444 sample passed at `03:19Z`.
- Local `tailscale status --json` at about `03:25Z`: `BackendState=Running`, self Online, phaedra present and Online at `100.94.116.17`. Local route lookup for `1.1.1.1` returned `dev tailscale0 table 52`. These are point-in-time readings; they do not establish client demand or continuous link health.
- The existing prediction had expired (`mesh-wake-expect vpn --show` showed it was written at `00:25:14Z`).

## Prediction and verification

Armed with TTL 300 seconds:

```text
rtk mesh-wake-expect vpn --ttl 300 '^ *phaedra VPN DEGRADED — SS:up trojan:up wg:up \| no WG client handshake in >24h \(all peers idle\?\) \| trojan cert ok \(62d left\);WG 16 peers, newest handshake ;clients: 0 active / 0 idle / 12 stale / 4 never \(16 provisioned\) \(logged [0-9]+m\)$' '^  enrichment cache: [0-9]+m old$' '^  \(0 SS/trojan clients connected right now -- measured, cache [0-9]+m old\)$'
```

`rtk mesh-wake-expect vpn --show` exited 0 and displayed three compiled patterns, written `2026-09-14T03:30:14Z`, expiring at `1789356914` (03:35:14Z). Armed artifact SHA-256: `dfe10094f706bf7036b7e7841da74c7f1c1c2aba69905fcfd9e371540621b396` (`/home/mesh-home/.mesh/wake-expect/vpn`).

A normalized-line check passed all six assertions: the WG log-minute age and the two connection-cache ages match; changing the service verdict, stale-peer count, active-client count, or endpoint result does not match. The pane heartbeat and wall-clock/cache timestamps are already stripped by `mesh-pane-consume` before the prediction gate, so they are not covered as churn here. This leaves actual service, peer/client-count, and endpoint-result changes eligible to wake the mind.

No VPN service, peer, route, firewall, DNS, or WireGuard state was changed. Current client demand/failure remains UNKNOWN; stale WG handshakes alone do not prove an active client failure.
