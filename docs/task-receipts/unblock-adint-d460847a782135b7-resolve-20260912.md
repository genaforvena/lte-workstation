# Resolver receipt: `unblock/adint/d460847a782135b7/resolve`

- Checked: 2026-09-12 UTC
- Actor: `adint`
- Parent referenced by dispatch row: `unblock/haunt/62c0662129fa8ee9/resolve`
- Disposition: stale duplicate; no operator input or additional dictionary work is needed for this parent.

## Finding

The dispatch description still says the parent is blocked on five operator-missing dictionary
inputs. Live state contradicts that description: `mesh-task status
unblock/haunt/62c0662129fa8ee9` reports the Haunt-owned resolver complete, with artifact
`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-a08-scope-amendment-20260912.md`.
That amendment freezes the dictionary source, languages, normalization, version, and corpus, and
limits the completed claim to the synthetic A08 fixture (120/120 exact); broader correction
behavior remains `INCONCLUSIVE`.

The original resolver's live resume check, `rtk mesh-task check resume
unblock/haunt/62c0662129fa8ee9/resolve haunt`, exits 2 because it is already complete. The earlier
adint correction receipt `docs/task-receipts/correction-unblock-adint-be51f6b216e5b0e3-20260912.md`
records the same stale-dispatch condition and evidence.

There is a separate blocked row, `unblock/haunt/fd5d75268b44e1cc/resolve`, for the broader BbyWVY
dictionary-behavior question. Its `experiment-contract` receipt explicitly says the frozen A08
result and six-case runtime smoke do not establish BbyWVY dictionary behavior. That separate
question belongs to Haunt and is not changed or claimed resolved here.

## Verification

- Owner-scoped dispatch returned this row; `rtk mesh-task check dispatch
  unblock/adint/d460847a782135b7/resolve adint` exited 0.
- `rtk mesh-task status unblock/haunt/62c0662129fa8ee9` reported the parent resolver complete.
- The parent resume gate exited 2 as expected for the already-complete row.
- `rtk mesh-task status unblock/haunt/fd5d75268b44e1cc` confirmed the broader experiment-contract
  row remains blocked.
- No Haunt-owned task, dictionary input, study, or project file was changed.
