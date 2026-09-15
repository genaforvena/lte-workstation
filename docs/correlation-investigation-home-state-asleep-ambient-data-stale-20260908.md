# Correlation investigation: `home_state=ASLEEP` ↔ `ambient=DATA-STALE` — discard

**Date:** 2026-09-08  
**Verdict:** discard; no fused sense or reflex.

The queued claim treats `ambient=DATA-STALE` as a state. The ambient producer explicitly
defines that token as unavailable sensor evidence and exits 2 on that path
(`scripts/mesh-ambient-clock`, source comments and stale branch). Therefore the claimed
association cannot be causal environmental structure: one side is a home-state inference and
the other is the ambient reader reporting that its BLE input is not current.

## Current real-tape remeasurement

Source: `~/.mesh/sensor-tape.tsv`, read through `2026-09-08T21:40:01Z` (4,797 rows).

| measure | value |
|---|---:|
| `home_state=ASLEEP` rows | 223 |
| `ambient=DATA-STALE` rows | 911 |
| joint `ASLEEP ∧ DATA-STALE` rows | 198 |
| `ASLEEP` rows with a valid ambient state | 12 |
| current `ASLEEP ∧ DATA-STALE` runs after 1-hour collapse | 16 |

The 198 joint rows are concentrated in persistent outage runs, not independent ambient
episodes. The tape's current ambient state is also `DATA-STALE`, while the authoritative
`~/.mesh/presence.log` has not advanced since `2026-08-30T07:10:12Z`; the producer's live
state file is `DATA-STALE|...`. This is a stale-input/readability pattern.

The queue's reported 5.57 lift, 22 episodes, and 11 occasions therefore measure the
co-occurrence of an inferred state with a missing-data token. Hour stratification and
autocorrelation/occasion collapse cannot repair that semantic invalidity; the analyzer
correctly excludes `DATA-STALE` from usable readings before its lift and stable-blanket
calculations. No meaningful causal or useful operational signal remains to fuse.

**One-line discard:** `DATA-STALE` is the ambient sensor's explicit no-evidence/error state,
so its lift with `ASLEEP` is persistent feeder outage/missingness, not a real-world relation.

## Verification

- `rtk bash scripts/mesh-correlate --test` — PASS; `DATA-STALE`/`DATA-WARMUP` are treated as missing.
- `rtk bash scripts/mesh-ambient-clock --test` — PASS; stale-input path and label contract verified.
- `rtk bash scripts/mesh-home-state --test` — PASS; ambient-unavailable handling verified.
- `scripts/mesh-correlate --dry` / `--stable` — no target candidate survives because the token is missing data.

No source tool was edited, no deployed copy was touched, and no commit was made.
