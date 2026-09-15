# Unblock receipt — `unblock/tg/d7120dfa529d79f6/resolve`

Captured 2026-09-11T23:00Z UTC by owner `tg`.

## Result

The resolver text is partly stale: the collage implementation is present in
`scripts/mesh-sound-reflex`. The parent
`design-audit-task-sweep-20260907/plans-sound-collage` still cannot close until
the live owner-run collage produces a settled ledger/MP3 receipt. This turn
verified the existing gates and the sandbox tick wiring; it did not create or
claim a live render.

## Evidence

- `bash -n scripts/mesh-sound-reflex`: passed.
- `timeout 120s bash scripts/mesh-sound-reflex --test`: `rc=0`, ending
  `smoke-test: ok`; captured output `/tmp/msr-base.U66ULJ`, SHA-256
  `a9bff65c24a30d8ff27f12e202761b847dc672cd43ad516d49d84832c736af4e`.
- Mutation-red for the actual source guard: a scratch copy changed the duration
  predicate to unconditional rejection. Its full `--test` run returned nonzero
  and reported `FAIL: valid near-silent source was rejected`; output
  `/tmp/msr-mut-valid2.rBUwCu.out`, SHA-256
  `61b2fad466934b4022bbf89ecf33e6cd2af2b2f018ab4e3108f2808605549a72`.
- Mutation-red for random cuts: a scratch copy pinned the cut to offset 0 and
  length 6. Its full `--test` reported `FAIL: cut_window produced one fixed
  window`; output `/tmp/msr-mut-cut2.54IYua.out`, SHA-256
  `90accb48dcff8195fff71198c741cdf062e7b4ffa5dd79a72865b708f82cbece`.
- Mutation-red for collage selection: a scratch copy forced `K=1` and removed
  the shuffle. Its full `--test` reported `FAIL: collage never selected
  multiple parts`; output `/tmp/msr-mut-collage3.HkLJun.out`, SHA-256
  `be9ba1fd750b2b57162bf67c2951a5ac4e72904e49638baa0552f14f3ddea977`.
- Isolated tick dry-run used a private ledger, record directory, and renderer
  stub. `timeout 30s bash scripts/mesh-sound-reflex` returned `rc=0`; the
  ordinary source settled as `grinding`, while the silent source settled as
  `skip:not-selected(random collage)`. Receipt directory:
  `/tmp/sr-dryrun3.VFesSe`; ledger SHA-256
  `89308ceb069f27ffb3f09ca44efdfd5dcf2dc7dea881879bda95891f13b0a9e5`.

## Disposition

Resolver diagnosis and prerequisite verification are complete; no production
source or wiring changes were warranted. The original audit remains blocked
only on a fresh reflex-owned, settled live collage ledger/MP3 receipt and its
media validation. Do not resume/close the original audit until that live
artifact exists. Next action: in a quiet window, capture one eligible live
collage tick and verify its owner ledger row, MP3 SHA-256, `ffprobe`, and full
decode, then reconcile the checklist.
