# Senses receipt: sound claim 4 measure contract — 2026-09-16

## Change

Reclassified claim 4 in `scripts/mesh-series-stats` from a structural impossibility claim to a
beat-tracker disagreement diagnostic. The gate now measures only rows with `fbeats > 1`, reports
`fbeats<=1` or missing whole-file periods as UNKNOWN coverage, and retains per-organ decomposition
for the measurable population. A degenerate whole-file scan cannot enter a disagreement rate or
mint a physical period.

The existing `scripts/mesh-sound-reflex` `fbeat_of` contract already abstains as `na:degenerate`;
its live `tick` test remains wired to the renderer metadata path.

## Verification

- Red phase: the updated live-shaped C4 fixture failed against the old output (`impossible=15/n=40`).
- Green phase: `bash scripts/tests/uxn/test-series-stats` passed all 17 truth-table rows, source
  mutants, carry checks, and claim-gate fixture arms.
- Syntax: `bash -n scripts/mesh-series-stats scripts/mesh-sound-reflex` passed.
- Live: `scripts/mesh-series-stats --claims` returned rc=2 and reported `measurable rows: n=1266
  disagreement=32 (2.5%) unknown(degenerate fbeats<=1)=748`; this UNKNOWN is intentional.
- Cross-path: `scripts/mesh-sound-reflex --test` completed its assertion run without failures.

Delegation: worker `senses-claim4-audit` was launched for an independent duplicate/eligibility
audit, but expired authentication (`Please run /login`) and returned no report; no worker result was
used as evidence. Ledger ownership, source inspection, edits, and final verification stayed local
because they are single-writer/tightly coupled.
