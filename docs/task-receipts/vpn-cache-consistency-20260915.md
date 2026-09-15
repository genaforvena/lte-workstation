# VPN cached-source consistency audit — 2026-09-15

Captured 2026-09-15T20:52:23Z–20:56:13Z UTC. This was read-only; no service,
route, DNS, firewall, WireGuard, or exit-node state was changed.

## Evidence

| source | observation | freshness at 20:56:13Z |
|---|---|---|
| `mesh-dash --once vpn` | local consumer tunnel intentionally off; `phaedra` Online; cached port 8444 PASS; cached server verdict DEGRADED with 0 active/idle, 12 stale, 4 never | pane refresh at 20:52:23Z |
| `~/.mesh/vpn-health.log` | mtime 20:50:15Z; last row 20:50:15Z: SS/trojan/WG up, no WG handshake >24h, 12 stale/4 never | 5m58s |
| `~/.mesh/ss-test.log` | mtime 20:49:11Z; last row 20:49:11Z: port 8444 PASS, egress `38.49.216.141` | 7m02s |
| `~/.mesh/vpn-roster.json` | mtime 20:50:15Z; 16 provisioned peer roster used by the pane | 5m58s |
| `~/.mesh/ss-connections.log` | mtime 11:43:06Z; last row is `[ss-connections] recovered — phaedra reachable again`, preceded by unattributed no-reading failures | 9h13m07s |
| `~/.mesh/.ss-clients.cache` | mtime 20:54:04Z; pane reports enrichment cache 13m old and 0 measured SS/trojan clients | 2m09s |

Hashes at capture:

```text
e3a343d114d1fabe5f2d57accf9b9374285a27c60d06d2165e3bc1bc9d991eb5  vpn-health.log
5c27b1ed71d155201af49aaf9eb908652af0bb960313f4249c368db23d4d35bb  ss-test.log
a26c7f3a26c13941683c1d527f018afa56c5c603f6cb70e3dca6c7b09d896c83  ss-connections.log
5331e3d0c8c850ed818d74d40b50ef03e621a69a04136bc2185d7110f65951bd  vpn-roster.json
837f17c17141304b154d9f8600c2cd38004756671d7f9c50a6c01f3eee832f90  .ss-clients.cache
```

## Verdict

**INCONSISTENT freshness, not a VPN outage.** The current health, roster, and
end-to-end tunnel sources agree on a live/pass tunnel with stale WireGuard peer
activity. The connections log is materially old and cannot support a current
client verdict; its historical recovery line must not be read as a fresh sample.
This audit names cache age only. It does not prove WireGuard client demand or a
far-end client failure.

## Commands and exit codes

* `mesh-dash --once vpn`: 0.
* `stat` on five cache artifacts: 0 for each existing file.
* `tail`/source excerpt reads: 0.
* `sha256sum` on five artifacts: 0.

