# When the observer boundary changes the result

*Draft based on the live literature review dated 2026-09-10:*
`docs/reviews/second-order-cyb-epistemic-cut-sensitivity-sensorium-20260910.md`.

## The measured problem

Second-order cybernetics puts the observer inside the system, but that statement can become a
convenient escape hatch: choose a boundary that makes the conclusion look inevitable. The review
identified a sharper test for that failure mode: move the observer/environment boundary between two
legitimate cuts and rerun the same determination.

The result is **epistemic-cut sensitivity**. If the verdict changes when a component moves from
observer to environment, the verdict is cut-dependent. It is not an intrinsic property of the
supposed system. If one cut lacks fresh evidence, the honest result is uncertainty, not a green
verdict by default.

## A bounded engineering test

The proposed application is the existing `scripts/mesh-sensorium` reports. For each percept
category, recompute the same viability/coverage determination under two declared cuts:

- **Narrow cut:** only producer streams directly mapped to the category.
- **Wide cut:** those producer streams plus available substrate and context streams, such as node
  health and operator/home context.

The report should retain both cut descriptions and input rows, then emit one of three outcomes:

- `CUT_STABLE` — both cuts produce the same class.
- `CUT_SENSITIVE` — the class changes between cuts.
- `CUT_UNKNOWN` — one cut lacks fresh evidence.

A first fixture should pair a fresh local producer with stale context and show both determinations
separately. A second should prove invariance where added context cannot change the result.

## What this does not claim

This is a design lead, not an implementation report. The reviewed artifact explicitly says no
`mesh-sensorium` source, deployed copy, or public report was changed, and no implementation was
landed. The proposal complements `mesh-observer-effect`: that tool asks whether running a sense
perturbs a quantity; this test asks whether the quantity depends on the declared boundary.

The underlying review cites Bedau (2016), Axelsson (2025), and Roffé and Díez (2025); see the source
links and the full evidence boundary in the review artifact above.
