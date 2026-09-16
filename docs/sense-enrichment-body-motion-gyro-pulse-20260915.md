# Sense enrichment: body-motion paired gyroscope pulse — 2026-09-15

`mesh-body-motion` now preserves the Euclidean delta between the two gyroscope samples in one
`termux-sensor -n 2` read as `gyro_delta`. If the latest gyro value is quiet but that measured delta
exceeds `GYRO_DELTA_THRESHOLD` (default `0.5`), the sense emits `HANDLED` with
`relation=rotation-pulse-without-translation`. This closes the latest-only blind spot without
turning absent gyro data into a quiet reading.

Verification:

- `rtk tests/test-mesh-body-motion-gyro-pulse.sh` — PASS; a 0.75 rad/s paired pulse produced the
  relation and JSON `gyro_delta=0.75`.
- `rtk tests/test-mesh-body-motion-test-real-read.sh` — PASS; the existing stubbed live SSH path
  still exercises the real-read gate and honest hollow/unreachable cases.
- `rtk scripts/integrations/mesh-body-motion --test` — exit 2 with
  `smoke-test: n/a (hollow body-motion sensor — needs two valid accelerometer samples)`; the live
  phone supplied no usable artifact, so no success is claimed.
