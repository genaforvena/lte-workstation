# Correlation investigation: `tempo=SILENT` → `psi=STALLED` — recheck 2026-09-23

**Disposition: spurious as a causal/useful fused sense; discard.** No fused sense, no
reflex, no tool edit. Confirms 2026-09-07, 2026-09-08, and 2026-09-22 verdicts (4th consecutive).

## Re-measurement (live tape 2026-09-23, 6632 rows)

- `SILENT` total 305: `CALM` 153 / `BUSY` 81 / `STALLED` 69 / `STALE` 2.
  SILENT co-occurs with CALM 2.2× more than with STALLED — no invariant coupling.
- `STALLED` total 627 spreads across tempo states: `RESTING` 250, `DARK_BUSTLE` 117,
  `DEGRADED` 74, `SILENT` 69, `UNKNOWN` 66, `BUSTLE` 51. Modal STALLED companion is
  RESTING, not SILENT (unchanged from 09-22).
- `mesh-correlate --dry` and `--dry --stable`: neither emits this pair on live data.
  The queued 3.72-lift candidate no longer clears the emit gate — intermittent
  historical regime, not a live coupling.

## Reality check

- `SILENT` (`scripts/mesh-activity-tempo`): tamper-quiet + wifi-STILL + light-DARK —
  a room-at-rest label. Note: tempo `--test` currently FAILs its own light-alphabet
  leg (mesh-light UNKNOWN band unclaimed — live BUSTLE read shows `light=UNKNOWN`
  dead axis). That weakens the SILENT producer itself, not this pair's case.
- `STALLED` (`scripts/mesh-psi`): host kernel contention. Live read now: `CALM`
  (cpu_some 16.55%), not stalled. Different domains; room-quiet cannot explain
  kernel contention.
- Queued stats (14 episodes / 12 occasions / 2-of-4 envs) already mark it
  Markov-blanket-only (seed withheld); live data weakens it further.

## Decision

Discard in one line: **`SILENT` is a room-motion classification while `STALLED` is
independent host kernel contention; their clustered overlap is shared night/workload
regime (RESTING dominates STALLED live), not a causal signal worth fusing or reflexing.**

No genome source or deployed copy edited, no seed created, no reflex wired, nothing
committed. Tree left exactly as found.

## Verification

- `python3` census over `~/.mesh/sensor-tape.tsv` (header-resolved, 6632 rows): splits above.
- `bash scripts/mesh-correlate --dry` / `--dry --stable`: pair absent from both.
- `bash scripts/mesh-psi --test`: PASS. Live `mesh-psi --json`: CALM.
- Read-only reads of both producers' SILENT/STALLED definitions.
