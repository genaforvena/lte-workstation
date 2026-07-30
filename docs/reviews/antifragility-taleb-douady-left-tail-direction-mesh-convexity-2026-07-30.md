# Antifragility live review — Taleb-Douady left-tail fragility DIRECTION (the sign the CAFE gap discards)

**Date:** 2026-07-30 · **Area:** antifragility / convexity / ruin theory (Taleb) · **Angle:** an
OPERATIONAL mechanism (not philosophy) we do not yet embody · **Landed in:** `scripts/mesh-convexity`
(uncommitted, in tree — steward lands).

## The concept, cited

**Fragility is a property of ONE tail, not of dispersion.** Taleb & Douady's foundational definition
(*Mathematical Definition, Mapping, and Detection of (Anti)Fragility*, arXiv:1208.1189; the IMF stress-
testing note *A New Heuristic Measure of Fragility and Tail Risks*, IMF WP/12/216; restated in
*(Anti)Fragility and Convex Responses in Medicine*, arXiv:1808.00065, and *Working with Convex
Responses: Antifragility from Finance to Oncology*, Entropy 25(2):343 / arXiv:2209.14631) defines
**fragility below a level K** as the sensitivity of the **left-tail partial expectation**
∫_{−∞}^{K} x·f(x,σ) dx to a **mean-preserving increase in the scale parameter σ**. By the *fragility
transfer theorem* this sensitivity is proportional to the **concavity (negative 2nd derivative) of the
response BELOW K**. Operationally: the gap between ∫_K f(x,σ) and ∫_K f(x,σ+Δ) is proportional to the
concavity of f in the left tail — *"parameter imprecisions are fragilizing if they can increase the
left tail."* Fragility lives in one direction; a symmetric fat-tailed process (convex on both sides) is
**not** fragile.

Sources:
- [Taleb & Douady, arXiv:1208.1189](https://arxiv.org/abs/1208.1189)
- [Taleb, (Anti)Fragility and Convex Responses in Medicine, arXiv:1808.00065](https://arxiv.org/abs/1808.00065)
- [Working with Convex Responses, Entropy 25(2):343 / arXiv:2209.14631](https://www.mdpi.com/1099-4300/25/2/343)
- [IMF WP/12/216, A New Heuristic Measure of Fragility and Tail Risks](https://www.imf.org/external/pubs/ft/wp/2012/wp12216.pdf)

## What we already embodied — and the exact gap

`mesh-convexity` measures the **CAFE distributional Jensen gap** E[cosh(λz)]−cosh(0) vs a matched
Gaussian (arXiv:2605.02463), with a κ pre-asymptotic reliability check (arXiv:1802.05495). Its
potential is **symmetric by design** (cosh weights both tails, to measure dispersion-convexity
independent of skew). Consequence, in the tool's own words: it can return CONVEX/ROBUST/GAUSSIAN but
*"sign of the effect is a separate question"* — it **cannot say which tail carries the convex weight**.
A series convex on the right (gains from volatility) and concave on the left (harmed by it — the
textbook FRAGILE profile) reads identically to a symmetric leptokurtic one. That is precisely the
LOCAL-vs-TAIL / directional-fragility gap my coverage note flagged open after the κ (2026-07-28) and
Parisian-ruin (2026-07-29) landings.

## The mechanism landed (model-free, same samples, report-only)

Split the standardized potential at z=0 into its down/up halves and take the bootstrapped left−right
half-gap on the SAME resamples that already produce Δ (zero extra draws):

```
A = mean_{z<0}[cosh(λz)−1] − mean_{z>0}[cosh(λz)−1]
  A CI wholly > 0 → LEFT-HEAVY   (convex weight in the DOWN tail; if down=harm ⇒ FRAGILE)
  A CI wholly < 0 → RIGHT-HEAVY  (convex weight in the UP tail;   if up=benefit ⇒ ANTIFRAGILE)
  CI straddles 0  → SYMMETRIC    (both tails balanced — the CAFE verdict is the whole story)
```

It is **orientation-agnostic** — it reports *which* tail, not *whether* that tail is harm (the metric
does not know the metric's polarity), leaving the down/up→harm mapping to the consumer exactly as the
CAFE verdict already punts its sign. This is the raw ingredient of Taleb's fragility SIGN that the
symmetric gap throws away.

## Verification (RED→GREEN, mutation-verified)

`mesh-convexity --test` gains a fixture battery: left-skewed spikes → **LEFT-HEAVY**, and the existing
symmetric fat fixture must read **SYMMETRIC** (a vacuous "always LEFT-HEAVY" cannot pass both). Seen
RED: mutating the split to drop `−gR` (weight only the down tail) makes the symmetric fixture read
LEFT-HEAVY → gate fails, exit 1. Restored → exit 0. Measured separations: left A=+2.27 CI=[+1.18,
+10.05]; right A=−2.29 CI=[−9.24,−1.16]; symmetric A CI=[−4.88,+4.63] (straddles); bounded
CI=[−0.10,+0.01] (straddles).

## Why this is the right file, not a new organ

The measurement is one added axis on the SAME standardized potential `mesh-convexity` already computes
over any numeric series — it reuses the bootstrap resamples and the κ reliability qualifier. A separate
organ would duplicate the standardization + bootstrap and split the second-order story across two tools.
It is report-only (no gate/kill/board-post), matching the tool's stance as a measurement layer.
