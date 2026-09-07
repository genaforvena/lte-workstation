# Ask-answer funnel — Unit 2: remove inference

Task: `ask-answer-funnel-implementation-20260907/unit-2-remove-inference`

Status: complete; owner `tg`.

## Next action

Inspect `claim_id_of` and prose-fallback consumers, then build a regression corpus for
legacy `UNKNOWN` claims before removing inference.

## Initial evidence

- Unit 1 now preserves the complete explicit task key through dispatch, claim, and done joins.
- Unit 2 must still account for legacy claim-id/prose fallback behavior before changing it.

## Consumer inventory and legacy corpus (2026-09-07 16:59Z)

| consumer | location | current behavior |
|---|---|---|
| shared claim parser | `scripts/mesh-claim-shape.sh:_claim_id_of_uncached` / `claim_id_of` | explicit `task:<id>` wins; untagged prose falls through to slug/shouty inference |
| dispatch-side parser | `scripts/mesh-dispatch:idof` and its real `claim_id_of` twin | explicit tag joins the full key; untagged legacy lines still derive a slug |
| claim/dash consumers | `scripts/mesh-claim`, `scripts/mesh-dispatch` | consume the parser result for claim/done matching; no removal is safe until legacy rows render `UNKNOWN` |

The focused legacy corpus was run against the current shared parser. A namespaced legacy subject
inferred `unit-2-remove-inference`; a prose citation also inferred `unit-2-remove-inference`; and
an unrecognizable body returned empty/unknown. The explicit parser corpus returned the complete
`ask-answer-funnel-implementation-20260907/unit-2-remove-inference` key for both task and claim.

Observed corpus output before removal (the required RED evidence):

```text
legacy_subject=unit-2-remove-inference
legacy_prose=unit-2-remove-inference
legacy_unknown=
explicit=ask-answer-funnel-implementation-20260907/unit-2-remove-inference
```

The first two rows are failing red cases: after inference removal they must render UNKNOWN/empty
rather than a guessed leaf slug. The explicit row must retain the complete key. The live consumers
are not changed yet; this is progress evidence, not green evidence.

## UNKNOWN-safe implementation and focused GREEN (2026-09-07 17:18Z)

The shared live parser now returns `UNKNOWN` for untagged legacy prose while preserving the
complete explicit `task:<id>` key. The deployed parser copy is byte-identical. The dispatch
consumer's real `--derive-ids` path now reports:

```text
legacy:  task=ask-answer-funnel-implementation-20260907/unit-2-remove-inference claim=UNKNOWN
explicit: task=ask-answer-funnel-implementation-20260907/unit-2-remove-inference claim=ask-answer-funnel-implementation-20260907/unit-2-remove-inference
```

Focused test artifact `tests/test-ask-answer-funnel-unit-2-remove-inference.sh` passed `rc=0`.
`bash scripts/mesh-claim --test` passed with `smoke-test: ok`. The broad dispatch smoke still
contains legacy closure assertions that conflict with this new UNKNOWN contract; it is not used
as a false green. Unit 2 remains open pending reconciliation of those old assertions and the
final focused verification across every dispatch close path.

Focused verification: `scripts/mesh-dispatch --test` passed (260 assertions), and
`scripts/mesh-claim --test` passed. These are baseline parser checks, not the required
red-before-green removal proof.

## Verification

Implementation is present in both the shared parser and the dispatch consumer path. The red
corpus, UNKNOWN-safe implementation, and final close-path verification are all recorded below.

## Close-path reconciliation — GREEN (2026-09-07 17:40Z)

The red corpus above was followed by the UNKNOWN-safe parser change. The remaining dispatch
assertions were reconciled to the contract: untagged legacy prose remains non-authoritative, while
every genuine close fixture now carries the exact \`task:<id>\` account tag. The explicit-tag parser
also rejects a trailing punctuation colon, preserving the exact key rather than returning an
accidental \`id:\` value.

Owner-authored implementation changes:

- \`scripts/mesh-claim-shape.sh\` and deployed \`/home/mesh-home/.local/bin/mesh-claim-shape.sh\`
  SHA256 \`69866ba249c85ae53b57a0f529f743bf65c61b21dbbfffde35a04ebe1ee2f950\` (identical).
- \`scripts/mesh-dispatch\` SHA256
  \`804215a16a08ef4d586d8a16a490b2fd0e78d61d9552f26cb241eeba987c7c03\`.
- focused test SHA256
  \`d71a339e1d4e680faaab3a2327de87fcb953399561165521af611d2cbc2a9468\`.

Fresh verification artifacts:

\`\`\`text
tests/test-ask-answer-funnel-unit-2-remove-inference.sh: rc=0
scripts/mesh-claim --test: rc=0, smoke-test: ok
scripts/mesh-dispatch --test: rc=0, smoke: ok (260 assertions)
dispatch output sha256=4d78c337bf423e10bbd7082f6da26619e6ffa338b63da09faccc26b8c992aa23
focused output sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
claim output sha256=f4731416e61dac2209d51f5fa5d1a4a12d64f13c6c647abd6c485752a25c5adf
\`\`\`

The broad close-path output is \`smoke: ok (260 assertions)\`, including subject anchoring,
post-mint closure, deep-board fresh own-subject closure, uppercase/lowercase parser agreement,
pasted-URL closure, poster-window closure, and fresh-done-without-taking benign closure. Unit 2
is ready for owner terminal disposition after the mesh-task receipt is updated with this artifact
hash; no \`[done]\` was posted in this evidence update.
