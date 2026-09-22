# Correlation investigation: `body_motion=STILL` ↔ `presence=MANY`

**Date:** 2026-09-22
**Disposition:** **SPURIOUS / discard.** No fused sense and no reflex. (Reconfirms 2026-09-07 and 2026-09-08 verdicts on the identical queued numbers.)

## Reproduction

`bash scripts/mesh-correlate --dry` (2026-09-22T05:31Z, rc=0): the queued candidate is **gone** —
"no correlation/prediction meets thresholds (need more data — honest empty, not a failure)".
The queued window (1304.7h, 60 episodes / 27 occasions / 344 rows, lift 3.01 hour-stratified vs 1.8
floor, full-window 2.1 confounded, shadow 1.15) has aged out of the live tape; the gates currently
drop every other candidate the same way (hour-shadow / occasion-gate / clock-gate lines).

`bash scripts/mesh-correlate --stable`: no `STILL`/`MANY` row at all — the UNSTABLE verdict
(0/4 environments clearing 1.8: env20 0.00, env25 1.00, env28 0.98, env29 0.98) stands unchallenged.

## Reality check

- `scripts/mesh-sensor-tape` maps BLE scan count `n > 8` → `presence=MANY` (NONE/FEW/SOME/MANY buckets).
  It counts radio identities, not people.
- `scripts/mesh-body-motion` `STILL` means the phone is stationary, not that a person is still or
  that multiple people are present.
- Live `~/.mesh/presence.log`: 896 scans with `n=9–14` persist; a sampled `n=14` row
  (2026-07-28T18:50:09Z) contains a Bose Revolve speaker, Quest 3, Samsung TV, a Bluetooth identity,
  and rotating `?` MACs — a device-visibility/MAC-regime coincidence. 4466 rows name
  Bose/Samsung/Quest appliances.
- Live `~/.mesh/sensor-tape.log` is a 565B rotated stub: zero `STILL`/`MANY` co-occurrence rows to
  re-test against. Nothing in fresh data revives the hypothesis.

## Decision

Discard in one line: **`STILL` is phone placement and `MANY` is an unstable, environment-specific
BLE device-count bucket dominated by appliances and rotating MACs, so fusing them would promote a
confounded, non-reproducing coincidence into a false presence reflex.**

## Verification

- `bash scripts/mesh-correlate --dry` — rc=0, honest-empty, queued candidate absent.
- `bash scripts/mesh-correlate --stable` — no STILL/MANY row.
- `grep -a -c "n=9\|n=1[0-4]" ~/.mesh/presence.log` → 896; sampled n=14 attribution inspected.
- No tool edited; receipt left uncommitted for steward landing.
