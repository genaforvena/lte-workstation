# Rhythm/event-coincidence investigation: `Smart TV Pro` APPEARS → `ваня тв` appears ~60 min later

**Date:** 2026-09-23
**Disposition:** **SPURIOUS / discard.** No fused sense, no reflex.

## Re-measurement (live presence.log 2026-09-23, 4764 scans)

- `Smart TV Pro`: present in 255/4764 scans (0.054) — rare fringe beacon,
  median RSSI -82 (range -92…-74), 73 occasions.
- `ваня тв`: present in 141/4764 scans (0.030), median RSSI -78, 89 occasions.
- Joint scans: **3/4764 (0.0006)**. P(vn|smart)=0.012, P(smart|vn)=0.021 —
  the two almost never co-occur. An arrival-coupling (one arrival predicts the
  other's arrival an hour later, both lingering) must leave joint presence;
  there is none.
- Full-tape onset replication (absent→present, blackout gaps >30 min
  excluded): 70 smart onsets, 89 vn onsets. Forward hit (vn onset 50–70 min
  after smart onset): **7/70 = 0.10** vs random-window base rate **0.051**
  (102/2000) — ~2×, not 4.6×, on N=7 hits. Reverse: 5/89 = 0.056. Three of
  the 7 forward hits cluster on a single day (2026-09-21) — one regime
  afternoon, not a repeating coupling.
- Both are single-blink fringe detections (vn 1.6 scans/occasion, smart
  3.5 scans/occasion): flicker in/out of the scan floor, not arrivals.
- `mesh-leadlag --dry` (48h window) on the live tape: **honest empty**
  ("no stream predicts another above the permutation null"). The queued
  0.60-of-5-onsets candidate (a 48h hand-window draw) does not survive the
  live tape.

## Reality check

- Both endpoints are **stationary TV beacons at the scan fringe** (RSSI -82 /
  -78, single-scan blinks). "Appearance" is scanner-sensitivity flicker, not a
  person arriving with a device, not a door, not a schedule.
- The queued signature (3 of 5 eligible onsets in one 48h window, surrogate
  p=0.035 on the global max) is a window-lucky draw over pairs×leads×windows
  on two rare blinkers; full-tape replication gives 0.10 vs 0.051 base, and
  the reach-control 4.6× collapses with it.
- Nothing passes between the two at that moment — there is no hidden
  propagating process. The shared driver is scanner-side sensitivity drift
  (interference/temperature/phasing) moving two fringe TVs across the
  detection threshold on the same afternoon.

## Decision

Discard in one line: **two fringe TV blinkers that co-occur in 3 of 4764
scans cannot be arrival-coupled — the 60-min "lead" is a 5-onset window draw
(full-tape 0.10 vs 0.051 base, 3/7 hits from one afternoon, live dry
honest-empty), scanner-threshold flicker, not a person, door, or schedule.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found.

## Verification

- `scripts/mesh-leadlag --dry` (48h default) — rc=0, honest-empty.
- presence.log counts recomputed from the live file (4764 scans, smart
  255, vn 141, joint 3; 70/89 onsets; 7/70 forward vs 0.051 random).
- No tool edited (guards already exist; the live re-test did the rejection).
