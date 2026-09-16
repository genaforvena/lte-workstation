# Sense enrichment: tamper event clock-skew guard — 2026-09-16

`mesh-tamper` now bounds producer timestamps before reading its event tape. Rows more than
`MESH_TAMPER_EVENT_FUTURE_SKEW` seconds ahead of the observer clock (default 300s) are excluded
from latest-event selection, recency, 24-hour counts, burst counts, and cadence. A bounded small
skew remains usable; a clock-corrupt future row can no longer manufacture `ACTIVE`, `BURST`, or
`PERIODIC` tamper evidence.

Verification:

- `rtk tests/test-mesh-tamper-test-real-read.sh` — PASS. The test drives the bounded real
  `SIGNIFICANT_MOTION` watch and confirms the hollow-driver path exits 2 without liveness writes.
- The same `--test` gate exercises clock fixtures: +100s is usable, +401s is rejected, the latest
  valid event skips the corrupt row, and recent counting excludes it.
- `rtk bash -n scripts/mesh-tamper` — PASS.
- Direct live `scripts/mesh-tamper --test` must remain an honest hardware result; its output and
  exit code are recorded in the handoff/board evidence, with exit 2 if the phone or driver is not
  live.

No commit made.
