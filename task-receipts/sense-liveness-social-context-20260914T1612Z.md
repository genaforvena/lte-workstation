# Sense liveness — social-context on mesh-home — 2026-09-14

Disposition: **decayed on mesh-home while its source axes are dark**. The scheduled fusion was
writing a fresh `DEGRADED` label despite all four input axes being unknown. The all-dark path now
deletes that label, touches `.social-context-offline` on every blind run, and exits 2. The schedule
stays installed as a revival detector.

## Organ probes

- `mesh-reflex-health` initially reported 36 per-run reflexes fresh and
  `social-context(value-frozen …, label axis)`. `mesh-reflex-health --check` after the fix still
  reports 36 fresh per-run reflexes; with the state removed it no longer treats social-context's
  old label as a reading.
- `mesh-sensorium` at `2026-09-14T15:47Z` read CPU/NVMe/GPU temperatures and enumerated audio
  capture/playback devices. It found no Bluetooth adapter and `mesh-wifiscan` found 0 APs.
- `mesh-sense-map --refresh` at `2026-09-14T15:46:35Z` reported 4/11 nodes reachable. Redmi 10,
  the phone endpoint used by the phone-bound axes, was offline (last tailnet sighting 11 days prior).
- Direct `mesh-social-context --json` at `2026-09-14T15:53:54Z` returned
  `DEGRADED`, with `audio=UNKNOWN`, `body=UNKNOWN`, `light=UNKNOWN`, `ble_any=0`,
  `person_count=0`, and `phone_ok=1`. The body command's non-n/a return was being mistaken for
  evidence even though it emitted no recognized body sign.

## Bounded windows

Windows are UTC and end at the timestamp of that direct live probe. Attempt counts are timestamped
`CRON CMD` records from retained `/var/log/syslog` and `/var/log/syslog.1`; the installed cadence is
`2-59/5 * * * *` (288 nominal slots/day).

| Window | Nominal slots | Timestamped launches | Missing launch records | Timestamped social-context rows | Real source reads | Empty/unreachable outcomes | Source-reading artifact coverage |
|---|---:|---:|---:|---:|---|---|---|
| `2026-09-13T15:53:54Z`–`2026-09-14T15:53:54Z` (24h) | 288 | 288 | 0 | 0 | **UNKNOWN** | **UNKNOWN** | 0 source-bearing rows evidenced / 288 launches; actual read rate **UNKNOWN** |
| `2026-09-07T15:53:54Z`–`2026-09-14T15:53:54Z` (7d) | 2,016 | 1,901 | 115 | 2 | **UNKNOWN** | **UNKNOWN** | 0 source-bearing rows evidenced / 1,901 retained launches; actual read rate **UNKNOWN** |

The two dated rows in the 7-day window (`2026-09-10T00:02:01Z` and
`2026-09-11T10:37:01Z`) both say `UNKNOWN — phone unreachable and ble scan failed`. The log has only
55 timestamped rows total: it records confirmed label changes and a first blind diagnostic, not
every attempt. There is no timestamped per-run tape of audio/body/light/BLE values or outcomes, so
the exact number of empty reads versus unreachable reads, and the historical real-read coverage,
cannot be recovered. The 115 missing 7-day `CRON CMD` records are unexplained; they are not assumed
to be power-off. The `.social-context.state` file contains only a label, so its mtime cannot supply
source-read coverage.

## Change and verification

- Added `_has_live_input`: only a recognized audio/body/light value or a successful BLE result
  counts; a command's success status or resolved phone endpoint does not.
- All-dark evaluations now remove the previous `.social-context.state`, touch
  `.social-context-offline`, and exit 2. `--test` reports n/a unless at least one dependency's own
  `--test` completes a live read.
- TDD regression `tests/test-mesh-social-context-all-dark.sh`: observed red before the fix (rc 0,
  emitted `DEGRADED`); green after the fix. Its second assertion also failed before state deletion
  was added, then passed after that change.
- `scripts/mesh-social-context --test` now reports `n/a (every sensor --test reports
  absent/unreadable; no live input to assert)` on this node.
- Post-fix direct probe returned exit 2. Its blind marker was refreshed by the scheduled invocation
  at `2026-09-14T16:12:01.771Z`; marker mtime became `2026-09-14T16:12:23.946Z`, while
  `.social-context.state` remained absent. This confirms the deployed `~/.local/bin` symlink ran the
  changed source on schedule and emitted a fresh blindness artifact, not a room reading.
- `mesh-reflex-health --check` passed with 36 per-run reflexes fresh. No commit was made.
