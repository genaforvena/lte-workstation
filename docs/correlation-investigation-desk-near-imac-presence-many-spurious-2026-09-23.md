# Correlation investigation: `desk=NEAR-IMAC` ↔ `presence=MANY` — recheck 2026-09-23

**Disposition: SPURIOUS / discard.** No fused sense, no reflex, no tool edit. Confirms
2026-09-07, 2026-09-08, and 2026-09-22 verdicts (4th consecutive).

## Re-measurement (live tape 2026-09-23, 6633 rows)

- `NEAR-IMAC` total 75: `SOME` 39, `MANY` 33, `NONE` 2, `STALE` 1. SOME beats MANY
  inside the candidate's own rows — no invariant state.
- `MANY` is non-specific: `AT-DESK-TYPING` carries MANY 187 / SOME 1104 on the same tape.
- `mesh-correlate --dry`: pair absent on live data (no NEAR-IMAC↔MANY line).
- Queued numbers (24 episodes / 17 occasions / lift 1.83 vs 1.8 floor / 0-of-5 envs)
  describe a marginal late-August regime, not a stable relation.

## Reality check

- `NEAR-IMAC` (`scripts/mesh-desk-state`, `--test` PASS re-verified): iMac RF MOTION +
  phone STILL — phone-placement inference, not a people count.
- `MANY` (tape `extract_token`): BLE scan n>8 bucket mixing appliances, personal
  devices, rotating MACs — count churn, not people.

## Decision

Discard in one line: **`NEAR-IMAC` is an RF-disturbance/phone-placement state and
`MANY` is an un-attributed BLE device-count bucket; their marginal 1.83 overlap is an
environment-specific artifact (0/5 envs, SOME≥MANY on live tape), not a causal or
useful people-presence relation.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found (artifact below intentionally uncommitted for steward).

## Verification

- `python3` census over `~/.mesh/sensor-tape.tsv` (header-resolved, 6633 rows): splits above.
- `bash scripts/mesh-correlate --dry`: pair absent.
- `bash scripts/mesh-desk-state --test`: PASS.
