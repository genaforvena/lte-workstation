# Haunt independent-review prerequisite — 2026-09-12

This receipt applies to these adint-owned duplicate resolver rows:

- `unblock/adint/d0e229ae2b51cc32/resolve` → `unblock/haunt/bc94e77f19f14dd1/resolve`
- `unblock/adint/a8c1487b3615dd3e/resolve` → `unblock/haunt/4491e5e46763bfae/resolve`
- `unblock/adint/62c04c13f8257c54/resolve` → `unblock/haunt/13c9ff98ef09ee8b/resolve`
- `unblock/adint/1f6dc696fef3898e/resolve` → `unblock/haunt/42c1ba603f1c658e/resolve`
- `unblock/adint/cb235046c815a1e4/resolve` → `unblock/haunt/0f515995e95e01ae/resolve`
- `unblock/adint/26eb9cd9018aad06/resolve` → `unblock/haunt/07940701bb859ee5/resolve`

## Fresh evidence

The shared review gate `crypthauntology-kids-followup-20260912/lesson-review-safety-gate` remains
blocked on two independent adult approvals. In `/home/mesh-home/src/hyperhauntology_for_kids`,
the signoff register has an empty `reviewers` array and no disagreements. Recomputing
`lesson_materials_sha256("lessons")` returned
`0e0e1b2a066541176fd2fddfb7a3ae30e1da5473dc24e41fa1f1b9258a09b405`, matching the current review
request. The exact owner-scoped review gate refuses dispatch with exit 2. None of these facts
constitutes an approval.

## Exact external prerequisite

Two distinct adults must independently review every file under `lessons/`, complete
`lessons/safety-review-checklist.md`, and self-attest separate decisions in
`protocol/lesson-review-signoffs.json`, each bound to the current hash above. Once both valid
approvals are recorded, the owner must revalidate/regenerate the release, verify
`educational_review.status: APPROVED`, then resume the lesson gate. Only after that step is
terminal may Tiny Fleet closeout eligibility be checked again. Do not write signoffs for anyone or
distribute the bundle while pending.

Supporting current request and signoff protocol:
`/home/mesh-home/src/hyperhauntology_for_kids/docs/lesson-review-request-kids-v1-20260912.md`.
No lesson, review register, Haunt claim, or release was changed.
