# VPN watchdog peer-restoration reconciliation — 2026-09-13

Task: `vpn-watchdog-peer-restoration-reconcile-20260913/reconcile-peer-restoration-evidence`.

## Verdict

The 00:18 watchdog event and the later stale-handshake verdict are compatible. The watchdog
reconciled 16 configured peer entries onto phaedra's live WireGuard interface; its “16 live peers”
means entries returned by `wg show wg0 peers`, not clients with fresh handshakes. At 01:22 UTC the
WireGuard service was active, all 16 entries were present, and none had a handshake within 24h.
The newest handshake was 1,188,897 seconds old. The current 01:20 health row reported the same
state within 146 seconds of age progression. The moved layer is runtime peer-entry restoration;
client activity remains IDLE / UNPROVEN. No VPN actuator or substrate change was made by this
diagnosis.

## Evidence and order

- Local-side proof first, at `2026-09-13T01:21:45Z`: `tailscale status --json` parsed to
  `BackendState=Running`, self `mesh-home`, and peer `phaedra Online=True IP=100.94.116.17`;
  `systemctl is-active tailscaled` returned `active`. `/proc/uptime` reported `59953.87s` since
  boot. The latest local egress-health row, timestamped `01:21:01Z`, was `QUALITY OK` with 0% loss.
  Continuous uplink age since boot is UNKNOWN; this point sample does not prove continuity.
- Cached pane at `01:17:35Z` reported the 01:10 health row as DEGRADED and the 01:09 port-8444
  fetch as PASS. Fresh cache rows at `01:22:02Z` were:
  `2026-09-13T01:20:14Z` health — SS/trojan/WG up, 16 peers, newest handshake 1,188,751s,
  0 active/idle, 12 stale, 4 never; and `2026-09-13T01:19:10Z` port 8444 PASS.
- Board source `~/.mesh/chat.log:58553` at `00:18:05Z` said
  `RESTORED friend-VPN peers — live:clients-friend1 (was a silent drop; now 16 live peers)`.
  Source `scripts/mesh-vpn-watchdog` lines 90–134 confirms it tests for a peer missing from the
  live interface, runs `wg syncconf`, then labels `wg show "$WG_IF" peers | wc -l` as “live
  peers.” This is presence on the interface, not proof of client traffic or handshakes.
- Only after the local proof, read-only off-tailnet query:
  `ssh -o BatchMode=yes -o ConnectTimeout=8 phaedra-direct 'sudo -n bash -s'` with the script
  `systemctl is-active wg-quick@wg0; wg show wg0 latest-handshakes` summarized by age; and
  `wg show wg0 transfer` summarized without peer keys. Exit `0`, remote time `01:22:32Z`,
  `wg_service=active`, `peers=16 never=4 under1h=0 under24h=0 newest_age_s=1188897`.
  Lifetime transfer totals were sampled once only and are not treated as evidence of current use.

## Provenance

- `vpn-health.log` SHA-256: `068a91aa5f545fe8d3d5056da5229f99a39162a262f752b6593f1fa00272b6e6`.
- `ss-test.log` SHA-256: `20d092979c8909b82bae63b4965b3a88455a7554f14b1742f90ca8e41a7df9c8`.
- `scripts/mesh-vpn-watchdog` SHA-256: `d007b26566a585572a221d94ee6e854b20f58fe199f46cddb5fa44dc53dc6545`.
- Board event line (`chat.log:58553`) SHA-256: `21e6ff6fd3e91b100f16fa456ae542126094d9777e38f35703ee9fee49890fce`.
- Redacted remote summary SHA-256: `d2258e8e428706b844a2d3fcff387836f82cacc4cd455d59603dc3e91cecfc3e`.

## Limits and disposition

Local tailnet visibility and local egress were healthy at the sample times; uplink continuity since
boot remains UNKNOWN. The direct remote read independently confirms the server's WG service and
peer-entry presence, while handshake telemetry shows no recent client connection. The cumulative
transfer totals have no before/after delta, so they do not establish active traffic. No client-side
attempt is observed, so no client fault is claimed. The existing watchdog is the idempotent
re-applier for missing runtime peer entries; no new remedy is indicated. Do not restart a working
VPN or alter peers, routes, DNS, firewall, or service state from this evidence.
