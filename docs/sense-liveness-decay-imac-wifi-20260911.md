# Sense liveness: decayed `mesh-imac-wifi` — 2026-09-11

`mesh-reflex-health` identified `imac-wifi` as a scheduled dark organ: its `*/2` cron reflex was
running, but the last real iMac Wi-Fi sample was 2026-08-31. The source's smoke test remained green
because its honest negative control accepts an unreachable iMac with exit 2; this is not a fresh
airport reading.

Evidence before decay:

- `mesh-imac-wifi --test`: smoke-green via honest unreachable path (`rc=0` for the test suite).
- `mesh-imac-wifi --edge`: `iMac unreachable (no TCP:22 on 192.168.8.214)` (`rc=2`).
- `~/.mesh/wifi-imac.log`: last real airport-derived sample `2026-08-31T16:04:01Z`.
- `~/.mesh/.imac-wifi-state`: `UNREACHABLE`; the scheduled writer was only refreshing a dark token.
- `mesh-reflex-health --check`: reported `imac-wifi value-frozen` beyond its freshness bound.

Action: marked the source `DECAYED` with `orphan-ok`, set `reflex-cadence: off`, removed its health
watch entry, and used `mesh-reflexes --apply` to deactivate the live cron line under a named
`DECLINED-BY-HEADER` tombstone. No data was deleted.

Afterward:

- `mesh-reflex-health --check`: PASS, 35 fresh per-run reflexes; `imac-wifi` no longer appears as a
  live stale organ.
- Fresh independent real artifact: `mesh-pty-count --json` at `2026-09-11T03:18:43Z`,
  `pty_count=37`, `rc=0`.
- The decayed iMac organ remains honestly unreachable and is not claimed live.

No commit was made.
