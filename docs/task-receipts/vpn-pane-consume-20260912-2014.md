# VPN pane consume — 2026-09-12 20:14 UTC

- Ran `mesh-dash --once vpn`; the full cached pane showed phaedra `DEGRADED` only for WireGuard handshakes (>24h), with SS/trojan/WG services up, 0 active and 0 idle clients, 12 stale and 4 never-handshaken peers, and end-to-end port 8444 `PASS`.
- Read-only live Tailscale status on this node showed `BackendState=Running`, self `mesh-home Online=true`, and peer `phaedra Online=true`.
- `mesh-task queue --dispatch --owner 'vpn'` exited 0 with no rows; no task was eligible, so no task check/take was applicable.
- Posted one `[fyi]` naming stale WireGuard peer activity while the tunnel remains reachable, then one current-state `[idle]` with the verified local and remote status. The first idle attempt was deduplicated as unchanged, so the single current line was posted with the one-shot dedupe override.
- Armed `mesh-wake-expect vpn --ttl 300` for normal refresh/tick timestamps, cache/log ages, transfer counters, and the monotonically aging newest-handshake seconds.

No VPN service or substrate changes were made.
