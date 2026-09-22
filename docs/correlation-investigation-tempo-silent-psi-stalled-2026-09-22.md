# Correlation investigation: `tempo=SILENT` ↔ `psi=STALLED` — recheck 2026-09-22

**Disposition:** **spurious as a causal/useful fused sense; discard.** No fused sense, no reflex, no tool edit. Confirms 2026-09-07 and 2026-09-08 verdicts.

## Re-measurement (live tape 2026-09-22)

- Aligned tape: 6454 rows. `SILENT` total 272: `STALLED` 68 / `CALM` 132 / `BUSY` 70 / `STALE` 2. `SILENT` co-occurs with `CALM` nearly 2× more than with `STALLED` — no invariant coupling.
- `STALLED` total 603 spreads across tempo states: `RESTING` 243, `DARK_BUSTLE` 111, `DEGRADED` 74, `SILENT` 68, `UNKNOWN` 66, `BUSTLE` 41. The modal STALLED companion is `RESTING`, not `SILENT`.
- `scripts/mesh-correlate --dry` and `--dry --stable`: honest empty on live data — the queued 3.72-lift candidate no longer clears the emit gate. Intermittent historical regime, not a live coupling.

## Reality check

- `SILENT` (`scripts/mesh-activity-tempo`): tamper-quiet + wifi-STILL + light-DARK — a room-at-rest label. Live read now: `DARK_BUSTLE` (camera motion in darkness).
- `STALLED` (`scripts/mesh-psi`): host kernel contention (CPU/IO/mem pressure). Live read now: `BUSY` cpu-dominant (cpu_some 32.84%), not stalled. Different domains; a room-quiet label cannot explain kernel contention.
- Queued stats (14 episodes / 12 occasions / 2-of-4 envs) already mark it Markov-blanket-only; live data weakens it further.

## Decision

Discard in one line: **`SILENT` is a room-motion classification while `STALLED` is independent host kernel contention; their clustered overlap is shared night/workload regime (RESTING dominates STALLED live), not a causal signal worth fusing or reflexing.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing committed.

## Verification

- `python3` census over `~/.mesh/sensor-tape.tsv` (header-resolved): joint splits above.
- `bash scripts/mesh-correlate --dry` / `--dry --stable`: both honest-empty.
- Live `mesh-psi --json` (BUSY/cpu) and `mesh-activity-tempo` (DARK_BUSTLE) reads.
- Read-only reads of `scripts/mesh-activity-tempo` (SILENT def) and `scripts/mesh-psi` (STALLED def).
