# VPN WireGuard freshness check — 2026-09-14

Task: `vpn-wg-zero-handshake-diagnosis-20260914/diagnose-wg-population`.

## Verdict

The fresh read-only health probe again localizes `DEGRADED` to WireGuard peer freshness. At
19:37:50Z, Shadowsocks, Trojan, and `wg0` were up; the expected egress was observed; the newest
WG handshake was 1,341,014 seconds old (about 15.5 days), with 0 active, 0 idle, 12 stale, and
4 never-used peers. No evidence here establishes a client access failure. Do not restart services
or edit peers/routes.

This is a new timestamped observation of a condition already checked at 08:30Z, not a new repair
claim. The morning receipt recorded newest handshake age 1,300,972 seconds; the increase is
40,042 seconds, with no newly observed handshake.

## Evidence

- `mesh-dash --once vpn` at 19:33:02Z: this node has no consumer tunnel by design; the cached
  end-to-end Shadowsocks probe passed on port 8444; the cached server row showed SS/Trojan/WG up,
  16 peers, 0 active/idle, 12 stale, 4 never, and newest handshake age 1,340,550 seconds.
- `tailscale status --json` at about 19:35:57Z: `BackendState=Running`, mesh-home online, phaedra
  present and online. A point-in-time peer record showed `Relay=tor` and `CurAddr=38.49.216.141:41641`.
- `tailscale ping --c 1 --timeout 3s 100.94.116.17` then succeeded: `pong from phaedra` via
  `38.49.216.141:41641` in 139 ms. The peer transport answered; the earlier relay field and this
  later reachable endpoint are observations at different instants, not evidence of a sustained
  Tailscale outage.
- `mesh-vpn-health --json` at 19:37:50Z completed with exit 0 and returned `DEGRADED`, `ss=up`,
  `trojan=up`, `wg=up`, egress `38.49.216.141`, WG age `1341014`, and `0 active / 0 idle / 12
  stale / 4 never (16 provisioned)`. Trojan certificate had 61 days remaining. The probe refreshed
  `~/.mesh/vpn-health.log` and the roster cache; it did not use `--edge` and made no board verdict
  transition.
- Local link proof: boot time `2026-09-13 11:35:40 UTC`; `/proc/uptime` was `115352.84` seconds.
  `enp42s0` was online/routable with carrier `1`; carrier counters were 2 changes, 1 up, 1 down.
  Kernel log records its initial `Link is Down` at 11:35:51Z and `Link is Up` at 11:35:55Z, with no
  later carrier transition in this boot. This supports link presence since boot initialization,
  though DHCP renewed/replaced the address and gateway roughly every ten minutes in the sampled
  networkd log. The latest renewal completed at 19:36:30Z; the subsequent VPN probe and Tailscale
  ping succeeded.
- `mesh-usb --age` found no USB network interface; the active uplink is Ethernet, so USB age is
  inapplicable. No service, route, peer, or VPN configuration was changed.

## Disposition

Name the moved layer as WG peer freshness/activity. The server paths and the sampled end-to-end
tunnel are serving; whether friends currently need WG access is unknown. Continue observing through
the existing health reflex. There is no evidence for a one-line repair, and no actuation is
justified.
