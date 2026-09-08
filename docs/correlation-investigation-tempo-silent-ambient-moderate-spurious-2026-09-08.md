# Correlation investigation: `tempo=SILENT` ↔ `ambient=MODERATE` — spurious

Date: 2026-09-08  
Disposition: discard; no fused sense and no reflex.

## Finding

The queued result (lift 3.8, 8 occasions / 8 episodes of 171, 815.7 h) is
not a room-level coupling. It is the same regime-shift case previously
reproduced from the source tape: `tempo=SILENT` was unreachable until the
light path began producing `DARK`, so the full-window denominator treated a
short late regime as if it had 34 days of exposure.

The historical producer artifact records the exact queued statistic and its
correction: before the SILENT era, the token had no history; inside its own
era the episode lift was 1.00. Conditioning on any readable tempo gave
`P(MODERATE)=0.972`, versus 0.963 when tempo was SILENT (lift 0.99). The
source record is `~/.mesh/knowledge/correlation-investigation-tempo-silent-ambient-moderate-spurious-2026-08-17.md`.

## Current re-audit

The current `~/.mesh/sensor-tape.tsv` contains 4,776 aligned rows from
2026-07-14T22:40:01Z through 2026-09-08T18:10:02Z. It has 246 SILENT tempo
rows, 1,128 MODERATE ambient rows, and 113 row-level overlaps. The overlaps
are concentrated in the original 2026-08-15–19 regime and later isolated or
clustered episodes; they do not form a stable all-window relation. A simple
one-hour-gap collapse of the current overlap gives 18 occasions, not the
queued eight, because the tape has since grown and added later clusters.

The live producer logs explain the labels rather than corroborating a causal
mechanism. `scripts/mesh-activity-tempo` emits SILENT from dark-room/no-motion
conditions and its historical SILENT transitions are explicitly accompanied
by `wifi=UNKNOWN` or `wifi=UNCERTAIN`, with phone/tamper axes frequently
unavailable. `scripts/mesh-ambient-clock` derives the ambient-clock label from
BLE/appliance presence history, not the room microphone. The corresponding
`~/.mesh/activity-tempo.log` and `~/.mesh/room-sense.log` show the dense
2026-08-15–19 interval as phone-unreachable/body-unknown/camera-blind in many
rows while the ambient-clock label remains MODERATE. That is shared sensing
availability plus a short instrument regime, not “silent room causes
moderate ambient.”

The label names are also easy to misread: this `ambient` tape column is the
ambient clock / BLE-appliance sense, whereas the room-sense log separately
reports microphone `ambient=` values. Fusing the two would therefore combine
an activity classifier with an independently derived social-clock label and
would amplify the shared-organ confound.

## Decision

Discard in one line: `tempo=SILENT` became readable only in a late,
phone/light-gated sensing regime, while `ambient=MODERATE` is an independent
BLE/appliance clock label; their short overlap is regime and availability,
not a useful causal signal.

## Verification

- `bash scripts/mesh-correlate --test` passed.
- `bash scripts/mesh-activity-tempo --test` passed.
- `bash scripts/mesh-ambient-clock --test` passed.
- `CORRELATE_REGIME_GATE=0 CORRELATE_STABLE_GATE=0 bash scripts/mesh-correlate --dry`
  was run read-only; no queue was written. A normal gated `--dry` run also
  produced no candidate for this pair; the historical source artifact records
  the regime-gate rejection of the original queued statistic.
- Counts and timestamps were independently read from
  `~/.mesh/sensor-tape.tsv`; label provenance was checked against the genome
  sources and the live producer logs named above.
- No mesh tool or deployed copy was edited. No commit was made.
