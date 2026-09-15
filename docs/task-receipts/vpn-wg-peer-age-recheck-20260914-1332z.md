# VPN WireGuard peer-age recheck — 2026-09-14

Task: `vpn-wg-recheck-20260914-1332/recheck-current-wg-freshness`.

## Result

The degraded layer remains WireGuard peer freshness. A fresh, read-only phaedra query found
`wg-quick@wg0` active and 16 configured peers: 0 handshakes under one hour, 0 between one and 24
hours, 12 older than 24 hours, and 4 with no handshake. The newest handshake was 1,319,545 seconds
old at 13:40:00Z. This agrees with the 13:20 health row's same bucket counts and 1,318,353-second
age; the newest handshake has not resumed. The 08:30 direct read recorded 1,300,972 seconds, so
the age increase to 13:40 tracks elapsed wall time within one second.

Local transport was proven before the remote query: Tailscale was Running, this node and phaedra
were Online, `tailscaled` was active, and a fresh public fetch returned `38.49.216.141`. The pane's
13:29:36Z sample also had the 8444 end-to-end probe passing. Client demand or a client-side failed
attempt remains unproven. No service, configuration, route, or peer state was changed.

## Ordered evidence and commands

- `2026-09-14T13:29:36Z` — `mesh-dash --once vpn` rendered the full stream. The latest server row
  was `13:20:21Z`: SS/trojan/WG up, WireGuard degraded on stale handshakes, 0 active / 0 idle /
  12 stale / 4 never, newest age `1318353s`; port 8444 passed at `13:29:10Z`.
- `2026-09-14T13:38:59Z` — local-side preflight:

  ```text
  timeout 15 tailscale status --json | jq -r '"backend=\(.BackendState // "na") self_online=\(.Self.Online // false) self_ip=\(.Self.TailscaleIPs[0] // "na") phaedra_online=\([.Peer[]? | select(.HostName == "phaedra") | .Online][0] // "missing") phaedra_ip=\([.Peer[]? | select(.HostName == "phaedra") | .TailscaleIPs[0]][0] // "missing")"'
  backend=Running self_online=true self_ip=100.81.222.19 phaedra_online=true phaedra_ip=100.94.116.17
  systemctl is-active tailscaled
  active
  awk '{print $1}' /proc/uptime
  93799.14
  curl -fsS --max-time 8 https://api.ipify.org
  38.49.216.141
  ```

- `2026-09-14T13:39:59Z` local start / `2026-09-14T13:40:00Z` remote sample — after the
  preflight passed, a read-only SSH command ran on phaedra:

  ```sh
  ssh -o BatchMode=yes -o ConnectTimeout=8 phaedra \
    "printf 'remote_utc='; date -u +%Y-%m-%dT%H:%M:%SZ; printf 'remote_epoch='; date +%s; printf 'wg_service='; systemctl is-active wg-quick@wg0; wg show wg0 latest-handshakes"
  ```

  A local Python aggregator discarded all public-key fields and retained only the timestamp,
  service state, peer count, age buckets, and newest age:

  ```text
  local_started=2026-09-14T13:39:59+00:00
  remote_utc=2026-09-14T13:40:00Z wg_service=active peers=16 fresh_lt1h=0 idle_1h_24h=0 stale_gt24h=12 never=4 newest_age_s=1319545
  peer_public_keys=not-retained
  ```

The sanitized remote summary SHA-256 is
`15655b460c1110b931aacb27455beb97ad4acb5fcfee653fcad5e2ba07ac729c`. The final receipt SHA-256
is recorded as `artifact_sha256` in the task ledger when this step is closed.

## Classification

This is a continuing WireGuard peer-freshness condition, not evidence of a failed service or
client-side access failure. Preserve the read-only diagnosis; do not restart WireGuard or edit
peers/routes without measured evidence of an active client failure.
