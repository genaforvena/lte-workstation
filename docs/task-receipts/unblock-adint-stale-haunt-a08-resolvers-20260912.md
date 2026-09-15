# Duplicate Haunt A08 resolver dispatches — 2026-09-12

This evidence applies to these adint-owned duplicate resolver rows:

- `unblock/adint/d460847a782135b7/resolve`
- `unblock/adint/5ec79ac25a2b8488/resolve`
- `unblock/adint/be412a44d95994aa/resolve`

Each dispatch row describes the same stale `operator-input` blocker for
`unblock/haunt/62c0662129fa8ee9/resolve`. Live status reports the Haunt-owned parent complete
under the A08-only scope amendment, with final artifact
`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-a08-scope-amendment-20260912.md`. The frozen
source, languages, normalization, version, and corpus are recorded there. The result is limited to
the five-substitution synthetic fixture (120/120 exact); it leaves broader behavior `INCONCLUSIVE`.

The parent resume gate exits 2 because the parent resolver is already complete. No operator input,
additional A08 dictionary work, or change to Haunt-owned state is required for these duplicate
rows. The distinct broader BbyWVY question remains blocked on its experiment contract and is
documented in `docs/task-receipts/haunt-dictionary-experiment-contract-20260912.md`.

Verification: `rtk mesh-task check dispatch` exited 0 for each listed row under owner `adint`;
live parent status was complete; the parent resume check exited 2. The duplicate rows are settled
against this evidence without changing the Haunt-owned parent.
