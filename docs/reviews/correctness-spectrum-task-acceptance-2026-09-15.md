# Correctness as a spectrum applied to task acceptance

Date: 2026-09-15
Source: https://miniblog.nicholasly.com/blog/correctness-as-spectrum/
Study brief: distributed systems, 2026-09-09; source hit “Correctness as spectrum not as binary”.

## Review

The source's useful mechanism is to state correctness relative to an explicit guarantee and
failure model. It distinguishes stronger consistency (more coordination and latency) from weaker
but available responses, and describes commutative, associative, idempotent merge as a way to make
some bad states impossible. The mesh analogue is task acceptance: a row is not simply “good” or
“bad”; its safe action depends on the predicate (`dispatch`, `pending`, or `resume`) and its
current lease/dependency state.

## Local application

Applied the mechanism to this task chain:

`discover-correctness-spectrum-20260915/review-and-apply-correctness-spectrum`

The exact-owner row was created with an artifact-backed acceptance condition, then claimed. A
post-claim dispatch check returned exit 2 (refused), which is the expected weaker state: the work
is valid and owned, but no longer dispatch-eligible. This records the predicate and state instead
of collapsing both into a binary failure.

Reproducible local merge probe (the CRDT property used as the bounded application):

```text
A={alpha,beta} B={beta,gamma} C={delta}
union(A,B)=alpha,beta,gamma
union(B,A)=alpha,beta,gamma
union(union(A,B),C)=alpha,beta,delta,gamma
union(A,union(B,C))=alpha,beta,delta,gamma
union(union(A,B),union(A,B))=alpha,beta,gamma
RESULT=commutative associative idempotent: PASS
```

The ledger task predicate remains authoritative; this review does not change routing or claim
semantics. The artifact is the durable result of the probe and the explicit state-qualified
acceptance mapping.

