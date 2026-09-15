# Router thermal sense liveness — 2026-09-14

Disposition: the **temperature axis** is honestly decayed on `mesh-home`; the reflex remains
scheduled because its independent gateway-reachability branch is still useful. The router is
currently unreachable from the LAN, so there is no defensible thermal value.

## Bounded evidence

Windows are UTC and end at `2026-09-14T07:55:40Z`. Attempt counts come from timestamped `CRON CMD`
records in retained `/var/log/syslog` and `/var/log/syslog.1`; cadence is one attempt per 15 minutes.

| Window | Nominal slots | Timestamped launches | Missing launch records | Numeric thermal reads | Fresh numeric artifact coverage |
|---|---:|---:|---:|---:|---:|
| `2026-09-13T07:55:40Z`–`2026-09-14T07:55:40Z` (24h) | 96 | 81 | 15 | 0 | 0/81 |
| `2026-09-07T07:55:40Z`–`2026-09-14T07:55:40Z` (7d) | 672 | 633 | 39 | 0 | 0/633 |

The state artifact `~/.mesh/.router-thermal-state` contained `unreachable-down` and reflex health
reported the content frozen for `1,170,199` wallclock seconds at `08:03Z`, predating both windows.
Every successful scheduled numeric read writes `cool` or `hot`, so that unchanged value is evidence
of no successful numeric reads during either window. The log `~/.mesh/router-watch.log` has 3,678
lines and 1,426 instances of the current gateway-unreachable message, but its lines have no
timestamps. Therefore per-window counts of empty results versus SSH/path failures, and an exact
windowed total of failed attempts, are **UNKNOWN**. There are also 15 and 39 nominal schedule slots
without a retained CRON record; their cause is **UNKNOWN**, not assumed power-off or success.

The historical log and state do not contain a numeric temperature artifact. The latest direct
`mesh-router-watch --status` probe at `2026-09-14T08:03Z` returned:

> router temp unreadable AND default gateway unreachable on LAN — gateway may be DOWN (LAN+egress at risk)

It refreshed `~/.mesh/.router-thermal-state` at `2026-09-14 08:03:17 UTC` with `unreachable-down`.
This is a fresh real reachability result, **not** a temperature measurement.

## Full organ probe

`mesh-sensorium` completed at `2026-09-14T08:05Z`: local CPU/NVMe/GPU thermals and audio devices
were readable; no Bluetooth adapter was present; WiFi scan returned 0 APs; GL-MT3000 was offline
(configured off-tailnet fallback unanswered), as were the remote Redmi 10 and several other nodes.
This corroborates the router-probe gap while showing that local thermal/audio organs were live.

## Verification and limits

- `mesh-router-watch --test`: exit 0; fixture suite covers dependency gating, parsing, blind streak,
  recovery, deduplication, fault classes, and blind wording. It does not establish live temperature.
- `mesh-reflex-health --check`: exit 0; reports 36 per-run reflexes fresh and continues to flag
  `router-watch(value-frozen …, label axis)`. The scheduled watcher remains live.
- Live `mesh-router-watch --status`: exit 0 with the gateway-unreachable result above; no temperature
  was fabricated.
- The comment in `scripts/mesh-router-watch` records this axis-only decay. Restore thermal coverage
  only after a real numeric read lands; the current network warning remains active.

The attempt evidence is limited to retained syslog and the watcher’s untimestamped output log; exact
historical empty/unreachable subtype counts cannot be recovered from those sources.
