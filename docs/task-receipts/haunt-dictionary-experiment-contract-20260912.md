# Haunt dictionary experiment contract — 2026-09-12

- Parent: `haunt-install-unblock-20260907/install-and-retry-tinyfleet`
- Resolver: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Decision: accept only the narrow, synthetic A08 fixture claim; keep the BbyWVY dictionary-behavior claim blocked.

## Revised claim

For the frozen CC0 A08 synthetic correction fixture, the exact, case-sensitive
replacement baseline produced 120/120 exact heldout outputs, mean CER 0, and
preserved protected fields in 120/120 cases; the identity baseline produced
0/120 exact outputs. The declared verdict remains `INCONCLUSIVE` for broader
correction behavior because the fixture contains five synthetic substitutions,
source-family uncertainty is not estimable, and the ByT5/LoRA arms are
unavailable. This result is not evidence of BbyWVY dictionary behavior.

The frozen manifest and corpus hashes are respectively
`9081dd78b28ed94b501016698cd6d5347095a5ea079730bf888123c3ec2e1e08` and
`81a41340c0c01555a536e9aa30b3b2b72b1dd9ae48908014fd0f58192515dcd3`. The
measured result hash is
`555f1ab7808d5d01324c770e58fc594b48ea17ff55364d6a4214e4aed8b988fd`.
Full input selection, method, and smoke details are in
`docs/task-receipts/unblock-adint-c0bd395c610ed1e1-resolve-20260912.md` and
`/home/mesh-home/tiny-fleet/docs/task-receipts/adint-operator-authorized-dictionary-input-20260912.md`.

## Revised retry and closure gate

Do not rerun `scripts/bbywvy_test.py` as a dictionary test: it is a six-case
generative runtime smoke with no dictionary arm. Do not resume the original
parent while its claim still says BbyWVY dictionary behavior. To close the
parent narrowly, its owner must amend the task claim and closure criterion to
the A08-only statement above and record the `INCONCLUSIVE` limit. If the
parent retains its BbyWVY behavior target, create or identify a BbyWVY-compatible
dictionary arm against this frozen manifest/corpus, measure it against a
declared comparison, and record output hashes plus a typed verdict before
resuming.

The row remains blocked as `experiment-contract`; inputs are no longer the
blocker. The current A08 artifact alone does not satisfy the broader parent.

## Ledger support and verification

The `mesh-task` blocker allowlist now accepts `experiment-contract`. This is
commit `85e2d61` (`Add experiment-contract task blocker type`), with regression
test `tests/test-mesh-task-experiment-contract-type.py`. The test passed;
`mesh-sync-tools --apply` deployed the committed CLI update, and the installed
`mesh-task --test` passed. The owned row is durably blocked with the new type
and retry text above. Its resume check correctly remains refused until the
parent scope is amended or a BbyWVY-compatible dictionary result exists.
