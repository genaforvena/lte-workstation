# Correlation investigation: `tempo=DARK_BUSTLE` → `desk=AWAY` — recheck 2026-09-23

**Disposition: SPURIOUS / discard.** No fused sense, no reflex, no tool edit.

## Re-measurement (live tape 2026-09-23, 6635 rows)

- `DARK_BUSTLE` total 723: desk split `UNKNOWN` 370 / `PARTIAL-IMAC` 146 /
  `AT-DESK-TYPING` 100 / `AWAY` 68 / rest 39. Desk-present states
  (PARTIAL-IMAC + AT-DESK-TYPING + AT-DESK = 256) outweigh AWAY 3.8× inside the
  candidate's own rows — no invariant coupling.
- `AWAY` total 405 spreads across tempo: `RESTING` 117, `DEGRADED` 104,
  `DARK_BUSTLE` 68, `UNKNOWN` 66, `SILENT` 42, `BUSTLE` 8. Modal AWAY companion
  is RESTING, not DARK_BUSTLE.
- Naive live lift P(AWAY|DB)/P(AWAY) = 0.094/0.061 ≈ 1.54 < 1.8 — does not clear
  the floor even before stratification.
- `mesh-correlate --dry` and `--dry --stable`: pair absent from both on live data.
  The queued 2.00-lift candidate no longer clears the emit gate.
- Queued invariance (0 of 3 envs: 1.47 / 1.52 / 1.49) already marks it
  Markov-blanket-only (seed withheld); live data weakens it further.

## Reality check

- `DARK_BUSTLE` (`scripts/mesh-activity-tempo`): wifi=MOTION + light=DARK —
  sustained room activity in darkness.
- `AWAY` (`scripts/mesh-desk-state`, `--test` PASS re-verified): iMac UNREACHABLE
  (off/asleep) — operator away from desk.
- Different domains: a person moving in a dark room while the iMac sleeps is a
  shared night regime (RESTING dominates AWAY live), not a causal signal.

## Decision

Discard in one line: **`DARK_BUSTLE` is a room-motion-in-darkness label while
`AWAY` is iMac-off/asleep state; their overlap is shared night regime
(RESTING dominates AWAY, desk-present beats AWAY 3.8× inside DARK_BUSTLE rows,
live lift 1.54 < 1.8, 0/3 envs), not a causal or useful fused signal.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found.

## Verification

- `python3` census over `~/.mesh/sensor-tape.tsv` (header-resolved, 6635 rows): splits above.
- `bash scripts/mesh-correlate --dry` / `--dry --stable`: pair absent from both.
- `bash scripts/mesh-desk-state --test`: PASS (smoke-test ok).
