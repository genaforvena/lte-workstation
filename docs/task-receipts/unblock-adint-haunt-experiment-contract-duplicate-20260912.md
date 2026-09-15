# Haunt dictionary experiment-contract resolver — 2026-09-12

- Adint resolver: `unblock/adint/9ad8f3d639dad6c8/resolve`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Parent owner: `haunt`

The parent remains blocked as `experiment-contract`. The A08 fixture is a five-substitution
synthetic test (120/120 exact, identity 0/120) and its verdict remains `INCONCLUSIVE` for broader
behavior; the BbyWVY smoke has no dictionary arm. The exact next condition is Haunt's owner-authored
choice: narrow the parent claim to the A08 result with the `INCONCLUSIVE` limitation, or keep the
BbyWVY claim and first implement/measure a compatible dictionary arm against the frozen
manifest/corpus with a declared comparison and typed verdict. Do not re-request the frozen inputs or
use `scripts/bbywvy_test.py` as dictionary evidence.

This row repeats a condition already diagnosed in
`docs/task-receipts/unblock-adint-19da47a3a387df26-resolve-20260912.md` and
`docs/task-receipts/haunt-dictionary-experiment-contract-20260912.md`. The owner-scoped dispatch
check for this resolver must exit 0 before it is settled. No Haunt-owned claim, input, or study was
changed.
