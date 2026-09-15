# Correlation investigation: `tempo=SILENT` → `psi=STALLED`

Date: 2026-09-08  
Disposition: **spurious as a causal/useful fused sense; discard.** No fused
sense and no reflex.

## Queued result and reproducibility

The queued result was the already-recorded 2026-09-07 candidate: lift 3.72,
14 episodes / 12 one-hour-collapsed occasions, 380 usable rows over 1297.7 h;
the tempo-hour shadow scored 1.23, while the full-window 2.2 was explicitly the
confounded number corrected away. Its stable-blanket split was 2 of 4
environments over the 1.8 floor (1.92, 1.50, 0.96, 1.83), so it is a
Markov-blanket hypothesis only and its seed must remain withheld.

On the current tape (`~/.mesh/sensor-tape.tsv`, 4,801 data rows through
2026-09-08T21:50:01Z), a normal `bash scripts/mesh-correlate --dry` and
`--stable` no longer emit this pair. The current candidate stream contains
other unstable pairs, not `tempo=SILENT` ↔ `psi=STALLED`. That is consistent
with the queued relation being an intermittent historical regime, not a live
coupling.

## Reality check

The producers measure different domains. `scripts/mesh-activity-tempo` defines
`SILENT` from quiet/no-motion plus dark context; when phone axes are unavailable
it records the missingness explicitly. The current
`~/.mesh/activity-tempo.log` entries show, for example, `RESTING` or `BUSTLE`
with `tamper=UNKNOWN wifi=UNKNOWN`, and the dark no-motion sample is
`cam=STILL`, not a host-health assertion. The underlying room-sense tape also
shows phone/BLE/body degradation while camera and ambient readings continue.

`scripts/mesh-psi` defines `STALLED` from host CPU/I/O/memory pressure and
attributes the dominant kernel resource. A current direct read returned
`level=CALM`, `cpu_some=5.96`, `io_some=0.12`, `mem_some=0.00`, with a full
331-second interval and no resource/thread stall to attribute. Thus a room
quietness label cannot explain the independent kernel contention label.

The historical overlap is therefore best explained by shared night,
availability, and workload regimes: the exact relation is environment-specific,
fails the stable-blanket test, and does not survive as a current candidate.

## Decision

Discard in one line: `SILENT` is a degraded/night room-motion classification,
while `STALLED` is independent host kernel contention; their clustered,
environment-specific overlap is shared sensing/workload regime, not a causal
signal worth fusing or reflexing.

## Verification

- `bash scripts/mesh-correlate --dry` and `--stable` ran read-only on the current
  tape; neither emitted this pair.
- `bash scripts/mesh-correlate --test` passed.
- `bash scripts/mesh-psi --test` passed; the live JSON read returned `CALM` with
  interval coverage and no stall attribution.
- The current tempo live/test path was bounded with `timeout 25s` and did not
  return; this is recorded as unavailable evidence, not converted into a
  positive or negative tempo reading. Existing dated producer logs were used
  instead.
- No mesh tool, deployed copy, queue entry, or reflex was edited. No commit was
  made; this artifact is intentionally left uncommitted for the steward.
