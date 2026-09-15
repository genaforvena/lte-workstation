# Repeat Haunt review-gate resolver rows — 2026-09-12

This receipt applies to these adint-owned rows:

- `unblock/adint/ee1fb920c5859c73/resolve` → `unblock/haunt/0f515995e95e01ae/resolve`
- `unblock/adint/a9a0dc80e4cd6887/resolve` → `unblock/haunt/13c9ff98ef09ee8b/resolve`
- `unblock/adint/0d00a8df2b9464b0/resolve` → `unblock/haunt/42c1ba603f1c658e/resolve`
- `unblock/adint/aaf49340733a1f6c/resolve` → `unblock/haunt/4491e5e46763bfae/resolve`
- `unblock/adint/1b656911cf0445be/resolve` → `unblock/haunt/bc94e77f19f14dd1/resolve`

The exact kids-v1 hash remains
`0e0e1b2a066541176fd2fddfb7a3ae30e1da5473dc24e41fa1f1b9258a09b405`; the current signoff
register has no reviewers, and the common Haunt lesson review gate remains blocked. These duplicate
rows cannot create the missing independent adult judgments. The exact prerequisite is two separate
adult reviews and self-attested approvals for this hash, followed by Haunt's release validation and
owner-authored resume. No signoff, release, or Haunt task was changed.

The fresh current-hash/signoff evidence and full review protocol are in
`docs/task-receipts/unblock-adint-haunt-independent-review-gate-20260912.md`. Each row must still
pass its own `mesh-task check dispatch <task-id> adint` before being settled against that evidence.
