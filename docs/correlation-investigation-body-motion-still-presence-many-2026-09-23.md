# Correlation investigation: `body_motion=STILL` → `presence=MANY` — recheck 2026-09-23

**Disposition: SPURIOUS / discard.** No fused sense, no reflex, no tool edit.

## Re-measurement (live tape 2026-09-23, 6637 rows)

- `STILL` total 229: `MANY` 108 / `SOME` 78 / `STALE` 36 / `NONE` 7. MANY leads
  but only modestly; the candidate's own rows do not pin an invariant state.
- `MANY` total 977 spreads across body_motion: `UNKNOWN` 401, `NOLOG` 223,
  `STALE` 189, `STILL` 108, `OFFLINE` 43, rest 13. Modal MANY companion is
  UNKNOWN (3.7× STILL) — STILL explains 11% of MANY rows.
- Naive live lift P(MANY|STILL)/P(MANY) = 0.472/0.147 ≈ 3.20, but the queued
  invariance kills it: 0 of 4 environments clear the floor (0.00 / 1.00 /
  0.98 / 0.98) — inside a single environment STILL carries ~zero information
  about MANY (env25: 18/18×26 of 26, lift 1.00 exactly).
- `mesh-correlate --dry` and `--dry --stable`: pair absent from both on live data.
  The queued 3.01-lift candidate no longer clears the emit gate.

## Reality check

- `STILL` (`scripts/integrations/mesh-body-motion`): phone body-activity —
  the phone is parked, not moving. Sparse axis (229/6637 rows; UNKNOWN 2852,
  NOLOG 2458, STALE 704 dominate).
- `MANY` (presence bucket): BLE-scan device-count bucket (n>8) mixing
  appliances, personal devices, rotating MACs — count churn, not people
  (same bucket semantics as the NEAR-IMAC×MANY 4×-spurious verdict).
- A parked phone in a device-dense radio environment (desk, charger, evening
  hours where both peak) produces the overlap; nothing about phone stillness
  causes or predicts device-count churn.

## Decision

Discard in one line: **`STILL` is a phone-parked state while `MANY` is an
un-attributed BLE device-count bucket; their overlap is a device-dense-regime
artifact (0/4 envs, in-env lift ≈1.0, UNKNOWN dominates MANY 3.7× over STILL
on live tape), not a causal or useful presence signal.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found.

## Verification

- `python3` census over `~/.mesh/sensor-tape.tsv` (header-resolved, 6637 rows): splits above.
- `bash scripts/mesh-correlate --dry` / `--dry --stable`: pair absent from both.
- Read-only reads of the STILL producer doc and MANY bucket semantics.
