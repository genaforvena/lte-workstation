# senses Wi-Fi cross-vantage live probe — 2026-09-16

Task: `senses-wifi-crossval-live-20260916/restore-live-wifi-crossval`

## Result

The producer cadence is live, but the local radio is hollow for this cycle. No synthetic
AP data was written. Cross-vantage remains UNKNOWN/partial because the local vantage has no
fresh sane union artifact.

## Evidence

- `mesh-wifiscan --test` at 2026-09-16T10:12Z: exit 1; `live iw read yielded 0 AP(s)`.
- `mesh-wifi-crossval` at 2026-09-16T10:12Z: exit 2; local vantage past the 1800s TTL.
- `/home/mesh-home/.mesh/wifiscan.log` was modified 2026-09-16 09:37 UTC and its latest
  scheduled attempts at 08:06–09:36 UTC all reported 0 APs and honest stale-cache misses.
- `/home/mesh-home/.mesh/.wifiscan-union` remains from 2026-08-30 07:36 UTC; it was not
  refreshed, correctly.
- `/home/mesh-home/.mesh/wifi-crossval.state` remains a cached state from 2026-09-16 08:23 UTC;
  the live command refused to treat it as current.

## Delegation record

Delegated a non-overlapping read-only cadence audit to `senses-wifi-cadence-audit` through the
Codex session relay. The worker accepted the prompt but produced no report before the relay
stalled; it was stopped. I personally inspected the producer tape, union/state mtimes, and the
captured test outputs in `/tmp/senses-wifiscan-test.out` and `/tmp/senses-wifi-crossval.out`.

## Retry edge

At the next live radio opportunity, rerun `timeout 100 mesh-wifiscan --test`; only a sane real
scan may refresh `.wifiscan-union`, then rerun `mesh-wifi-crossval`. Until then the cross-vantage
verdict must stay UNKNOWN/partial.
