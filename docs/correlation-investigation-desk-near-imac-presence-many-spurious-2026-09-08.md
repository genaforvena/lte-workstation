# Correlation investigation: `desk=NEAR-IMAC` ↔ `presence=MANY`

**Date:** 2026-09-08  
**Disposition:** **SPURIOUS / discard.** No fused sense and no reflex.

## Re-measurement

The live miner reproduces the queued candidate after its clock gate: lift **1.83**, 24
episodes, 17 one-hour-collapsed occasions, over 1,253 aligned rows in the
`desk=NEAR-IMAC` 13:00–01:00 band. The full-window lift is 1.9, but it is the
confounded number rejected by the gate. The current stable report still marks the pair
`UNSTABLE`: **0 of 5 environments** clears the 1.8 floor (env18 0.00, env24 0.75,
env25 1.00, env28 0.86, env29 1.03).

A direct count of the current aligned tape gives 64 `NEAR-IMAC` rows:

| `presence` | rows |
|---|---:|
| `MANY` | 31 |
| `SOME` | 31 |
| `NONE` | 1 |
| `STALE` | 1 |

Thus the candidate is a narrow historical association, not an invariant state: even
inside the candidate's own band, `MANY` is tied with `SOME`, and the held-out
environment results never reproduce the floor.

## Reality check

`NEAR-IMAC` is not a people-count sensor. `scripts/mesh-desk-state` defines it as
iMac RF motion plus phone `STILL`: “RF disturbance near iMac but phone stationary —
phone set down at desk.” The RF motion can be multipath or a nearby disturbance; it
does not identify a person or imply multiple people.

`presence=MANY` is also not a people-count sensor. `scripts/mesh-sensor-tape` buckets
the raw BLE scan count (`n > 8`) into `MANY`. The live source records fixed appliances
(including the Bose desk speaker), known personal devices, and unidentified/random
devices in that count. For example, the source contains `n=10–11` scans on
2026-08-25 with several `?` devices alongside the recurring Bose device; the count
cannot distinguish people from appliances or RF churn.

The joint rows cluster in a short late-August source regime: 14 of the 31 `MANY`
rows occur on 2026-08-26, while `SOME` dominates the earlier 2026-08-15–20 period
(with only five later `SOME` rows). The BLE log then stops at 2026-08-30 and the aligned tape
correctly renders later presence as `STALE`; this is not evidence for a continuing
desk/presence coupling.

## Decision

Discard in one line: **`NEAR-IMAC` is an RF-disturbance/phone-placement state and
`MANY` is an un-attributed BLE device-count bucket; their 1.83 lift is an
environment-specific late-August artifact (0/5 environments), not a causal or useful
people-presence relation.**

No genome source or deployed tool was edited, no seed was created, and no reflex was
wired.

## Verification

- `scripts/mesh-correlate --dry`: reproduced the candidate and its corrected lift.
- `scripts/mesh-correlate --stable`: reproduced the 0/5 unstable invariance verdict.
- `awk` over `~/.mesh/sensor-tape.tsv`: counted 64 `NEAR-IMAC` rows and the
  `MANY=31`, `SOME=31`, `NONE=1`, `STALE=1` split.
- Read-only inspection of `scripts/mesh-desk-state`, `scripts/mesh-sensor-tape`,
  `~/.mesh/desk-state.log`, and `~/.mesh/presence.log`: confirmed the source
  semantics and dated device-count evidence.
