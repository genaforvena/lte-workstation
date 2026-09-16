# Coevolutionary minimal-criterion link — 2026-09-16

## Selection

Chose option (b): extend `mesh-sensorium --cached` to consume the live-but-under-consumed
`mesh-imac-cam-watch` sense. Before the patch, this proof returned no matches:

    grep -rlF 'imac-cam-watch' scripts/mesh-situation scripts/mesh-sensorium \
      scripts/mesh-stress scripts/mesh-ambient-clock scripts/mesh-operator-state

The producer artifact was live and real:

    mesh-imac-cam-watch --state       -> SEEING, rc=0
    ~/.mesh/.imac-cam-watch.state     -> fresh mtime
    ~/.mesh/imac-cam-watch.log        -> fresh producer log

## Closed edge

`scripts/mesh-sensorium` now reads `~/.mesh/.imac-cam-watch.state` into the ROOM roll-call as
`eyes=$(mark ... 600)`. The consumer preserves the minimal honest states: fresh `SEEING`,
`SEEING (STALE)` after the freshness bound, and `? (—)` when the artifact is absent. No new
producer tool was created, so no new orphan/cadence header or autowire mutation was required.

## Verification

- Focused sensorium fixture passed all three branches: `ROOM eyes=` fresh/STALE/absent.
- Live producer: `mesh-imac-cam-watch --state` returned `SEEING`, rc 0.
- Live consumer: `mesh-sensorium --cached` rendered `eyes=SEEING (fresh)`.
- Post-patch grep finds the edge in `scripts/mesh-sensorium`.
- `mesh-doctor --test` passed, rc 0, with no orphan warning.
- `bash -n scripts/mesh-sensorium` passed and the source remained executable.

The broader `mesh-sensorium --test` returned rc 1 only at its existing dependency gate:
`mesh-wifiscan --test failed, rc=1`; the new `ROOM eyes=` fixture passed before that gate.
The full aggregate `mesh-doctor` exceeded its 120-second bound; its captured output showed
pre-existing substrate warnings/failures, not a new orphan warning. No commit was made.
