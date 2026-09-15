# VPN WireGuard stale-peer follow-up — 2026-09-12

Task: `vpn-wg-peer-staleness-20260912/diagnose-wg-peer-staleness`.

## Verdict

At 22:19 UTC the changed layer remains WireGuard peer handshake freshness on `phaedra`. The local
Tailscale backend is `Running`, `phaedra` is present and `Online`, and local egress was `OK` one
minute before the remote read. After those local-side checks, a redacted read-only SSH query found
`wg-quick@wg0` active, 16 provisioned peers, 4 with no handshake, 0 handshakes within one hour, and
the newest handshake 1,177,915 seconds (13 days, 14 hours) old. The cached end-to-end Shadowsocks
probe still passes. This does not establish a WireGuard server outage or a client-side failure:
current client attempts are not observed, so peer use remains **IDLE / UNPROVEN**. No network,
service, routing, or peer state was changed.

This is a freshness follow-up to the completed `docs/vpn-peer-activity-diagnosis-20260912.md`
(SHA-256 `a97dad8d4fc0960e6f471759c2d60b31f3de0dcd842aa6a8a47a6108f18f6875`), not a new repair
claim. The earlier direct read at 18:17 UTC also found 0/16 peers fresh within one hour and the
same healthy service path. The new read confirms that the verdict persisted for another four hours.

## Evidence

- `mesh-dash --once vpn` at `2026-09-12T22:16:04Z`: consumer tunnel on this node is disabled by
  design; `phaedra` is Online; the latest server-health cache at `22:10:10Z` says `SS:up
  trojan:up wg:up`, 16 peers, newest handshake age `1,177,352s`, with 12 stale and 4 never; the
  end-to-end SS result at `22:09:11Z` is PASS via `38.49.216.141`.
- Local-side prerequisite at `2026-09-12T22:18:33Z`: `tailscale status --json` returned
  `BackendState=Running`, self `mesh-home`, and peer `phaedra` Online at `100.94.116.17`.
  `systemctl is-active tailscaled` returned `active`. `/proc/uptime` was `48962.26s`; this does
  **not** establish continuous uplink age since boot, which remains UNKNOWN. The local
  `egress-health.log` sample at `22:18:01Z` says `OK`, egress IP `38.49.216.141`, path `route`.
- Only after the local-side prerequisite, read-only command:
  `ssh -o BatchMode=yes -o ConnectTimeout=8 phaedra 'sudo -n wg show wg0 latest-handshakes; systemctl is-active wg-quick@wg0; date -u +%Y-%m-%dT%H:%M:%SZ'`.
  Output was captured and peer public keys were withheld from the receipt. SSH exit `0`, stderr
  empty; remote time `2026-09-12T22:19:30Z`; `wg-quick@wg0=active`; `16` peers, `4` never,
  `0` under one hour, newest handshake age `1,177,915s`.
- Source line SHA-256 values (the last row of each cached file): `vpn-health.log`
  `c41b6a31399350abd192abe6715cb44632322f42e737cef078e51c165a846e74`;
  `ss-test.log` `4160082c17453a2f3a66075bfdcd04eb2c13064bd8be9fbf0f5ca993a5724215`;
  `egress-health.log` `0f41affecde7fdbbcf6e37bb43de2e43a3cc9025cc38c82d719432366dae3279`.
  SHA-256 of the redacted remote summary (`BackendState=Running; Phaedra=Online; uptime_s=48962.26;
  remote=2026-09-12T22:19:30Z; wg=active; peers=16; never=4; under1h=0; newest_age_s=1177915`):
  `bd3cf39d0a9116fe0d4cef5822fedabae918a6266a632b71c5a5daa8d4fb5870`.

## Disposition

There is no evidence for an idempotent remedy: all observed WireGuard peers are idle or stale,
with no client attempt to diagnose. The existing VPN service/reflex path is healthy for SS, and
the local side is reachable, so no re-applier or actuator is warranted from this evidence. Keep the
verdict UNKNOWN about client demand; obtain client-side evidence only if an active WireGuard failure
is reported. No substrate change was made.
