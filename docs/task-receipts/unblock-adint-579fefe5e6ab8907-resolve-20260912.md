# Resolver receipt: `unblock/adint/579fefe5e6ab8907/resolve`

- Checked: 2026-09-12 UTC
- Actor: `adint`
- Parent blocker: `unblock/haunt/fd5d75268b44e1cc/resolve` (owner `haunt`)
- Result: **original `operator-input` diagnosis is stale; broader BbyWVY dictionary behavior remains blocked on experiment contract**

## Evidence

The five requested dictionary inputs are now frozen in Tiny Fleet's
`docs/task-receipts/adint-operator-authorized-dictionary-input-20260912.md` (SHA-256
`c441c0bf969cbe50a177cdf04b842c97193f30c3a6746ae0fd2f32dc604fe31a`). That receipt records
the source, languages, exact normalization, immutable commit, and 152-row corpus hash, plus a
measured synthetic A08 result. The owner-authored scope amendment
`docs/task-receipts/haunt-a08-scope-amendment-20260912.md` (SHA-256
`dc3258137018f05c1912dd29e165d77e44a26f0acf2b86f208d3a11e44053bcf`) narrows the parent claim
to that fixture and keeps broader correction behavior and BbyWVY dictionary behavior explicitly
`INCONCLUSIVE` / unproven.

Live checks at 2026-09-12 show:

- `haunt-install-unblock-20260907/install-and-retry-tinyfleet` is complete with the A08 scope
  amendment as its artifact.
- `unblock/haunt/fd5d75268b44e1cc/resolve` remains blocked as `experiment-contract`; its retry text
  requires either the parent claim to be narrowed to A08 with the inconclusive limit, or a
  BbyWVY-compatible dictionary arm against the frozen inputs.
- `mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt` exits 2. Adint does not
  resume or mutate the haunt-owned resolver.

The existing six-case `scripts/bbywvy_test.py` smoke is not dictionary evidence and was not rerun.
The A08 measurement closes only the amended synthetic-fixture criterion; it does not establish
BbyWVY dictionary behavior.

## Exact next action

The `haunt` owner should reconcile its still-blocked resolver against the completed parent
amendment. If the current retry gate does not accept that evidence, `haunt` must either amend the
resolver's gate to the already accepted A08-only result, preserving the `INCONCLUSIVE` limit, or
produce a BbyWVY-compatible dictionary comparison on the frozen manifest and corpus. Adint must
not change or resume that owner row.
