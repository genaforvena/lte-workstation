# VPN peer activity diagnosis — 2026-09-12

Task: `vpn-peer-activity-diagnosis-20260912/read-only-peer-activity-diagnosis`.

## Verdict

The changed layer is WireGuard peer handshake freshness on `phaedra`: the server interface and UDP listener are up, but no provisioned peer has handshaken within the last hour and the newest handshake is about 13.46 days old. This supports the dashboard's stale-peer signal. It does **not** establish a server outage: the evidence cannot distinguish expected client inactivity from clients attempting and failing to connect. Classify the peer-use question as **IDLE / UNPROVEN**, not `DOWN`.

The other observed paths were healthy during this check. `phaedra`'s Shadowsocks and trojan processes/listeners were up; the VPN pane's cached end-to-end SS fetch passed and reported egress `38.49.216.141`. On this node, Tailscale reported `BackendState=Running`, self Online, and `phaedra` Online; a live public fetch returned the same egress address. No restart, peer edit, or network change was made.

## Evidence

- `mesh-dash --once vpn` at `2026-09-12T18:11:25Z`: no consumer tunnel here by design (`MESH_EGRESS_TUNNEL=off`); four Tailscale machines Online; `phaedra` Online; `mesh-vpn-health` at `18:10:14Z` reported `SS:up trojan:up wg:up`, 16 WireGuard peers, newest handshake age `1,162,954s`, 12 stale and 4 never; cached end-to-end SS test passed with egress `38.49.216.141`.
- Local vantage at `2026-09-12T18:16:53Z`: `tailscale status --json` returned `Running`, `Self.Online=true`, `phaedra.Online=true`. `curl -4 --max-time 8 -fsS https://api.ipify.org` returned `38.49.216.141`. The node booted at `2026-09-12 08:42:31`; this proves current reachability, not continuous uplink continuity since boot (that age remains unknown).
- Read-only SSH to `phaedra` at `2026-09-12T18:17:00Z`: `ss-server` and `trojan` processes up; `wg0` interface up; TCP listeners present on 443 and 8443; two UDP listener rows matched 51820; `wg-quick@wg0` active; egress fetch returned `38.49.216.141`.
- `sudo -n wg show wg0 latest-handshakes` summary at `18:17:00Z`: 16 peers, 4 with no handshake, 12 with a historical handshake, 0 with a handshake under 3600s, newest handshake age `1,163,365s` (13d 11h 9m), oldest `7,530,882s`. The repeated read at `18:15:47Z` agreed on peer counts and freshness. `wg show wg0 transfer` showed nonzero cumulative counters on 12 peers; these are lifetime totals, not evidence of current traffic.

## Limits and disposition

The successful SS fetch validates that client-facing path at the time of the cached check; it does not validate WireGuard client traffic. The local public fetch and Tailscale netmap checks prove the local vantage and reachability to `phaedra`, while continuous uplink age since boot is unavailable. No active WireGuard client was observed, so no far-end client fault can be named. Keep this diagnostic read-only; collect a client-side attempt only if a user reports an active WG failure. No one-line repair is justified by idle peer freshness alone.
