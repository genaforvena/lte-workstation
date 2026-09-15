# Unblock receipt — `unblock/tg/d5d46783d677c68e/resolve`

Captured 2026-09-12T00:14Z UTC by owner `tg`.

## Result

The blocker text was stale about missing collage helpers. The source already contains `valid_source`,
`cut_window`, `collage_build`, the detached `launch_grind`, and the collage tick path. This audit
reconciled all six plan tasks in `docs/design-audit-sound-collage-checklist-20260907.md` and completed
the missing live-evidence gate: one bounded live tick built and ground a random ambient collage. The
fresh MP3 is present, decodes fully, and matches the reflex-owned settled ledger and params rows.

## Six-task reconciliation

| plan task | disposition | evidence |
|---|---|---|
| 1 `valid_source` | DONE | Current source/test; near-silent valid input accepted and empty/corrupt input rejected. Mutation-red evidence is summarized in the 2026-09-11 `d7120dfa` receipt. |
| 2 `cut_window` | DONE | Current source/test; bounded, varying offsets. Fixed-window mutation dies in the `d7120dfa` receipt. |
| 3 `collage_build` | DONE | Current source/test; random valid-source subset and shuffled feed. Single-part mutation dies in the `d7120dfa` receipt. |
| 4 `launch_grind` | DONE | Detached launcher exercised by prior sandbox receipt and fresh live render. |
| 5 collage `tick` path | DONE | Prior sandbox ledger settles selected/non-selected rows; fresh live params and ledger identify collage seed and blended inputs. |
| 6 recipe/verdict/deploy | DONE | Fresh source smoke pass, matching deployed hash, cron wiring, settled MP3 with media validation. |

The prior mutation-red and sandbox-dry-run evidence is retained at
`docs/task-receipts/unblock-tg-d7120dfa529d79f6-resolve-20260911.md`. The sound source was not changed
between that verification and this pass.

## Fresh live verification

- `timeout 180s mesh-sound-reflex`: `rc=0`; tick artifact mtime `2026-09-12 00:08:29Z`.
- `room-music-params.log` row at `2026-09-12T00:08:50Z` records
  `src=collage/083ad98e parts=083ad98e,223db7ed,4b5f916a cuts=0:8,6:12,6:8`.
- `records.log` settles `ear 083ad98e` to
  `ground:l120_w5_ss0.25_s0.25_c100-8000_m-poly_k3_n8_st2+3_2026_09_12_0008.mp3`; the other
  selected inputs settle `blended:083ad98e`.
- MP3: `/home/mesh-home/grainneukeln/output/l120_w5_ss0.25_s0.25_c100-8000_m-poly_k3_n8_st2+3_2026_09_12_0008.mp3`;
  4,482,656 bytes; SHA-256 `391880bd1c4097557ef4a137a5dae0ef15f9a035c16a38787dedda101641aae3`;
  `ffprobe` duration 112.039184s; full `ffmpeg -f null -` decode `rc=0`.
- `timeout 150s bash scripts/mesh-sound-reflex --test`: `rc=0`, ending `smoke-test: ok`.
- Source and deployed SHA-256 both
  `030160982a5f9324b68a9677c728e32a0d6ddc27b5afae004dcdb8361324ce44`.
- `~/.mesh/reflexes.cron:144` contains the load-gated `*/10` sound-reflex wiring.

## Disposition

Resolver prerequisite satisfied. The exact parent audit step is eligible for resumption after this
resolver is settled; it should continue from the six-task reconciliation, not repeat the live tick.
No production source change was needed.
