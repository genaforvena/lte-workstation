# Antifragility live review — BOUNDED ANTIFRAGILITY: the convex→concave inflection ("antifragility up to a point")

**Area:** antifragility, convexity & ruin theory (Taleb) · **Angle:** a known CRITIQUE / failure mode
**Date:** 2026-07-31 · **Node:** mesh-home · **Home file:** `scripts/mesh-resource-guard`
**Status:** HELD design block landed (comment-only, 0 behavior change) — NOT wired; see "Why held".

## The concept (what we do NOT already embody)

**Bounded antifragility — the convex→CONCAVE INFLECTION.** Antifragility = a *locally convex* response
to a stressor (gains from variation exceed losses). But convexity is a **local, floor-anchored**
property, not a global one. The mathematical constraint (Taleb's own medicine/oncology work): *every
relatively smooth dose-response with a **ceiling** has to be **concave** while approaching the ceiling.*
So a hormetic/biphasic response is **convex near the floor, concave near the ceiling, with an inflection
between** — gains from small/medium doses, **collapse** from large ones. Hormesis is biphasic precisely
because "high-dose exposures overwhelm repair mechanisms, causing damage rather than enhancement."

**Why this is a failure mode of the whole convexity program (the critique):** a convexity/robustness
verdict measured at **low** magnitude does **not** certify convexity at **high** magnitude. Any policy
that extrapolates a locally-measured "convex/antifragile/robust" reading to larger stressors walks the
system **past the inflection into the concave/ruin regime while believing it is still antifragile.**
"Antifragile" is always "antifragile *up to a point*"; a program that never locates the point is blind
to its own boundary.

## Citation (where it was found — live literature)

- N.N. Taleb & collaborators, **"(Anti)Fragility and Convex Responses in Medicine"** / **"Working With
  Convex Responses: Antifragility from Finance to Oncology"**, *Entropy* **25(2):343 (2023)**
  (arXiv:1808.00065). The ceiling→concavity constraint and the biphasic-hormesis dose-response.
- Surfaced by WebSearch `"bounded antifragility hormesis dose-response ceiling stress threshold convex
  response inversion critique"` (2026-07-31) — top hit arXiv:1808.00065; the search synthesis states the
  ceiling/concavity constraint and the biphasic "high dose overwhelms repair → damage" mechanism, plus a
  meta-critique that antifragility *bundles* hormesis/optionality/selection/convexity which "fail for
  different reasons."

## The gap — mesh-wide

The mesh embodies only the **LOWER** hormesis threshold. `scripts/mesh-chaos` (~L400, "DOSE-CONCENTRATION
GAP", cites the same program) says *"a convex response is exercised only ABOVE a threshold → CONCENTRATE
few large doses."* That is the **floor**. There is **no axis anywhere for the UPPER inflection** where the
same convex response turns concave. The two consumers of a locally-measured convexity verdict are both
blind to the ceiling:

- `mesh-chaos`'s HELD escalating-magnitude / dose-concentration tier — its stated prerequisite "confirm
  recovery-capacity is convex" is measured **once, at low dose**. Insufficient: convex@low ≠ convex@high.
- `mesh-convexity`'s global CONVEX/ROBUST verdict — a single Jensen gap `E[f(X)]−f(E[X])` over the whole
  series **cannot** say the response is convex to small deviations but concave to large ones. (Note:
  `mesh-convexity` uses a *fixed globally-convex cosh probe* to characterize a distribution's
  fat-tailedness; the inflection is a property of a system's *response function*, so it does not live in
  mesh-convexity — it lives where a real stress→recovery response is measured.)

This review lands the **missing UPPER companion** to that lower floor.

## The concrete application (named file + axis)

`scripts/mesh-resource-guard` → **`node_recovery_curvature`** over the same `accel_series` (retained
MemAvailable history). Read the **curvature of the RECOVERY LEG** — the ASCENT after the last trough, the
second derivative of the recovery response:

- steady / growing positive deltas → **CONVEX bounce = robust** (the node is antifragile to this dip);
- **DECELERATING** positive deltas → **CONCAVE stall = fragile** — the bounce is dying before it completes
  the climb back; the recovery-capacity **ceiling** has been exceeded; at risk of re-absorption.

**Distinct from every existing axis, all of which read the DESCENT or the LEVEL:** `node_pressure`
(level), `node_accel_classify` (is the *drop* accelerating — the descent's 2nd derivative), `node_tau_eta`
(time-TO barrier, forward), `node_dwell_classify` (time-SINCE crossing — Parisian dwell). None reads the
ASCENT. Descent-accelerating ("falling faster") ≠ recovery-decelerating ("rising slower / can't finish
the bounce") — opposite legs, distinct fragilities.

## Why held (not wired) — the honest blocker

Never ship a data-starved organ ("declaring an organ before arming it", "a signal from too-short a window
rots"). The retained window is `ACCEL_KEEP=4` samples. A recovery leg needs ≥3 ascending points to yield
even **one** delta-comparison, so curvature here is fit from **n=3 — noise, not signal**; a curvature axis
on 4 points would fire on cache churn as readily as on a real stall. **Prerequisite before wiring:**

1. a persistent **excursion ledger** — accumulate `(dip-depth, recovery-cost)` pairs across episodes, so
   the inflection is fit from **many** excursions spanning depths (this also enables the fuller depth→cost
   curvature form of the mechanism); **or**
2. a widened dedicated recovery-window — a separate longer history than the 4-sample `accel_series`, whose
   size is load-bearing for the dwell/accel axes and must not be bent for this.

RED-first + a fixture battery lands **with** the ledger, not before: a convex-bounce series must read
robust; a decelerating-recovery series must read stall; a still-descending or fully-recovered series must
read clean n/a.

## Coverage delta

Closes the antifragility area's open **upper-inflection** item (the lower hormesis floor was already in
`mesh-chaos`). Related landed axes it complements: Parisian dwell (`node_dwell_classify`, 2026-07-29),
Taleb-Douady left-tail direction (`mesh-convexity asymmetry()`, 2026-07-30), κ pre-asymptotic
(`mesh-convexity`, 2026-07-28), degeneracy-vs-redundancy (`mesh-sensorium`, 2026-07-31). Still open after
this: the **absorbing-barrier as an explicit hard GATE** (Parisian dwell is its report-only precursor),
and Hill/EVT tail-exponent estimation.
