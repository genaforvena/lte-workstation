# VPN pane cache-source audit — 2026-09-13

Task: `vpn-pane-cache-source-audit-20260913/audit-current-vpn-pane-cache-provenance`

## Capture and verdict

Read-only pane capture: `rtk mesh-dash --once vpn`, exit 0, refresh timestamp `2026-09-13T14:42:37Z` (pane finished at `14:42:43Z`). At capture, phaedra's cached server verdict was **DEGRADED**: SS/Trojan/WG services reported up, but no WG client handshake for more than 24 hours; 12 peers stale, 4 never seen, none active/idle. The latest cached end-to-end SS test passed on port 8444. This is a current verdict for the health sample written at 14:40, not evidence that clients are using WG now.

## Source map and freshness

| Pane section | Source and producer | Evidence at audit | Interpretation |
|---|---|---|---|
| My egress | `mesh-egress-tunnel` invoked by `scripts/mesh-dash`; this node has `MESH_EGRESS_TUNNEL=off` | Pane said `n/a ... BY DESIGN` | Configuration/local egress context, not the phaedra server verdict. The helper is invoked each render; no state change was requested. |
| Connected machines | `tailscale status --json` read locally by the pane | Pane returned 4 online / 9 offline at 14:42 | Live local-daemon view, not a cached reflex artifact. It does not alone prove phaedra's VPN service health. |
| Server health and WG summary | Tail of `~/.mesh/vpn-health.log`, produced by `mesh-vpn-health --edge` | Source mtime `14:40:13Z`; pane age `2m`; health verdict DEGRADED and newest handshake age `1,236,753s` | Fresh cached server-side sample relative to this capture. No claim about client demand follows from stale handshakes alone. |
| Tunnel end-to-end | Tail of `~/.mesh/ss-test.log`, produced by `mesh-ss-test --edge` | Source mtime `14:39:11Z`; pane age `3m`; PASS, port 8444, egress `38.49.216.141` | Fresh cached end-to-end sample relative to this capture. |
| SS client enrichment | `~/.mesh/.ss-clients.cache`, written by `mesh-ss-clients` | Source mtime `14:39:03Z`; pane age `3m` | The displayed zero-client reading is fresh for this cache sample. |
| SS connection summary | Tail of `~/.mesh/ss-connections.log`, producer `mesh-ss-connections --edge` | Source mtime `2026-09-09 07:28:03Z`; pane showed “no active SS connections” without an age | **Stale history, not a current client census.** `scripts/mesh-dash` omits this log's age. The reflex is listed in `~/.mesh/reflexes.cron` at `13-59/15 * * * *`, but the artifact mtime is four days old; whether the scheduled job is unloaded or failing was not tested here. |
| WG names | `~/.mesh/vpn-roster.json`, written by `mesh-vpn-health` | Source mtime `14:40:13Z`; pane age `2m`; 16/16 named | Fresh mapping of the cached peer states to names. |
| Escalation gate | `mesh-ss-escalate` reads the last eight unknown-client entries in `ss-connections.log` and `.ss-escalation-posted.state`; may classify a newly added IP using cached class data or network lookups | Pane showed `SUPPRESS` and seven IPs; `.ss-escalation-posted.state` mtime Aug 12, `.ss-ip-class.cache` mtime Aug 11; the source connection log is stale as above | This result is not evidence of current clients. The helper is executed during rendering and can perform lookups for a newly added IP; its output is not a pure file-tail read. Its state/cache mtimes did not change during this audit. |
| Verdict changes | Last three `[vpn-down|degraded|ok|blind]` entries from `~/.mesh/chat.log` | Chat log mtime `14:42:46Z`; shown transition timestamps ended at 12:00Z | Historical board transitions, not a second live health probe. |

The pane's overall `refresh`/`pane live` timestamps are render times and can change without any source verdict moving. Tailscale peer traffic counters and last-seen ages can also change independently of the cached phaedra health sample.

## Commands and source identity

Read-only commands used: `rtk mesh-dash --once vpn`; `rtk sed -n '2840,3060p' scripts/mesh-dash`; `rtk sed -n '1,110p' /home/mesh-home/.local/bin/mesh-ss-test`; `rtk sed -n '1,160p' /home/mesh-home/.local/bin/mesh-ss-escalate`; `rtk sed -n '330,390p' /home/mesh-home/.local/bin/mesh-ss-connections`; `rtk sed -n '92,113p' ~/.mesh/reflexes.cron`; and `rtk stat`/`rtk sha256sum` on source and cache files. No service, route, DNS, firewall, or WireGuard change was made; no VPN probe was run as part of this audit.

Source hashes at audit:

```text
c25a421e259cb157d31b7234153c12c826087b6d9cf16080e55819ad4052c7a2  scripts/mesh-dash
1458900854b2d74c263252908f237f39fad9068be3c737d045691370b5ba1fed  ~/.local/bin/mesh-vpn-health
74d6778c9c550453e8436f8f4f06e287716f53557834ae604051eee84e7e33d0  ~/.local/bin/mesh-ss-test
2d50c7f2452c0cb970949217beb62b7ec2930638927116bd2930ce5f4617aabd  ~/.local/bin/mesh-ss-clients
cfe334a50f24f9c98493d5ec7210cd5c73648247e1b0cd3b1afab31a3580099f  ~/.local/bin/mesh-ss-connections
54f51f2b771cf56556697c1c26f2c9c02895f42451a1999fe07ebd17f9317efe  ~/.local/bin/mesh-ss-escalate
22603aa3a1a306457211e779f47a6df864c1ce4b6e23f260912b72ed39f36664  ~/.local/bin/mesh-egress-tunnel
```

## Bounded conclusion

The current **server/tunnel verdict is DEGRADED with a recent successful SS end-to-end sample and persistently stale WG peer handshakes**. The layer that changed in this capture is not established; the log supports WG peer inactivity, while whether clients are idle remains unknown. Separately, the SS connection-summary and escalation inputs are at least four days old, so their present-tense pane wording overstates freshness. A safe follow-up is to make that section age-aware and recover/verify its scheduled writer; this audit did not run the producer or repair its schedule.
