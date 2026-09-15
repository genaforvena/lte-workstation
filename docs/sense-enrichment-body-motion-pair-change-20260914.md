# Body-motion paired accelerometer change signal — 2026-09-14

`mesh-body-motion` already required two valid accelerometer samples from one sensor call and
published their vector delta as `accel_delta`. The delta is now classified as an additive
`sensors.sample_change` value: `CHANGING` at or above 0.5 m/s², `LOW_CHANGE` below that threshold,
and JSON `null` / text `UNKNOWN` when a paired delta is absent. Set
`MESH_BODY_ACCEL_DELTA_THRESHOLD` to change the band boundary. This paired interval is supplementary;
`LOW_CHANGE` does not mean the body was still during the rest of the cadence window, and the existing
body-state verdict is unchanged.

## Verification

- TDD red: before implementation, the new assertions failed because `sample_change` was missing for
  high, low, and absent paired-delta cases.
- TDD green: `scripts/mesh-body-motion --test` passed all classifier, honest-degrade, confidence,
  dwell, simulate-isolation, hysteresis, and paired-change assertions. Its final real phone probe
  exited 2 with `phone unreachable or no termux-sensor`; no hardware success is claimed.
- `tests/test-mesh-body-motion-test-real-read.sh` passed. It exercises fresh two-sample sensor
  artifacts plus hollow, one-sample, and unreachable paths; the unreachable case exits 2.
- Direct live `scripts/mesh-body-motion --json` exited 2 with
  `phone unreachable — no body-motion read (not a state, n/a)`. No reading was fabricated.
- `bash -n scripts/integrations/mesh-body-motion scripts/mesh-body-motion` passed.

The paired-change classifier has fixture evidence, but a fresh physical paired sample was unavailable
on mesh-home at verification time. No commit was made.
