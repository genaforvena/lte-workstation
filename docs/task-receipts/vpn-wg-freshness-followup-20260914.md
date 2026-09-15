# VPN WireGuard freshness follow-up — 2026-09-14

Task: `vpn-wg-freshness-followup-20260914/verify-current-peer-freshness`.

## Verdict

At 08:30 UTC, phaedra's WireGuard service was active and the 16-peer roster still had no
handshake within 24 hours: 12 peers were stale and 4 had never handshaken. The newest nonzero
handshake was 1,300,972 seconds old (about 15.1 days), matching the cached 08:20 health row
(1,300,351 seconds). The changed layer remains peer freshness/activity. The end-to-end Shadowsocks
probe passed, and this evidence contains no client-side failed attempt; client demand/failure is
still unproven. No service, configuration, route, or peer state was changed.

## Ordered evidence

- `2026-09-14T08:29:49Z`: `tailscale status --json` reported `BackendState=Running`, this node
  online, and `phaedra` online at `38.49.216.141:41641`.
- `2026-09-14T08:29:49Z`: `systemctl is-active tailscaled` returned `active`; `/proc/uptime`
  reported `75249.01` seconds. This does not prove uninterrupted uplink since boot.
- Egress log at `2026-09-14T08:27:01Z`: `OK`, public egress `38.49.216.141`, path `route`,
  `loss=0%`.
- Only after those local-side checks, a read-only SSH query to `phaedra` at `2026-09-14T08:30:26Z`
  returned `wg-quick@wg0=active`, `peers=16`, `active_lt1h=0`, `idle_1h_to_24h=0`,
  `stale_gt24h=12`, `never=4`, `newest_nonzero_age_s=1300972`. Public keys were not retained.
- The contemporaneous `mesh-dash --once vpn` stream at `08:26:54Z` reported SS/trojan/WG up,
  newest handshake age `1300351s`, and the end-to-end SS probe passing. Its age agrees with the
  direct read after allowing for the four-minute interval.
- The completed 2026-09-13 freshness receipt found the same 0 fresh / 12 stale / 4 never
  classification. No peer has resumed a handshake since that check.

## Disposition

The current observation confirms a continuing WireGuard peer-freshness condition, not a
demonstrated client access failure or a failed server process. Preserve the read-only diagnosis;
do not restart the service or edit peers/routes without evidence of an active client failure.
