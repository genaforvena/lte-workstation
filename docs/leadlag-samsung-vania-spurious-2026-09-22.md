# Lead-lag investigation: `[TV] Samsung 5 Series (40)` → `ваня тв`

**Date:** 2026-09-22
**Disposition:** **SPURIOUS / discard.** No fused sense and no reflex.

## Reproduction

`mesh-leadlag --dry` / `--list` (2026-09-22T06:51Z, rc=0): honest empty —
"no stream predicts another above the permutation null". The queued candidate
(r=-0.82 at lag 1, 13 aligned Δ-steps, 48h window, perm p=0.020, circular p=0.010)
does not survive the live tape.

## Reality check

- Both "streams" are RSSI-visibility traces of two TV Bluetooth beacons in the SAME
  `~/.mesh/presence.log` scans, not independent moving processes: 127 `ваня тв` rows total,
  113/127 (89%) co-visible with the Samsung TV in the same sweep (e.g. 2026-07-15T07:00:10Z
  n=5: Bose + ваня тв + DV8235 + Bluetooth in one scan). The "lead" is one beacon's RSSI
  crossing a bin edge one 600s scan before the other's — scanner duty-cycle phasing, not motion.
- Coverage asymmetry 77%/12% says it outright: the Samsung (3658 rows) is near-always visible
  while ваня тв (127 rows) is sparse — correlating a dense stream against a sparse one over
  13 aligned steps manufactures direction.
- OUT-OF-WINDOW hold-out is `na (3 steps, UNREPLICATED)` — zero independent confirmation.
- No physical process exists by which one TV's "movement" drives another TV's movement 10 min
  later; the shared driver is the household radio environment plus the scanner's own schedule
  (the task itself notes the grid had to be raised 300s→600s because at 300s the delta lane is
  structurally empty — the signal lives in the binning, not the world).

## Decision

Discard in one line: **two co-visible TV beacons in the same BLE scans (113/127 joint) with
77%/12% coverage asymmetry over 13 steps and zero hold-out is scanner-phasing coincidence, not
a propagating process.**

## Verification

- `mesh-leadlag --dry` / `--list` — rc=0, honest empty.
- presence.log: 127 ваня rows, 113 joint with Samsung, 3658 Samsung rows; recency checked.
- No tool edited; receipt left uncommitted for steward landing.
