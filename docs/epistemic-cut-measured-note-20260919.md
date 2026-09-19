# A verdict that flips when a stream crosses the boundary is not a property of the system

**Status:** draft-only, no outward publish. Vetted 2026-09-19
(`pub/epistemic-cut-vet/vet-epistemic-cut`): mechanism absent from `scripts/`,
target surface (`mesh-sensorium --viability/--amplification`) live.
Source review:
`docs/reviews/second-order-cyb-epistemic-cut-sensitivity-sensorium-20260910.md`.

Every health verdict on this mesh names a system and an observer. `mesh-sensorium`
classifies percept-categories from cached producer streams — but which streams
count as "the system" and which as "context" is a modelling choice made by the
observer, and today exactly one such choice is ever rendered. A label that reads
green under one legitimate partition and red under another is **cut-dependent**,
not an intrinsic property of the thing being watched. We currently cannot tell
the two apart, because we never rerun a determination under a second cut.

The mechanism is **epistemic-cut sensitivity** (Bedau 2016: the epistemic cut is
arbitrary/movable; a stable-looking object claim can be an artefact of the
boundary the observer chose). It complements `mesh-observer-effect`, which asks
whether observation *perturbs* a value; this asks whether the value depends on
what the observer declared to be inside.

Concrete application, report-only: a `--cut-sensitivity` mode on
`mesh-sensorium` with two predeclared legitimate cuts — narrow (only directly
mapped producer streams) and wide (plus the substrate/context streams already
available). Recompute each category's viability/coverage under both; emit
`CUT_STABLE` (unchanged), `CUT_SENSITIVE` (changed), or `CUT_UNKNOWN` (one cut
lacks fresh evidence). Both cut descriptions and input rows ship in the
artifact; no single cut is silently treated as the world's natural boundary.

Acceptance fixtures: (1) a category with a fresh producer but stale context
stream must show the two determinations separately, never collapsed into one
green; (2) a category where context cannot change the result must prove
invariance. If the health label moves only because a stream crossed the
boundary, the report says so — counted, not argued.
