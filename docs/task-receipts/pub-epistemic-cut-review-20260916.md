# Pub epistemic-cut draft review — 2026-09-16

## Decision

**PUBLISHABLE as a measured design case; do not present it as shipped implementation.**

The angle is bounded and falsifiable: rerun one `mesh-sensorium` viability/coverage determination
under two declared legitimate observer cuts (narrow producer-only and wide producer+context),
retain both input rows, and emit `CUT_STABLE`, `CUT_SENSITIVE`, or `CUT_UNKNOWN`.

## Personally inspected evidence

- `docs/reviews/second-order-cyb-epistemic-cut-sensitivity-sensorium-20260910.md` — dated
  2026-09-10 literature review; identifies epistemic-cut sensitivity as a missing mechanism,
  supplies the concrete application and fixtures, and states that no implementation was landed.
- `docs/drafts/epistemic-cut-sensitivity.md` — human-facing draft; preserves both cut definitions,
  the three outcomes, the fixture plan, and the explicit design-only boundary.

## Provenance and boundary

The draft is derived from the dated genome review and its cited Bedau (2016), Axelsson (2025), and
Roffé & Díez (2025) sources. No `scripts/mesh-sensorium` implementation, deployed copy, or
production report is claimed. No edits were required for this review.

## Next outward action

Use the existing draft for a public design-case write-up only after the pub pre-publish board notice;
the eventual implementation remains a separate task requiring fixtures and wiring verification.
