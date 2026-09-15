# Sense liveness — `phone-prox` — 2026-09-12 12:22 UTC

Disposition: **DECAYED on this node**. `phone-prox` is cron-scheduled, but its Redmi input is
unreachable and its last real proximity log is stale. The current state reports `UNREACHABLE`; it is
not a proximity value. Keep the scheduled probe available to detect recovery, but do not consume the
old reading as current.

Evidence:

- `mesh-reflex-health` and `mesh-reflex-health --check` both report the `phone-prox` value frozen for
  795,368 seconds (about 9.2 days), while the related reflex remains scheduled. The overall health
  check has other stale axes too; it is not an all-clear.
- Crontab contains `2-59/10 * * * * ... mesh-phone-prox --edge`.
- `~/.mesh/phone-prox.log` is 23,610 bytes and last changed 2026-09-03 07:12:08 UTC. Its tail says
  `phone unreachable — can't read proximity (not an alarm)`.
- `mesh-phone-prox --test` exits 2 with `phone unreachable — no live proximity read`; the subsequent
  live `--json` probe also exits 2. `~/.mesh/.phone-prox.state` says
  `UNREACHABLE|why=ssh|ts=2026-09-12T12:22:01Z`, which records the failed transport, not a sensor
  measurement.
- `mesh-sense-map --refresh` produced a fresh inventory at 12:20:10 UTC: Redmi 10 is offline, while
  Note3 is online. This corroborates the unavailable input without interpreting silence as absence.
- Other reachable Note3 organs were probed with their real-read tests: light, magnetic field, motion,
  proximity, and thermal all returned live ADB readings. Webcam (`mesh-light --test`) and climate
  (`mesh-climate --test`) also returned live artifacts.
- After recording this disposition, `mesh-note3-light-raw --edge` returned a live reading
  `STABLE (raw=4003.32 lux=3.3742 delta=3.7% gate=HOLD)` at 12:22 UTC; the real-read log was updated
  at 12:22:05 UTC. This verifies a fresh real artifact from a reachable sense organ after the
  disposition.

Recovery: when Redmi SSH is reachable, require `mesh-phone-prox --test` to produce a live proximity
read and confirm the real log advances before removing this decay assessment.

No code or cron changes were made; nothing was committed.
