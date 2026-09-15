# promise-writeoff Component C implementation — suggested-owner-hints — 2026-09-12

- Step: promise-writeoff-implementation-20260912/suggested-owner-hints (owner witness).
- Spec: promise-writeoff-reroute §C, test 6. Read-only charter-overlap suggestions
  for :unrouted rows. This step WROTE code (unlike the prior verify-only step).

## Change (worktree only, NOT landed — autoland task posted for genome)

`scripts/mesh-promises` (+~100 lines):

- `charter_map()` (shell): parses `account expenses:labour:<w> ; duty` rows from the
  same accounts.journal the roster reads (declared, else seed fallback) into
  `window<TAB>comment` lines. Window = last :-segment (covers the
  `expenses:labour:<prov>:<w>` form); comment-free rows skipped. Empty when no chart
  found (fail-open).
- `replay()` env: `MESH_PROMISE_CHARTERS="${MESH_PROMISE_CHARTERS-$(charter_map)}"`,
  mirroring the ROSTER pattern (preset wins, so fixtures stay hermetic).
- Python `CHARTERS` + `suggest_owner(lead)` + `suggest_text(lead)`: unique-best
  token overlap wins using the shared `toks()` tokenizer (Cyrillic-safe, stopwords
  never score); ties and zero-overlap both abstain (`suggest: none`); absent chart
  prints nothing at all.
- Render: `--all` (promise/claim/hold loops) and `--report` (three leak sections)
  append ` (suggest: <w> — overlap: a, b)` / ` (suggest: none — no charter overlap)`
  to UNROUTED rows only. Routed rows untouched. journal/counts/json/check paths
  untouched (read-only — replay never posts).

## Evidence (executed 2026-09-12T03:3xZ)

- `bash -n` clean; `scripts/mesh-promises --test` → rc 0, `smoke-test: ok`
  (new block 57 = spec test 6: unique-best fires, zero-overlap → none, tied-best →
  none with no fabricated pick, routed row silent, --report carries it, absent
  chart silent with compass intact).
- Mutation: expected overlap string altered → suite FAILs rc 1 on the rig row;
  control green. The gate is real, not vacuous.
- Live board: `--all` renders suggestions on real unrouted rows, e.g.
  `mesh-health … (suggest: health — overlap: health)`, zero-overlap rows read
  `(suggest: none — no charter overlap)`.
- Deployed copy `~/.local/bin/mesh-promises` is STALE by construction (source
  uncommitted); landing + deploy is genome's autoland lane (task posted).

## Disposition

Step complete. Remaining chain step: gated-auto-reaction (Component D, separate
scope — needs these suggestion scores plus margin/floor/incident guards).
