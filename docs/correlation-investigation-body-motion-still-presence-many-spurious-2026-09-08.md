# Correlation investigation: `body_motion=STILL` ↔ `presence=MANY`

**Date:** 2026-09-08
**Disposition:** **SPURIOUS / discard.** No fused sense and no reflex.

## Reproduction

`bash scripts/mesh-correlate --dry` reproduces the queued candidate: corrected,
hour-stratified lift **3.01**, 60 episodes, 27 one-hour-collapsed occasions, and 344
usable rows. The queued window was 1304.7h; the live tape has since advanced to 1344.0h.
The uncorrected full-window lift is **2.1** and is explicitly confounded. A shadow with
`body_motion=STILL`'s own hour-of-day histogram scores **1.15**, leaving only the narrow
3.01-vs-1.8 margin.

`bash scripts/mesh-correlate --stable` reports **UNSTABLE**: the 1.8 floor clears in
**0/4** environments (env20 0.00, env25 1.00, env28 0.98, env29 0.98). The relation
therefore remains a Markov-blanket hypothesis, not a stable-blanket relation suitable for
generalization or seeding.

## Reality check

`scripts/mesh-body-motion` defines `STILL` from the phone's fused accelerometer,
orientation, step-counter, gyroscope, ambient-light, and proximity readings. It means the
phone is stationary; it does not establish that a person is stationary or that multiple
people are present.

`scripts/mesh-sensor-tape` maps a BLE scan count `n > 8` to `presence=MANY`. The live
`~/.mesh/presence.log` provides a concrete counterexample to reading this as people count:
the 2026-08-26 13:00–16:00 run repeatedly has `n=9–14`, including the recurring Bose
speaker, Samsung TV, Quest, a Bluetooth identity, and rotating `?` MACs. The 14:20 scan
has `n=14`, attribution `personal:11,appliance:2,ambiguous:1`, and `random:10`; those
fields classify BLE identities, not people.

An independent parse of the current tape finds **84** direct `STILL`/`MANY` rows, clustered
on Aug 26 (29), Aug 28 (14), Aug 29 (19), and Aug 30 (9), with only isolated rows on the
other dates. Across 688 `MANY` scans in the source log, the summed attribution counts are
1,410 appliance, 1,405 ambiguous, and 3,757 random-unidentified sightings. This is a local
BLE visibility/MAC-regime coincidence, not evidence that phone stillness causes or reliably
predicts multiple occupants.

## Decision

Discard in one line: **`STILL` is phone placement/motion and `MANY` is an unstable,
environment-specific BLE device-count bucket dominated by non-person and rotating-device
visibility, so fusing them would promote a confounded coincidence into a false presence
reflex.**

## Verification

- `bash scripts/mesh-correlate --dry` — reproduced the candidate and corrected lift.
- `bash scripts/mesh-correlate --stable` — reproduced the 0/4 unstable invariance result.
- `bash scripts/mesh-correlate --test` — passed its gate/falsifier smoke suite.
- `bash scripts/mesh-sensor-tape --test` — passed extraction, stale/missing, alignment, and
  rotation checks.
- Independent read-only parsing of `~/.mesh/sensor-tape.tsv` and `~/.mesh/presence.log` —
  confirmed the 84-row cluster and attribution evidence above.

No genome source or deployed tool was edited; no seed or reflex was created.
