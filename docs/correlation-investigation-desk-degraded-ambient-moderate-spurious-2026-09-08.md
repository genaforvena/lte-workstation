# Correlation investigation: `desk=DEGRADED` ↔ `ambient=MODERATE` — spurious, 2026-09-08

**Disposition:** discard as a causal or operational coupling. No fused sense and no reflex.

## Reproduction and re-measurement

The queued observation was recorded as lift **2.5**, 11 episodes, 8
autocorrelation-collapsed occasions, and 567 usable rows over 794.2 hours. A
read-only run of `scripts/mesh-correlate --dry` against the current live tape
does not reproduce this pair as the best finding; the current tape has 20
`desk=DEGRADED` rows, 15 of them paired with `ambient=MODERATE`, over 4,776
rows. The old support therefore came from a short historical regime, not a
stable relation.

The current matching rows cluster on 2026-08-15–17 (15 of the 20 rows). The
remaining five are isolated later observations, and the paired value is not
specific to the desk state: `ambient=MODERATE` is common in the full tape
(1,128/4,776 rows). The candidate has no stable, repeatable support after the
historical regime is extended.

## Reality check

`scripts/mesh-desk-state` defines `DEGRADED:signals` as mixed/insufficient
evidence, commonly `iMac=STABLE|MOTION`, stale camera, idle input, and
`body=UNKNOWN`; it is an uncertainty/fault label, not a physical desk state.
The code explicitly distinguishes phone-offline and hollow body reads as
`PARTIAL-IMAC`, so the historical `DEGRADED` rows are evidence of incomplete
desk instrumentation rather than “the operator is at a degraded desk.”

The ambient side is an independent sound-level classifier. The corresponding
`room-sense.log` records around the dense 2026-08-15–17 cluster show the room
as present but degraded by phone/body/camera availability, while the ambient
clock remains `MODERATE`; `room-activity.log` also records moderate audio with
media sessions. This is a shared availability/time regime (and sometimes
ordinary playback), not a mechanism whereby desk ambiguity causes moderate
sound.

The live tape also contains `desk=DEGRADED` with `ambient=QUIET` (5/20 rows),
including 2026-08-16 10:10Z and 2026-08-26 16:20Z/21:10Z, which directly breaks
the proposed “DEGRADED tends to MODERATE” interpretation outside the original
cluster.

## Decision

Discard in one line: `desk=DEGRADED` is an instrumentation-uncertainty label,
while `ambient=MODERATE` is an independent audio-level reading; their brief
overlap is explained by the same degraded historical sensing regime and does
not justify a fused sense or reflex.

## Verification

- `bash scripts/mesh-correlate --test` passed.
- `bash scripts/mesh-desk-state --test` passed.
- `bash scripts/mesh-correlate --dry` was run read-only against a copy of the
  live tape with optional gates disabled for the re-measurement; no queue was
  written.
- The counts and matching timestamps were independently read from
  `~/.mesh/sensor-tape.tsv`; desk semantics from `scripts/mesh-desk-state` and
  ambient provenance from `~/.mesh/room-sense.log` and
  `~/.mesh/room-activity.log`.
- No mesh tool was edited, no deployed copy was edited, and no commit was made.
