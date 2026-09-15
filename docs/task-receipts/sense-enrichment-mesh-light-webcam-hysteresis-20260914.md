# Sense enrichment: mesh-light webcam hysteresis — 2026-09-14

## Change

The coarse webcam fallback now classifies the measured frame median through a four-luma-unit
hysteresis band around its DARK/DIM/MODERATE/LIT thresholds. First reads retain the existing raw
thresholds; later readings hold their prior band until the relevant edge is crossed. The fallback
still publishes the webcam source, coarse flag, measured frame age, scene, and spread. It does not
invent lux or a BRIGHT band. `MESH_CAM_LIGHT_HYST` configures the luma deadband; malformed median or
configuration degrades the fallback as unreadable.

## Verification

- Test-first red: before adding `classify_webcam_level`, 13 boundary assertions failed with the
  expected missing-classifier result, and the smoke test exited 1.
- `scripts/mesh-light --test` — PASS, including 13 band-edge assertions, an end-to-end fallback
  assertion for hysteresis plus source/coarse tags, and a fresh webcam frame artifact:
  `MODERATE mean=94.2 median=89.0 stddev=58.1 p10=26 p90=183 spread=157 scene=varied`.
- `scripts/mesh-light --json` — exit 0 with a live fallback artifact at
  `2026-09-14T17:27:59Z`: `level=MODERATE`, `source=webcam`, `coarse=true`, frame age 2s,
  median 89, spread 159, `scene=varied`.
- Isolated all-vantages-unavailable runtime check — exit 2 and wrote an `OFFLINE` state; no light
  level was returned. Phone SSH, beacon, and camera frame were deliberately unavailable in the
  isolated HOME.
- `bash -n scripts/mesh-light` and `git diff --check -- scripts/mesh-light` — PASS.

No commit was made.

## Live recheck — 2026-09-14 21:18 UTC

- `scripts/mesh-light --test` — PASS; the gate completed its classifier/fallback assertions and
  available-live-vantage checks.
- `scripts/mesh-light --craft` — exit 0 with a live Note3 sensor artifact:
  `DARK`, `lux=0`, `tick=208522050255868`, `dwell_s=13766`, `changes_24h=10`.
  The resulting `~/.mesh/.light-craft-state` was 72 bytes, mtime `2026-09-14 21:18:27 UTC`, with
  bytes `DARK|room=craft|lux=0|tick=208522050255868|dwell_s=13766|changes_24h=10`.
- Primary `scripts/mesh-light --json` returned exit 2 (`phone unreachable`); explicit
  `scripts/mesh-light --webcam` returned exit 2 (`covered`, flat frame). Neither failure was
  converted to a light level. The live craft-room Note3 read supplied the real artifact.
- `bash -n scripts/mesh-light` and `git diff --cached --check -- scripts/mesh-light` — PASS.

No commit was made.
