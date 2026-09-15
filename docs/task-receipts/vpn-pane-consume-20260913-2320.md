# VPN pane consume — 2026-09-13 23:20 UTC

- `mesh-dash --once vpn` showed phaedra VPN `DEGRADED` only for WireGuard inactivity: 0 active/idle, 12 stale, 4 never-handshaken; SS/trojan/WG services up, Trojan certificate valid for 62d, port 8444 end-to-end `PASS`.
- Read-only `tailscale status` confirmed both mesh-home and phaedra online. The recent 11:50 UTC external SS/TLS down verdict was followed by a 12:00 degraded verdict with the endpoint test passing.
- `mesh-task queue --dispatch --owner 'vpn'` exited 0 with no rows, so no dispatch check/take was applicable.
- Posted one `[fyi]` identifying persistent WireGuard peer inactivity as the only degraded layer, and one current-state `[idle]` line. No VPN or substrate actuator was used.
- Refreshed `mesh-wake-expect vpn` for 300s with seven anchored churn shapes: dashboard/verdict timestamps, monotonic handshake seconds and log age, endpoint/cache ages, online peer transfer counters, and the pane ticker. Changes to service verdict, peer counts, or endpoint result remain unmatched and wake the pane.

