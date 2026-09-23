# Lead-lag investigation: `[TV] Samsung 5 Series (40)` → `ваня тв` (~10min movement lead)

**Date:** 2026-09-23
**Disposition:** **SPURIOUS / discard.** No fused sense, no reflex.

## Re-measurement (live presence.log 2026-09-23, 4753 scans)

- `Samsung 5 Series (40)`: present in 3817/4753 scans (0.80) — a near-ubiquitous
  fixed beacon, median RSSI -80, 45 occasions over 2026-07-15→2026-09-23.
- `ваня тв`: present in 141/4753 scans (0.030) — rare, median RSSI -78
  (same room, both TVs), 71 occasions.
- Joint scans: 126/141 vn scans (0.89) contain Samsung — but only 126/3817 sam
  scans (0.03). Asymmetric by base rate: vn almost never appears without sam
  because sam is almost always there.
- `mesh-leadlag --dry` (48h window) on the live tape: **no Samsung→ваня row —
  honest empty.** The queued r=-0.82/lag-1 candidate does not survive the live tape.
- Median scan interval 600.0s confirms the grid note.

## Reality check

- Both endpoints are **stationary TV beacons**, not arrival processes. A TV's
  RSSI "movement" (Δ-steps across scans) is scan-floor flicker + scanner phasing,
  not a device moving. No physical process exists by which one TV's flicker
  drives another TV's appearance 10 min later.
- The queued signature (13 aligned Δ-steps, perm p=0.020) is a window-lucky draw
  on the global max over pairs×lags: with sam present in 80% of scans, any
  10-min post-movement window covers vn movement by chance; out-of-window
  hold-out is na (3 steps, UNREPLICATED).
- Same-room medians (-80 vs -78) confirm co-location, not coupling: two TVs in
  one room share the scanner's sweep, and shared-sweep phasing is exactly what
  the leadlag guards (surrogate, blackout) already exist to reject.

## Decision

Discard in one line: **an always-on TV beacon (80% of scans) cannot "predict" a
rare co-located TV's flicker 10 min later — the lead is shared-sweep phasing of
scan-floor RSSI jitter, unreplicated on the live tape (dry honest-empty), not a
propagating process.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found.

## Verification

- `LEADLAG_WINDOW_H=48 scripts/mesh-leadlag --dry` — rc=0, no Samsung→ваня row.
- presence.log counts recomputed from the live file (4753 scans, joint 126/141).
- No tool edited (guards already exist; the live re-test did the rejection).
