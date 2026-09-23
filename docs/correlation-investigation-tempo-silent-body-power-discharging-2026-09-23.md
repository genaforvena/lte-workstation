# Correlation investigation: `tempo=SILENT` → `body_power=DISCHARGING` — 2026-09-23

**Disposition: spurious as a causal/useful fused sense; discard.** No fused sense, no
reflex, no tool edit.

## Re-measurement (live tape 2026-09-23, 6659 rows)

- Naive: `SILENT` 307 rows, `DISCHARGING|SILENT` 95/307 (0.309) vs base 445/6659
  (0.067) — lift ≈ 4.63. **Confounded by sensor availability**: `SILENT` first
  appears 2026-08-15; the early tape is `NOLOG`/`STALE` body_power (2812 rows),
  so any late-era label "predicts" any live battery state.
- Era-restricted (1029 live-battery rows only): `DISCHARGING|SILENT` 95/151
  (0.629) vs base 445/1029 (0.432) — lift **1.45**, below the 1.8 floor.
  `CHARGING` naive lift 3.50 collapses to 1.10 live-only: SILENT predicts
  "phone reachable" (P(live|SILENT)=0.49 vs 0.16 base), not "discharging".
- Modal `DISCHARGING` tempo companion is `DEGRADED` (99), not `SILENT` (95);
  modal `SILENT` body_power companion is `UNREACHABLE` (113 > 95 DISCHARGING).
- `mesh-correlate --dry` and `--dry --stable` on live data **DROP this pair**:
  hour-stratified lift 1.64 < 1.8 (shadow with SILENT's hour histogram already
  scores 1.05 of 1.72) — time-of-day profile, not structure. Queued 1.80 does
  not survive the live gate.

## Reality check

- `SILENT` (`scripts/mesh-activity-tempo`): tamper-quiet + wifi-STILL +
  light-DARK — a room-at-rest label.
- `DISCHARGING` (`scripts/mesh-body-power`): phone battery status=discharging,
  i.e. phone off charger. No causal path either direction: room quiet neither
  unplugs the phone nor follows from it.
- Shared regime explains all of it: evening/night hours where the room is quiet
  AND the phone sits off its charger. Queued invariance (1 of 7 envs clear the
  floor; Markov-blanket-only, seed withheld) already marks it environment-specific.

## Decision

Discard in one line: **`SILENT` is a room-at-rest classification while
`DISCHARGING` is phone-off-charger status; their overlap is a shared
evening/night regime plus sensor-availability confounding (live-only lift 1.45,
live hour-stratified lift 1.64 < 1.8 floor, gate DROPs it), not a causal or
fusable signal.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found.

## Verification

- `python3` census over `~/.mesh/sensor-tape.tsv` (header-resolved, 6659 rows): splits above.
- `bash scripts/mesh-correlate --dry` / `--dry --stable`: pair DROPPED by hour-shadow gate, both modes.
- Read-only reads of both producers' SILENT/DISCHARGING definitions.
