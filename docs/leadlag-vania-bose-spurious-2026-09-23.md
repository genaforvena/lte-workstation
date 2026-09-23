# Lead-lag investigation: `ваня тв` → `LE-Bose Revolve SoundLink` (~10min movement lead)

**Date:** 2026-09-23
**Disposition:** **SPURIOUS / discard.** No fused sense, no reflex.

## Re-measurement (live presence.log 2026-09-23, 4763 scans)

- `LE-Bose Revolve SoundLink`: present in 4620/4763 scans (0.970) — a
  near-ubiquitous fixed speaker, median RSSI -68, 132 occasions over
  2026-07-15→2026-09-23.
- `ваня тв`: present in 141/4763 scans (0.030) — rare, median RSSI -78, 89 occasions.
- Joint scans: 140/141 vn scans (0.993) contain Bose — but only 140/4620 bose
  scans (0.030). Asymmetric by base rate: vn almost never appears without Bose
  because Bose is almost always there (mirror of the Samsung→ваня 80%-beacon
  verdict filed this morning).
- Bose Δ-steps are scan-floor flicker, not movement: 3611/4433
  consecutive-present pairs nonzero (81.5% jitter rate, RSSI range -90…-48).
  Any 10-min post-vn window covers a Bose "movement" step by chance.
- `mesh-leadlag --dry` (48h window) on the live tape: **honest empty**
  ("no stream predicts another above the permutation null"). The queued
  r=0.89/lag-1 candidate does not survive the live tape.
- Median scan interval 600.0s confirms the grid note.

## Reality check

- Both endpoints are **stationary indoor devices** (TV + fixed Bluetooth
  speaker), not arrival/movement processes. Neither physically moves; RSSI
  Δ-steps across scans are scan-floor flicker + scanner phasing.
- The queued signature (10 aligned Δ-steps, perm p=0.005) is a window-lucky
  draw on the global max over pairs×lags; the out-of-window hold-out already
  degrades (r 0.89 → +0.46 on 37 steps) instead of replicating.
- No physical process exists by which a TV's flicker drives a speaker's
  appearance 10 min later. Nothing moves first; there is no hidden
  propagating process — the shared driver is the scanner's own sweep phasing
  over two co-located beacons (same-room, medians -78 vs -68).

## Decision

Discard in one line: **a rare TV's flicker (3% of scans) cannot "predict" a
near-ubiquitous co-located speaker's jitter (97% of scans, 81% flicker rate)
10 min later — the lead is shared-sweep phasing of scan-floor RSSI noise,
window-lucky (hold-out degrades 0.89→0.46) and unreplicated on the live tape
(dry honest-empty), not a propagating process.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found.

## Verification

- `LEADLAG_WINDOW_H=48 scripts/mesh-leadlag --dry` — rc=0, honest-empty.
- presence.log counts recomputed from the live file (4763 scans, joint 140/141,
  Bose 4620/4763, vn 141/4763, 81.5% Bose jitter rate).
- No tool edited (guards already exist; the live re-test did the rejection).
