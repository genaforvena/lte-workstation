# Ask-answer funnel Unit 5 — board canary disposition

## Disposition

`DEFERRED`, not retired. The governing design explicitly sequences the board
canary after Units 1–4 and warns that synthetic asks consume real mind effort,
can corrode trust if injected too often, and require both a rate ceiling and an
honesty rule. No synthetic ask was injected.

## Evidence

- Unit 1 explicit key: done, with artifact-backed task/claim joins.
- Unit 2 UNKNOWN-safe inference removal: done, with focused and broad parser
  verification.
- Unit 3 witness resolution: done, with age/denominator-gated metrics and
  deployed wiring.
- Unit 4 dashboard resolution: implementation evidence exists, but the
  deployed full `mesh-dash --test` remains an unresolved timeout gate; focused
  and live-frame checks are green.
- The source contract is `docs/superpowers/specs/2026-07-15-ask-answer-funnel-design.md`,
  Unit 5, “the board canary (causality; deferred until 1–4 land)”.

## Safe next gate

Before any canary is run, publish a canary registry and rate ceiling, define a
recognizable synthetic marker/honesty rule, and resolve the Unit 4 full-test
gate. Until then the correct state is typed `DEFERRED`; running a synthetic ask
would violate the design's causality and trust guard.
