# VPN corrective receipt — WireGuard peer-age degradation

- Task: `witness-chat-range-review-medium-69531-70002-correctives-vpn/route-wireguard-degradation`
- Observed: `2026-09-16T11:27:42Z`
- Scope: diagnose-only; no VPN, routing, DNS, firewall, or WireGuard actuator was used.

## Fresh evidence

`mesh-vpn-health --edge` exited 0 and reported:

```text
phaedra VPN DEGRADED — SS:up trojan:up wg:up | no WG client handshake in >24h (all peers idle?) | trojan cert ok (59d left);WG 16 peers, newest handshake 1484403s ago;clients: 0 active / 0 idle / 12 stale / 4 never (16 provisioned)
```

`mesh-ss-test --edge` exited 0 with no stdout. The preceding `mesh-dash --once vpn` stream recorded the end-to-end port 8444 tunnel as `PASS` (egress `38.49.216.141`, Montréal, CA), checked five minutes before the consume turn.

## Layer verdict and retry edge

The moved layer is the WireGuard peer-handshake/consumer layer on `phaedra`; the server services and end-to-end tunnel remain up. The local vantage is healthy enough to name the far-end condition because `phaedra` is present and Online in the Tailscale netmap and the local egress tunnel fetch passes.

Retry after the next fresh `mesh-vpn-health --edge` sample or any new WireGuard handshake event. If the tunnel itself changes from PASS, reclassify the layer before any action. No restart is justified by this evidence.
