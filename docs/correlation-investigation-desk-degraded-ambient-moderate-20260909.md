# Correlation investigation: `desk=DEGRADED` ↔ `ambient=MODERATE` — discard, 2026-09-09

## Verdict

Discard: `desk=DEGRADED` is an instrumentation-uncertainty/fault verdict, while
`ambient=MODERATE` is an independent room-audio level; their short historical
overlap is a shared sensing regime, not a causal desk state. No fused sense or
reflex is justified.

## Current reality check

The live `~/.mesh/sensor-tape.tsv` contains 4,940 data rows. There are exactly
20 `desk=DEGRADED` rows: 15 are paired with `ambient=MODERATE` and 5 with
`ambient=QUIET`. The rows are confined to 2026-08-15 through 2026-08-29; the
last two days of tape contain no new desk-degraded episode. The five QUIET
counterexamples include 2026-08-15 12:50Z, 2026-08-16 10:10Z, 2026-08-18
21:10Z, and 2026-08-26 16:20Z/21:10Z. Thus the proposed direction does not
survive even the existing extension of the original sample.

The 15 MODERATE rows cluster on 2026-08-15–17. `scripts/mesh-desk-state`
documents `DEGRADED` as mixed/insufficient evidence and records the specific
regression: a reachable phone whose body-motion producer returned no reading
was previously rendered as `DEGRADED:signals`; the corrected path is
`PARTIAL-IMAC` with `body=NO-READ`. This makes the historical cluster evidence
of a dead/partial desk axis, not a physical “degraded desk.”

The ambient producer is a separate sound-level classifier. During the cluster,
`~/.mesh/room-sense.log` shows the room sensor repeatedly reporting
`degraded=body-unknown,cam-blind` (and often `phone-unreachable`) while its
ambient clock remains `MODERATE`; the same records include ordinary `QUIET`
and `SILENCE` audio. That is a common availability/time regime (with some
ordinary playback), not evidence that desk uncertainty causes moderate sound.

## Evidence and verification

- `bash scripts/mesh-correlate --dry` completed with rc 0 and did not emit this
  pair as a current candidate; its live analysis reported the other surviving
  candidates instead.
- A direct parse of `~/.mesh/sensor-tape.tsv` reproduced `4,940` rows,
  `desk=DEGRADED: 20`, and the `MODERATE: 15 / QUIET: 5` split above.
- `bash scripts/mesh-correlate --test` and `bash scripts/mesh-desk-state --test`
  are the relevant producer checks; the desk test includes the hollow-phone
  regression assertion.
- No source or deployed mesh tool was edited and no commit was made.
