# Resolver receipt: `unblock/adint/19da47a3a387df26/resolve`

- Checked: 2026-09-12 UTC
- Actor: `adint`
- Referenced row: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Disposition: the dispatch row's `operator-input` diagnosis is stale; the remaining requirement is an experiment-contract decision owned by Haunt.

## Finding and exact prerequisite

Frozen dictionary inputs now exist in the selected manifest and materialized corpus documented by
`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-a08-scope-amendment-20260912.md` and
`docs/task-receipts/haunt-dictionary-experiment-contract-20260912.md`. The inputs are not enough to
support the broader BbyWVY behavior claim: the A08 result is a synthetic five-substitution fixture,
and `scripts/bbywvy_test.py` is only a six-case runtime smoke with no dictionary arm.

The exact remaining prerequisite is Haunt's owner-authored choice of one of these scopes:

1. amend the parent claim and closure criterion to the frozen A08-only result, preserving its
   `INCONCLUSIVE` limit for broader behavior; or
2. retain the BbyWVY dictionary-behavior claim and first identify and measure a BbyWVY-compatible
   dictionary arm against the frozen manifest and corpus, with a declared comparison, output hashes,
   and typed verdict.

The existing experiment-contract receipt records this condition and explicitly forbids treating the
runtime smoke as dictionary evidence. No dictionary input is missing, so asking the operator to
resupply or refreeze those inputs would be inaccurate. I did not change Haunt's claim or run its
study.

## Verification

- `rtk mesh-task status unblock/haunt/fd5d75268b44e1cc` reported the parent still blocked as
  `experiment-contract` with the exact retry condition above.
- Read `docs/task-receipts/haunt-dictionary-experiment-contract-20260912.md`, which records the
  frozen manifest/corpus hashes and the limit of the existing A08 evidence.
- `rtk mesh-task check dispatch unblock/adint/19da47a3a387df26/resolve adint` exited 0 before take.
- No Haunt-owned task, source input, study result, or project file was changed.
