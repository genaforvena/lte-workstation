# witness TOP pane: labour as a self-balancing tree — design (2026-07-24)

Operator direction (direct conversation, 2026-07-24, following the stuck-strands cleanup on the
same pane): the witness TOP (TAPE) pane should present `chat.log`/`spend.log` as an hledger-style
double-entry accounting system that **self-balances around labour spent** — not just report a
one-line labour summary alongside two other one-line ledger summaries. Builds on the third-axis
labour ledger (`mesh-labor`, commodity `TURN`) and the "board as a game" chart-of-accounts doctrine
already landed per `docs/design-hledger-coordination-2026-07-24.md`.

## Thesis

`mesh-labor --budget` already answers "who's spending labour right now" (rolling 5h, per window,
matching the "windows ARE the accounts" doctrine applied to it 2026-07-24). What it doesn't do is
show the double-entry **balance property** — the structural checksum that two independent totals
(labour expended vs budget drawn down) must sum to zero, which is the actual payoff of framing this
as hledger rather than a plain report (`docs/design-hledger-coordination-2026-07-24.md`: "a free,
structural CHECKSUM on every ledger the mesh keeps"). The witness pane should make that visible as
the PRIMARY view, not bury it in a one-liner.

## Non-goals

- Not touching the hledger journal / chart of accounts (`~/.mesh/labour/*.journal`,
  `expenses:labour:<prov>:<window>`) — this is a new **rolling-window** renderer sourced the same
  way `--budget` already is (direct `spend.log` tally; hledger's day-granular dates can't do
  sub-minute rolling windows, per `mesh-labor`'s own header comment). The committed all-time journal
  and its existing `--balance` output are unchanged.
- Not changing `mesh-promises` or `mesh-ledger` content or their cadence — they move position on the
  pane (demoted below labour) but render identically to today.
- Not changing the BOARD half of the fused witness pane (board churn / claims / digest gaps — just
  fixed 2026-07-24) or the sparkline measurement block at the top of the TAPE half.
- Not adding a cache file. `mesh-labor --budget` measured at 35ms (pure file read + tally, no
  git/hledger fork) — cheap enough to call live every render tick, same as the sparkline block
  already does. No new staleness class to reason about.

---

## Component 1 — mesh-labor: rolling self-balancing tree renderer

**What it does:** adds `mesh-labor --balance --rolling`, a new output mode alongside the existing
`--balance` (all-time, hledger-sourced) and `--budget` (rolling 5h table). Computes the same
rolling-5h per-window tally `do_budget` already computes (refactored into a shared function so both
renderers read one source of truth — no duplicate tally logic, no drift risk between the two views),
and prints it as an explicit Dr/Cr tree instead of a cap/burn/projection table:

```
assets:budget            -43 TURN
expenses:labour            43 TURN
  tg                       12
  genome                    8
  witness                   6
  senses                    5
  sound                     4
  pub                       3
  discover                  2
  vpn                       1
  health                    1
------------------------------
                            0
```

**Breakdown: window only**, no provider nesting — matches the "windows ARE the accounts" doctrine
already applied to `--budget`'s primary table (provider is which engine a window runs on, not the
budgeted thing).

**The trailing `0` is computed, not printed.** Sum the window totals (`expenses:labour`) and negate
it against the budget drawdown (`assets:budget`); if a future refactor of the tally introduces an
asymmetry (e.g. a window's turns counted twice, or a provider's spend dropped), the line reads
non-zero and the pane visibly shows a broken books — the same double-entry error-detecting property
`mesh-ledger`/`mesh-promises` already rely on, extended to the rolling view.

**Interface:** `mesh-labor --balance --rolling [--window-hours N]` (defaults to
`MESH_LABOR_WINDOW_H`, same env var `--budget` already reads). Existing `--budget`, `--balance`,
`--dash`, `--json`, `--branch`, `--availability` etc. unchanged.

## Component 2 — mesh-witness: pane reorder

**What it does:** in `mesh-witness`'s pane renderer, replace the current
`-- labour ledger (mesh-labor · labour-time · rolling 5h budget) --` one-liner block (today: cats
the cached `.labor-summary` file) with a live call to `mesh-labor --balance --rolling`, and move it
**above** the promise ledger and resource ledger sections (both unchanged in content, just demoted
to thin footer lines below labour). Sparkline measurement block (nodes/minds/board-lines/senses/
paid-turns with sparklines) stays first, unchanged. Raw `witness.log` row tail stays last, unchanged.

```
-- latest measurement --                              (sparklines, unchanged, still first)
  ...

-- labour ledger (mesh-labor · rolling 5h · self-balancing) --      (NEW: primary view)
  assets:budget            -43 TURN
  expenses:labour            43 TURN
    tg                       12
    ...
  ------------------------------
                              0

-- promise ledger (mesh-promises · unkept board obligations) --     (unchanged content, moved down)
  promises: 6 open · 1 LEAKED · ...
  leaked (drive owner: pick-up-or-retire):
  ...

-- resource ledger (mesh-ledger · double-entry) --                  (unchanged content, moved down)
  ledger: inference(imputed) $658.29 · ...

-- ledger tail (last N of M rows) --                                (unchanged, still last)
  ...
```

**Failure mode:** if `mesh-labor --balance --rolling` errors or times out, the section renders
`(labour tree render FAILED — this frame BLIND, not all-clear)` rather than silently dropping the
section — same loud-not-silent convention `mesh-dash` already uses for the whole TAPE half when
`mesh-witness` itself fails.

**Interface:** no CLI change to `mesh-witness --pane`/`--embed` — this is an internal render-order
and content change to the existing labour section.

## Component 3 — testing

- `mesh-labor --test`: new RED-first case for `--balance --rolling` — assert the output ends in a
  bare `0` line; mutate the shared tally function (drop one window's count from the expenses side
  only) and assert the balance line goes non-zero, proving the checksum is computed from the same
  data it displays, not printed-and-trusted (the "gate must assert your code, not the model's mood"
  / "non-empty is not correct" doctrine — a tree that always prints `0` regardless of input asserts
  nothing).
- `mesh-witness`'s own test path (driven via `mesh-dash --test`'s TAPE-half assertions, lines
  ~39-52): extend to assert the labour section header and trailing `0` line appear in a live
  `--pane` render, and that the FAILED-render fallback text appears when `mesh-labor` is forced to
  fail (a real mutation, not a happy-path-only check).
- `mesh-dash --test` (the fused-pane smoke test): no change needed — it already asserts both TAPE
  and BOARD halves render non-empty and drives through `mesh-witness --pane`, so it exercises this
  transitively.

## Rollout

Edit `scripts/mesh-labor` (Component 1) and `scripts/mesh-witness` (Component 2), run
`mesh-labor --test` and the `mesh-witness` test path green, render `mesh-dash --once witness` live
to eyeball the pane, deploy both to `~/.local/bin`, leave uncommitted in the tree for the next
`mesh-land` pass (same settle-then-land pattern used for the stuck-strands fix earlier today).

## Open question (not blocking, parked)

`--window-hours` on the new flag defaults to `MESH_LABOR_WINDOW_H` (mesh-wide rolling window, today
5h) — if the operator wants the PANE specifically to use a different granularity than `--budget`'s
cap-tracking window, that's a follow-up, not scoped here.
