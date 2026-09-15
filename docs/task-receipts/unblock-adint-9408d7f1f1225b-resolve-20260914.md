# Routing-shadow resolver audit — 2026-09-14

Task: `unblock/adint/9408d7f1f1225b/resolve`

## Finding

The target `unblock/witness/35ba3fdf2a36b891/resolve` is already rejected, and its parent
`self-review-routing-shadow-20260914/independently-evaluate-routing-shadow` remains blocked on the
frozen evaluation gate. The trial began at `2026-09-14T16:52:06Z`; it requires at least 14 days and
100 eligible shared/unowned tasks. The earliest valid review is after `2026-09-28T16:52:06Z` if all
100 tasks exist. Otherwise the required terminal verdict is INCONCLUSIVE by `2026-10-14T16:52:06Z`.

I inspected the live task ledger, task queue, scorer implementation and registration references. The
scorer is present as `scripts/mesh-task-routing-shadow`; there is no missing code or mesh-owned
registration prerequisite that can supply elapsed time or genuine eligible shared/unowned tasks.
Creating synthetic eligible work would violate the frozen sample definition. The existing exact-owner
follow-up `routing-shadow-resolver-followup-adint-20260914/review-frozen-gate-after-parent-completion`
is already recorded with `waiting_for` set to the blocked witness evaluation, and its task plan covers
review after that parent reaches a terminal state. No duplicate successor or early comparison is
warranted.

## Fresh verification

- `mesh-task check dispatch unblock/adint/9408d7f1f2f1225b/resolve adint` exited 0, then the
  owner-authored take claimed this resolver.
- `mesh-task status self-review-routing-shadow-20260914` still shows steps 1–3 done and the witness
  evaluation blocked on its frozen external event.
- Re-ran `scripts/mesh-task-routing-shadow` at `2026-09-14T17:52:46Z`; it exited 0 with
  `candidates=0 excluded=0 report_rows_written=1 decision=collecting`.
- The latest report row records `elapsed_days=0.0421`, zero eligible tasks in both baseline and shadow,
  null wait/completion comparisons, zero protected/exact-owner recommendations, and
  `production_routing_changed=false`. Source coverage is 64,934 chat lines, 55,746,298 bytes, zero
  malformed task events, SHA-256
  `8a2672b8fd335e5621ecd17417f4b48fc5c078355a01d22e0045cbf8afef5f98`.
- Raw report `/home/mesh-home/.mesh/self-review-routing-shadow/reports/routing-shadow.jsonl` SHA-256:
  `63c3517ba737ddad0d66454dad9bf33dc051d8f2d3fb5942ffbfbef725c236dd`.
- `python3 tests/test-mesh-task-routing-shadow.py` passed all 9 tests.

## Disposition

The audit result is ready, but the resolver could not be closed in the structured task ledger. After
the owner-authored take, the canonical chat log no longer contains this chain: a fresh
`mesh-task check dispatch unblock/adint/9408d7f1f1225b/resolve adint` returned exit 3 (untracked), and
`mesh-task done` refused with exit 2 because the chain is absent. I did not record a false completion.

Keep the witness parent blocked and preserve its retry and terminal deadline. The existing wait-for
successor remains responsible for checking the parent's eventual outcome; at the next review, rerun
the scorer and evaluate the frozen gate only after both the time and sample thresholds are satisfied.

## Resume attempt — 2026-09-14T18:10Z

The operator resurfaced the still-open `[taking]` claim. Rechecked the current source of truth before
trying to close it:

- The canonical `/home/mesh-home/.mesh/chat.log` no longer contains the resolver's `[task-ledger]`,
  `[task]`, or `[taking]` records. Its only matches for this ID are the 18:00 FYI and 18:01 handoff.
- `mesh-task status unblock/adint/9408d7f1f1225b` reports that the chain is absent from `chat.log`.
- There is no matching `task-chains/unblock__adint__9408d7f1f1225b.json` cache to import; the
  overflow log also has no copy of the missing structured history.
- The artifact-backed blocker result above still stands, but a terminal task-ledger transition cannot
  be appended safely without the canonical prior state and revision sequence. Reconstructing that
  state from the FYI would invent ledger history.

Disposition: release the resurfaced claim with `[yield]`, citing this receipt. Do not claim `[done]`
unless the ledger source is restored from an authoritative copy and its task transition verifies.
