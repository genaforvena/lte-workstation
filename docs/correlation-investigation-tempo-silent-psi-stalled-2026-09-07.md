# Correlation investigation: `tempo=SILENT` → `psi=STALLED`

**Disposition:** spurious as a causal/useful fused sense; discard. No fused sense or
reflex.

## Reproduction

`bash scripts/mesh-correlate --dry` reproduces the queued candidate exactly: lift
3.72, 14 episodes, 12 occasions, 380 usable rows, 1297.8 h; the hour-matched
shadow is 1.23 and the stable-blanket verdict is `UNSTABLE` (only 2 of 4
environments clear 1.8: 1.92, 1.50, 0.96, 1.83). The analyzer's fixed
autocorrelation/one-hour occasion gates are therefore working, but they do not
turn this into a causal relation.

The aligned tape currently has 4,528 data rows, 246 `tempo=SILENT`, 250
`psi=STALLED`, and 63 row-level co-occurrences. Those rows form seven broad
clusters, concentrated on 2026-08-19/20 and 2026-08-28/30, rather than a
repeatable all-window condition.

## Reality check

The two labels measure different things. `mesh-activity-tempo` defines `SILENT`
from no detected room motion plus dark/rest context; its live log explicitly
reports `tamper=UNKNOWN`, `wifi=UNKNOWN/UNCERTAIN`, and webcam `STILL` or a
blind/covered camera during much of the relevant period. `mesh-psi` defines
`STALLED` from kernel CPU/IO/memory pressure, with the dominant resource and
interval window in its output; it is not a room-activity observation.

The tape makes the confound visible: among the 63 joint rows, 37 have
`body_motion=UNKNOWN`, 34 `body_state=DEGRADED`, 33
`body_power=UNREACHABLE`, 30 dark and 25 dim light, and 28 degraded social
readings. This is a sensor-availability/night/workload regime, not corroborated
evidence that a quiet room causes resource stalls. The current live check is
also reversible: `mesh-psi --json` reads `CALM` while the independent process
table shows active CPU consumers, demonstrating that the level changes with
host workload and is not pinned to the room's tempo.

## Decision

Discard in one line: `SILENT` is a degraded/night room-motion classification and
`STALLED` is host kernel contention; their few environment-specific overlaps
are a shared operating regime, not a physical coupling worth acting on.

## Verification

- `bash scripts/mesh-correlate --dry` and `--stable` reproduced the candidate and
  its `invariance=UNSTABLE` breakdown without writing the queue.
- Direct `awk` census over `~/.mesh/sensor-tape.tsv` recorded the row and cluster
  counts above.
- Live `~/.local/bin/mesh-psi --json` returned `level=CALM` with interval
  coverage, while `/proc/pressure/*` and `ps` provided the independent host
  readings.
- No deployed copy was edited, no reflex was wired, and no commit was made.
