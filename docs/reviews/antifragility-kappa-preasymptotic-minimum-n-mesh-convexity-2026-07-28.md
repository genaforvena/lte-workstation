# LITERATURE review — antifragility/ruin: Taleb's κ metric, the minimum-n our second-order gate skips (2026-07-28)

**Area:** antifragility, convexity & ruin theory (Taleb), from the angle of a **concrete metric this
area uses to measure itself** — and a metric we do NOT embody: the *pre-asymptotic sample-size
requirement* for a mean (or a variance) to be trustworthy on a fat-tailed axis.

## What we already embody in this area (so this doesn't re-land)

- `scripts/mesh-convexity` — the **distributional Jensen gap** under a convex potential (CAFE,
  arXiv:2605.02463): E[f(X)]−f(E[X]), f=cosh, verdict CONVEX/ROBUST/GAUSSIAN-LIKE. Fixed the
  first-vs-second-moment *misread* ("antifragile" as a first-order word for a second-order thing).
- `scripts/mesh-chaos` — chaos engineering / Chaos Monkey, adaptive stress-and-learn.
- `scripts/mesh-endogeneity` — the correlated/dependent-trials failure mode of the convex-payoff story.
- `docs/reviews/ergodicity-breaking-pooled-corpus-2026-07-24.md` — time- vs ensemble-average (the ruin core).
- `review-antifragility-iatrogenics-via-negativa` — the subtract-arm / via negativa.

## The concept we do NOT embody: Taleb's κ (kappa) metric — "how much data do you need?"

Taleb, **"How Much Data Do You Need? An Operational, Pre-Asymptotic Metric for Fat-tailedness"**
(arXiv:1802.05495, 2018), folded into **"Statistical Consequences of Fat Tails"** (Technical Incerto,
arXiv:2001.10488, 2020, still the live reference edition). κ is a concrete *self-measurement* of a
distribution — on [0,1], **0 = Gaussian (maximally thin), 1 = Cauchy-like (maximally fat)** — defined
from the **rate of convergence of the Law of Large Numbers for finite sums**:

> κ(n₀, n) = 2 − ( ln n − ln n₀ ) / ( ln M(n) − ln M(n₀) ),   M(n) = E| Sₙ − E[Sₙ] |

where M(n) is the **mean absolute deviation of the sum** of n iid copies. Gaussian: M(n)∝√n ⇒ the
ratio is ½ ⇒ κ=0. Cauchy: M(n)∝n (averaging buys you nothing) ⇒ κ=1. The operational reading — and the
reason it's the *metric this area uses to measure itself* rather than another fragility opinion: **κ tells
you the multiplier on sample size**. To reach the statistical significance a Gaussian gets from n₀
samples, a κ>0 axis needs far more; a sample mean/σ computed over a small window on a high-κ axis is
**pre-asymptotic** — it hasn't converged, and it swings with the window. (Companion diagnostic in the same
work: the **maximum-to-sum (MS) plot** — R_n^p = max/Σ of the p-th powers; if R_n^p doesn't fall to 0,
the p-th moment *does not exist*. That says *which* moments are even defined; κ says *how slowly* the ones
that exist converge.)

## Where it bites us — and the exact file

`scripts/mesh-convexity` fixed the *misread* but silently inherited the assumption underneath it: it
**standardizes X by its sample σ** (`sd = math.sqrt(var); z = (x−m)/sd`) and reads the Jensen gap off the
standardized series. That is only valid if the **second moment exists and has converged** on the window it
was handed. On a fat-tailed axis (infinite or slow-converging variance) σ is itself a pre-asymptotic
artifact — so the CONVEX/ROBUST/GAUSSIAN verdict is computed on an unstable denominator, and the tool
gives **no signal that this is happening**. It's the same shape as its own founding lesson one moment
higher up: convexity assumed the *first* moment was the whole story; κ says convexity now assumes the
*second* moment is stable, and for exactly the leptokurtic series it's built to flag, it may not be. The
mesh-wide doctrine caveat — *"any figure is only its current answer, RE-DERIVED from the sliding window"*
(`docs/uxn-doctrine-claims.md`, `mesh-series-stats`) — understates this: for a high-κ axis, even the
*current* answer over a small window is not just stale-able but **not-yet-meaningful**, and nothing
measures which axes those are.

## Proposed concrete application (HELD — steward lands) — `scripts/mesh-convexity`

Add a **κ pre-check** as a reliability qualifier on the convexity verdict (not a new verdict — a
*confidence gate on the existing one*), computed from the samples already in hand:

1. Estimate M(n) at a few block sizes by resampling sums of b∈{1,2,4,8,…} draws from the window
   (bootstrap, reuse the existing RNG/seed), fit κ from the ln M(n) vs ln n slope over the available
   range. Cost: same order as the bootstrap already running.
2. **Qualify, don't overrule:** append to the verdict line — κ≲0.25 → `(σ-stable)`; 0.25<κ≲0.5 →
   `(σ pre-asymptotic — verdict tentative)`; κ≳0.5 → `(fat-tailed: n=<N> likely too few — σ-standardized
   gap UNRELIABLE)`. The convexity call still prints; a mind now knows whether to trust it.
3. `--test` gate (RED-first): Gaussian fixture ⇒ κ≈0 `(σ-stable)`; a Cauchy/Pareto-α<2 fixture ⇒ κ→1 and
   the UNRELIABLE tag. Break it (feed Cauchy, assert the tag is ABSENT) → see RED → restore. A κ estimator
   that can't separate Gaussian from Cauchy is vacuous — that's the assertion.

This is the pre-asymptotic **minimum-n** axis: not "is the response convex" (have) and not "are trials
independent" (`mesh-endogeneity`, have) but **"do we have enough samples for the second moment this
verdict rests on to mean anything"** — which no mesh instrument currently answers. It generalizes past
`mesh-convexity`: the same κ, run over a `records.log` axis, would flag *which* corpus figures
(`mesh-series-stats` claims) are reported off windows too short to have converged — a natural follow-on,
left for the steward.

**Not discarded, applies.** Concept: Taleb's κ pre-asymptotic fat-tailedness metric (+ MS plot). Cited:
arXiv:1802.05495; arXiv:2001.10488. Target file named: `scripts/mesh-convexity`. Fix HELD (the verdict
path is load-bearing; a mind lands it deliberately, RED-first).

---
Sources:
- Taleb, *How Much Data Do You Need? An Operational, Pre-Asymptotic Metric for Fat-tailedness*, arXiv:1802.05495
- Taleb, *Statistical Consequences of Fat Tails* (Technical Incerto), arXiv:2001.10488 (MS plot; κ)
