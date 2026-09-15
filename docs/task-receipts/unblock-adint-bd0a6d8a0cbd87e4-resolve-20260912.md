# Resolver receipt: `unblock/adint/bd0a6d8a0cbd87e4/resolve`

- Checked: 2026-09-12 UTC
- Parent: `unblock/haunt/07940701bb859ee5/resolve`
- Review gate: `crypthauntology-kids-followup-20260912/lesson-review-safety-gate`

The live Haunt parent remains blocked pending two distinct adults' independent reviews. The current
signoff register at `/home/mesh-home/src/hyperhauntology_for_kids/protocol/lesson-review-signoffs.json`
has an empty `reviewers` array. Recomputing the materials hash returns
`0e0e1b2a066541176fd2fddfb7a3ae30e1da5473dc24e41fa1f1b9258a09b405`, and the Haunt-owned review
gate's dispatch check exits 2. The prerequisite is two independent, self-attested approvals bound
to this exact hash; then Haunt must revalidate the release before resuming. No signoff or release
state was written. The shared protocol and detailed evidence are in
`docs/task-receipts/unblock-adint-haunt-independent-review-gate-20260912.md`.

Verification: this row's owner-scoped dispatch check exited 0 before take; the live parent status is
still blocked; the signoff register is empty; the current review gate remains refused.
