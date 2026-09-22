# Correlation investigation: `desk=NEAR-IMAC` ↔ `presence=MANY` — recheck 2026-09-22

**Disposition:** **SPURIOUS / discard.** No fused sense, no reflex, no tool edit. Confirms 2026-09-07 and 2026-09-08 verdicts.

## Re-measurement (live tape 2026-09-22)

- Aligned tape: 6452 rows. `NEAR-IMAC` total 70: `SOME` 36, `MANY` 32, `NONE` 1, `STALE` 1. Even inside the candidate's own rows, `MANY` is tied with `SOME` — no invariant state.
- `scripts/mesh-correlate --dry` on the live tape: honest empty ("no correlation/prediction meets thresholds"); the 1.83-lift candidate no longer even clears the emit gate on current data. `--dry --stable` likewise emits nothing.
- Queued numbers (24 episodes / 17 occasions / lift 1.83 vs 1.8 floor / 0-of-5 environments) describe a narrow late-August regime, not a stable relation.

## Reality check

- `NEAR-IMAC` (`scripts/mesh-desk-state`): iMac RF `MOTION` + phone `STILL` — "phone set down at desk". An RF-disturbance/phone-placement inference, not a people count.
- `MANY` (`scripts/mesh-sensor-tape` `extract_token`): BLE scan `n > 8` bucket. Live scans mix fixed appliances (Bose, Samsung TV), personal devices, and rotating `?`/random MACs — count churn, not people.
- Non-specific: `MANY` occurs across desk states on the same tape — `AT-DESK` 33/97, `AT-DESK-TYPING` 156/1305. Nothing about `MANY` selects `NEAR-IMAC`.

## Decision

Discard in one line: **`NEAR-IMAC` is an RF-disturbance/phone-placement state and `MANY` is an un-attributed BLE device-count bucket; their marginal 1.83 overlap is an environment-specific late-August artifact (0/5 envs, tied SOME/MANY on live tape), not a causal or useful people-presence relation.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing committed.

## Verification

- `python3` census over `~/.mesh/sensor-tape.tsv` (header-resolved columns): 70 `NEAR-IMAC` rows, split above.
- `bash scripts/mesh-correlate --dry` and `--dry --stable`: both honest-empty on live data.
- Read-only reads of `scripts/mesh-desk-state` (NEAR-IMAC branch), `scripts/mesh-sensor-tape` (`extract_token` buckets), `~/.mesh/desk-state.log`, `~/.mesh/presence.log`.
