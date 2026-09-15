# Unblock receipt — `unblock/tg/bc9722e64e8166d4/resolve`

Captured 2026-09-11T22:28Z UTC by owner `tg`.

## Result

The implementation is present and source/deployed parity holds. The missing mutation-red
acceptance evidence was captured in a quiet window. The resolver remains partially blocked on
the separate requirement for a fresh reflex-owned settled collage MP3 plus ledger/params receipt.

## Evidence

- `mesh-dash --once tg`: voice-rx/textin/pane live; inbound state is `HEARING`, queue=0.
- `mesh-task check dispatch bc9722e64e8166d4 tg`: `rc=0`; task was taken with
  `MESH_TASK_ACTOR=tg`.
- `scripts/mesh-sound-reflex --test`: `rc=0`, `smoke-test: ok`; output SHA-256
  `a9bff65c24a30d8ff27f12e202761b847dc672cd43ad516d49d84832c736af4e`.
- Source/deployed SHA-256 match:
  `030160982a5f9324b68a9677c728e32a0d6ddc27b5afae004dcdb8361324ce44`.
- `valid_source` mutant: `rc=1`, red `FAIL: valid near-silent source was rejected`; output
  SHA-256 `61b2fad466934b4022bbf89ecf33e6cd2af2b2f018ab4e3108f2808605549a72`.
- `cut_window` fixed-window mutant: `rc=1`, red `FAIL: cut_window produced one fixed window`;
  output SHA-256 `90accb48dcff8195fff71198c741cdf062e7b4ffa5dd79a72865b708f82cbece`.
- `collage_build` fixed-selection mutant: `rc=1`, red selection-collapse and no-multi-part
  failures; output SHA-256 `d25b0023e3382f5d494a91dd45458decaca1507900ec5116e16a5536f8c03f43`.
- Full captured outputs remain at `/home/mesh-home/.mesh/tg-receipts.Mx7l9o/{source,valid,cut,collage}.out`.

## Disposition

`PROGRESS/PARTIAL`: mutation-red evidence is now real and artifact-backed. Do not close the
parent sound-collage audit yet. Exact next action: during the next quiet window capture a fresh
reflex-owned settled collage MP3, ffprobe/full-decode it, record the matching ledger and params
row, then rerun the six-task checklist.
