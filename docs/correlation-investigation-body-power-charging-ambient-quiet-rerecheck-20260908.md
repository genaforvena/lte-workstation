# Correlation re-check: `body_power=CHARGING` ↔ `ambient=QUIET` — discard

**Date:** 2026-09-08  
**Artifact:** current `~/.mesh/sensor-tape.tsv`, current producer sources, and live self-checks  
**Verdict:** discard; no fused sense or reflex.

The queued claim is a repeat of the 2026-08-20 finding. That investigation already showed the
original 2.26 lift was a clock-shaped artifact: `mesh-ambient-clock` renames `QUIET` to
`NIGHT-QUIET` at hours 23:00–05:00 (`scripts/mesh-ambient-clock:1068-1070`), while charging
clusters in the daytime/evening shoulders. Its hour-stratified lift was 1.37, below the 1.8
floor, and the general hour-shadow correction is now landed in `scripts/mesh-correlate`.

## Current tape re-measurement

From the claimed era start (`2026-08-15T06:30:01Z`) through the current tape tail, excluding
non-readings (`STALE`, `UNKNOWN`, `UNREACHABLE`, `TIMEOUT`, `DATA-*`):

| measure | value |
|---|---:|
| aligned valid rows | 540 |
| `body_power=CHARGING` | 136 |
| `ambient=QUIET` | 236 |
| joint `CHARGING ∧ QUIET` | 80 |
| raw aligned lift | **1.35** |
| hour-matched expected joint rows | 63.323 |
| hour-stratified lift | **1.26** |

The current corrected value is further below the floor than the queued value. `CHARGING` also
has 26 `NIGHT-QUIET` rows; treating the producer's explicit night label as ordinary `QUIET`
would erase the very clock boundary that explains the original result.

## Reality check

`ambient` in the sensor tape is `ambient-clock`, the fixed-appliance BLE classifier—not the
microphone's independent dB tape. The BLE input is not currently live: `~/.mesh/presence.log`
has its last write at 2026-08-30T07:10:12Z, while the current tape continues to emit
`ambient=DATA-STALE`. Therefore recent apparent pairings cannot be treated as fresh ambient
evidence. `body_power` is likewise frequently unavailable in the current tail; its live ledger
ends with repeated `UNREACHABLE` readings.

This leaves no operationally trustworthy joint state to fuse. The residual historical association
may reflect ordinary phone charging coinciding with household schedule, but it is not a causal
ambient signal and does not clear the corrected evidence floor.

## Decision

**SPURIOUS / discard:** the original lift was primarily the ambient clock's deliberate
`QUIET`/`NIGHT-QUIET` boundary plus charging's time-of-day distribution; the current valid tape
re-check is only 1.26 hour-stratified lift, and the ambient BLE source is now stale. No fused sense
or reflex is justified.

## Verification

- `rtk bash scripts/mesh-correlate --dry` — current live miner ran read-only; no candidate for
  this already-suppressed pair was emitted.
- `rtk bash scripts/mesh-correlate --test` — PASS.
- `rtk bash scripts/mesh-ambient-clock --test` — PASS.
- `rtk timeout 20 bash scripts/mesh-body-power --test` — timed out (124), consistent with the
  phone-unreachable live ledger; this is an honest failed live check, not a green claim.

No source tool was edited and no commit was made.
