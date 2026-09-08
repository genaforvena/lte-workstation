# Correlation investigation: `tempo=RESTING` ↔ `light=LIT` — spurious by construction

Date: 2026-09-08  
Disposition: discard; no fused sense and no reflex.

## Finding

The queued result was lift **1.86** (**9 occasions / 10 episodes** of 203, **876.2 h**),
re-measured inside `light=LIT`'s 07:00–17:00 band.  The full-window lift was **1.8**;
the hour-shadow correction reduced the surviving lift to **0.89**, below the 1.8 floor.

## Reality check

This is not an independent cross-sensor relation.  The producer contract in
[`scripts/mesh-activity-tempo`](../scripts/mesh-activity-tempo) defines:

- `RESTING = wifi=STILL + light=LIT`;
- the phone-off fallback emits `RESTING` only for `tamper=QUIET + light=LIT`;
- the camera fallback emits `RESTING` for a live still camera, but that branch is a
  separate degraded path and does not support the queued claim.

So every normal `RESTING` sample already contains `light=LIT` as an input.  The reported
co-occurrence is a feature of the label construction, not evidence that room rest causes
illumination or that illumination predicts rest.  The historical activity log shows the
same provenance explicitly, e.g. `RESTING — room quiet but lit | ... light=LIT`; it also
shows `SILENT` for the corresponding still/dark case and `BUSTLE` for motion/lit.  The
tempo vocabulary is encoding light context by design.

The current tape re-audit remains consistent with this diagnosis: 1,121 `RESTING` rows,
135 `RESTING∧LIT` rows, and 350 `LIT` rows give a full-window lift of 1.65; restricting
to 07:00–17:00 gives 74 joint rows out of 498 `RESTING` rows (conditional lift 2.03),
but that is still the producer's input copied into its output, not an independent test.

## Decision

Discard in one line: `RESTING` is defined using `light=LIT`, so the lift is producer self-correlation; the hour-shadow's 0.89 residual is below the floor and no fused sense/reflex is justified.

## Verification

- Read-only `bash scripts/mesh-correlate --dry` on the live tape; no queue write.
- Read-only census of `~/.mesh/sensor-tape.tsv` using the `tempo` and `light` columns.
- Inspected the live `~/.mesh/activity-tempo.log` provenance and the `mesh-activity-tempo`
  source branches named above.
- No genome tool or deployed copy was edited; no commit was made.
