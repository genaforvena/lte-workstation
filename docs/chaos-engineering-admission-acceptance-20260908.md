# Chaos-engineering admission — acceptance and price

## Predicate

One isolated sample is admitted only if all three checks pass:

1. final consumer rc is `0`;
2. the outcome records a deterministic injected failure followed by a retry transition and a recovery transition;
3. the outcome artifact is nonempty.

## Price

- Sample count: `1`
- Samples satisfying the complete predicate: `1/1` (`100%`)
- Predicate components: `3/3` (`100%`)
- Bounded work: three local emulator calls, two injected rc `75` failures, no live service or substrate mutation.

## Decision

ADMIT the bounded local chaos-engineering mechanism. The result proves a reusable, deterministic
fail-then-recover path, but does not prove that a live mesh service is wired to consume it.
That wiring/consumerization gap is handed to genome; discover does not wire it.
