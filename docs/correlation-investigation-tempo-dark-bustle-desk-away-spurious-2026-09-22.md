# Correlation investigation: `tempo=DARK_BUSTLE` ↔ `desk=AWAY`

**Date:** 2026-09-22
**Disposition:** **SPURIOUS / discard.** No fused sense and no reflex. (Reconfirms 2026-09-07 discard and 2026-09-08 rerecheck on the identical queued numbers.)

## Reproduction

`bash scripts/mesh-correlate --dry` (2026-09-22T06:06Z, rc=0): the queued candidate
(lift 2.00, 20 episodes / 13 occasions / 666 rows, window 1298.7h, shadow 0.98, full-window 3.0
confounded) is **gone** — "no correlation/prediction meets thresholds (honest empty)".
The live tape now reports the same pair as an hour-shadow DROP: lift 1.95, 49 episodes, shadow
already scores 1.03 of observed 0.92 (n=663), hour-stratified lift **0.89 < 1.8** — time-of-day
profile, not structure. The already-narrow 2.00-vs-1.8 margin has not survived the moving tape;
it has inverted.

No `--stable` row for the pair exists (UNSTABLE 0/3: env18 1.47, env20 1.52, env29 1.49 stands).

## Reality check

- `scripts/mesh-activity-tempo` `DARK_BUSTLE` = sustained/camera activity while the room is dark
  (provenance: `wifi=MOTION`, `light=DARK`, cam often UNKNOWN) — weak night-room activity, not an
  operator-location signal.
- `scripts/mesh-desk-state` `AWAY` = iMac UNREACHABLE (off/asleep) — a reachability verdict, not a
  witnessed departure.
- Joint rows per the 09-08 rerecheck: 30 joint rows / same 13 occasions, 28/30 `wifi=UNKNOWN`,
  corroborating body-motion mostly UNKNOWN/COVERED/OFFLINE — shared night/outage structure plus
  partial sensor failure.
- Live `~/.mesh/sensor-tape.log` is a rotated 565B stub: 0 `DARK_BUSTLE` rows to re-test. Nothing in
  fresh data revives the hypothesis.

## Decision

Discard in one line: **`DARK_BUSTLE` is weak night-room activity and `AWAY` is an iMac-reachability
verdict, so their narrow, environment-specific, now-inverted overlap is shared night/outage structure,
not a causal operator signal.**

## Verification

- `bash scripts/mesh-correlate --dry` — rc=0, honest-empty; same-pair hour-shadow drop at 0.89.
- `bash scripts/mesh-correlate --stable` — no DARK_BUSTLE/AWAY row (UNSTABLE stands).
- No tool edited; receipt left uncommitted for steward landing.
