# Receipt: `sound-experiments-20260908/min-beats-material-cost`

Date: 2026-09-08 22:24–22:27 UTC  
Owner: sound  
Status: measured; no threshold change recommended

## Live instruction/code audit

The board task was open in `docs/plans/2026-09-08-sound-experiments-ledger.tsv` and
`docs/audits/operator-status-model-20260908.tsv` at start, so it was not stale.

Current deployed/source code still has the two relevant gates:

- `scripts/mesh-sound-reflex:322`: `SR_MIN_BEATS` defaults to 3.
- `scripts/mesh-sound-reflex:356` and `scripts/mesh-sound-reflex:2877-2878`:
  `beats >= MIN_BEATS` **and** `beats/window >= 0.8`.
- `scripts/mesh-soundscape:81-82`: the analyzer-side default remains `SS_MIN_BEATS=4`,
  `SS_MIN_DENSITY=0.8`.

That distinction matters: lowering the reflex consumer floor alone would not make a two-beat,
three-second candidate eligible when its density is only 0.667 beats/s.

## Fresh same-window corpus

Corpus: records from 22:00:00 through 22:24:00 UTC, restricted to `win=3.00`, before this
receipt. Material strata are the live organ/duration classes: `ear` is the 18.00s VAD-railed
material; `note3` is the real segmented material (11.40–11.80s in this sample).

| stratum | n | beats >= 3 | beats >= 2 | exactly 2 | gate at MIN_BEATS=3 | gate at MIN_BEATS=2 |
|---|---:|---:|---:|---:|---:|---:|
| 18s VAD-railed (`ear`) | 33 | 33 | 33 | 0 | 33 | 33 |
| real segmented (`note3`) | 2 | 1 | 1 | 0 | 1 | 1 |
| total | 35 | 34 | 34 | 0 | 34 | 34 |

The eligible pool changes by **0/35 overall (0 percentage points)**, and by **0** in each
stratum. The one ineligible segmented row has one beat, not two; all 18s VAD-railed rows clear
both floors in this fresh window.

The density arithmetic independently blocks a two-beat 3s fragment: `2 / 3 = 0.667 b/s < 0.8`.
Therefore changing the beat floor from 3 to 2 would not admit the requested material under the
current coupled gate.

## Two-beat render/listen artifact

The fresh corpus contained no two-beat source, so I used the retained real two-beat source
`~/.mesh/records/20260810-220142-drop-67c31658.wav` (`dur=2.97`, `win=2.97`, `beats=2`).
`SS_MIN_BEATS=2 mesh-soundscape --measure` re-read it as `beats=2`, `fbeats=2`, `score=56.0`.

Rendered output:

`/home/mesh-home/grainneukeln/output/l1500_w4_ss1.25_s2.0_c300-12000_k3_n8_2026_09_08_2225.mp3`

Evidence:

- `mesh-room-music --remix` returned the output path successfully.
- `mesh-song-verify <render> <render>`: `SONG ok`, `beats=1.67`.
- Local `ffplay -nodisp -autoexit`: rc 0 (decoded/played successfully).
- `mesh-room-music --play` could not push to the room node: `play: push to room node failed`.
  This is a delivery limitation, not a fabricated listen claim.

## Verification and verdict

`mesh-soundscape --test` reached its analyzer, measure, ACI, and none-reason checks. The
`mesh-sound-reflex --test` was honestly blocked with rc 2 because a live reflex tick held
`~/.mesh/records.log.reflex.lock`; I did not disrupt the active writer.

Recommendation: **keep `MIN_BEATS=3`**. Do not lower it based on two-beat fragments: the fresh
same-window eligible pool does not change, and the current density floor rejects the two-beat
case anyway. A future two-beat experiment would need an explicit density-floor decision and a
fresh real segmented sample, not a beat-floor-only edit.
