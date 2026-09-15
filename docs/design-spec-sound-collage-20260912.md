# Sound-random-collage design reconciliation — 2026-09-12

## Disposition

The 2026-07-17 design matches the current `mesh-sound-reflex` implementation. The ambient path
selects from valid mesh-owned records by random subset and random cuts, includes valid silence,
remeasures the resulting feed for recipe axes, and grinds it through the existing detached path.
The operator-drop path remains privileged and whole-file. No code, media, or cron changes were
needed for this audit.

## Design-to-code map

| Design obligation | Current implementation evidence | Result |
|---|---|---|
| Validity is the only ambient admission gate; silence is allowed | `valid_source()` checks file presence, size, audio stream, and positive duration; comments explicitly admit near-silence | MATCH |
| Randomly choose 1..min(pool, max) records and random cuts; no score/beat floor | `collage_build()` validates the fresh non-drop pool, shuffles indices, draws K and cuts, then copies or concatenates the feed | MATCH |
| Measure the feed for recipe axes, not as an admission gate | `collage_tick()` calls `mesh-soundscape --measure` after building the feed; missing axes use documented defaults and do not reject a valid feed | MATCH |
| Settle every fresh row according to its use | selected non-seed rows become `blended:<seed>`, valid non-selected rows `skip:not-selected(random collage)`, invalid/missing rows get explicit skip verdicts; the seed enters `grinding` before detached render | MATCH |
| Keep detached grinding, provenance, and drop priority | collage path calls `launch_grind` with `src=collage/...` metadata; `tick()` diverts only non-drop blocks to collage and retains the existing operator-drop branch | MATCH |
| Exercise validity, randomness, multi-part collage, and recipe coupling | The current source/deployed `--test` passed in the six-task reconciliation recorded in `docs/design-audit-sound-collage-checklist-20260907.md`; mutation-red receipts are cited there | PASS |

The one-part quiet-window render below is allowed by the design: when a fresh block has one valid
source, K is 1 and the cut is still random. A separate multi-part render proves the production
concatenation path with three contributors.

## Live media and wiring

The multi-part live collage at 2026-09-12 00:08Z used three ambient records. Its settled params row
at `~/.mesh/room-music-params.log:4729` records
`src=collage/083ad98e parts=083ad98e,223db7ed,4b5f916a cuts=0:8,6:12,6:8`; the seed's source row
at `~/.mesh/records.log:2037` settles as `ground:<render>` and the other selected rows were
settled as `blended:<seed>` in the earlier live audit.

- MP3: `/home/mesh-home/grainneukeln/output/l120_w5_ss0.25_s0.25_c100-8000_m-poly_k3_n8_st2+3_2026_09_12_0008.mp3`
- Size: 4,482,656 bytes; duration: 112.039184s; SHA-256:
  `391880bd1c4097557ef4a137a5dae0ef15f9a035c16a38787dedda101641aae3`
- `ffprobe` identified MP3 and the stated duration/size; full `ffmpeg -f null -` decode returned rc 0.

A later one-source quiet-window render at 00:40Z proves the single-source boundary and its recorded
provenance: `records.log:2110` settles source `68367792` to
`l120_w4_s0.25_c80-15000_m-poly_k3_n8_st3_2026_09_12_0040.mp3`, while
`room-music-params.log:4736` records `src=collage/68367792 parts=68367792 cuts=7:5`.

- MP3: `/home/mesh-home/grainneukeln/output/l120_w4_s0.25_c80-15000_m-poly_k3_n8_st3_2026_09_12_0040.mp3`
- Size: 802,525 bytes; duration: 20.035918s; SHA-256:
  `5864126586e816ead1ffd519b4747bfd3c1187a9e4fd7f1dc73f0119a1982ed5`
- `ffprobe` identified MP3 and the stated duration/size; full `ffmpeg -f null -` decode returned rc 0.

Current `scripts/mesh-sound-reflex` and `/home/mesh-home/.local/bin/mesh-sound-reflex` match at
SHA-256 `030160982a5f9324b68a9677c728e32a0d6ddc27b5afae004dcdb8361324ce44`. Live wiring remains
the load-gated `*/10` entry at `/home/mesh-home/.mesh/reflexes.cron:144`, matching the source's
declared cadence.

## Final result

The implementation, current test receipt, deployment wiring, settled ledger rows, and two playable
real MP3s cover the design's current obligations. The previous blocked audit is superseded by the
2026-09-12 fresh owner evidence in `docs/design-audit-sound-collage-checklist-20260907.md`; no
remaining sound-collage implementation obligation was found in this spec review.
