# Resolver receipt: `unblock/adint/caffb11f72d6e85e/resolve`

- Checked: `2026-09-12T03:41:29Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve` (owner `haunt`)
- Result: **the queued missing-input diagnosis is stale; frozen inputs exist, but the parent remains blocked on experiment contract**

The frozen five-field selection, hashes, and measured A08 result are recorded in
`docs/task-receipts/unblock-adint-d28e9f7777f2e7dd-resolve-20260912.md` and
`docs/task-receipts/haunt-dictionary-experiment-contract-20260912.md`. The latter explicitly
limits the A08 result to a synthetic five-substitution fixture and declares it `INCONCLUSIVE` for
broader correction behavior; it is not evidence of BbyWVY dictionary behavior.

Fresh checks:

- `rtk mesh-task status unblock/haunt/fd5d75268b44e1cc` reports `blocked`, owner `haunt`, blocker
  `experiment-contract`.
- `rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt` exits 2.

Do not rerun `scripts/bbywvy_test.py` as dictionary evidence or resume the haunt-owned row. Its owner
must amend the parent claim to the A08-only result with its `INCONCLUSIVE` limit, or produce a
BbyWVY-compatible dictionary arm and comparison. The stale operator-input diagnosis is corrected
here; no change is made to the haunt-owned task.
