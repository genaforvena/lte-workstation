# LITERATURE (live review) — antifragility as a trajectory metric, not a single good shock

**Date:** 2026-09-10 · **Mind:** genome@mesh-home · **Area:** antifragility, convexity & ruin theory (Taleb)
**Angle:** a concrete metric/experiment the field uses to measure itself
**Status:** review artifact; application proposed, not implemented

## Source actually read

Koenig, Carwehl & Imrie, **“RESMETRIC: Analyzing Resilience to Enable Research on Antifragility”**,
arXiv:2501.18245 (30 Jan 2025), with the associated open-source artifact
[ResMetric](https://github.com/ferdinand-koenig/resmetric) and its [SEAMS 2025 proceedings entry](https://www.proceedings.com/content/080/080669webtoc.pdf).
I read the arXiv HTML sections describing the metric definitions (III-A–III-C), the gas-detection
case study (IV), and the discussion of detector sensitivity (IV-F), rather than relying on a title
or search snippet. The paper is still a live research artifact: the repository and package metadata
remain published, and the proceedings place the paper at SEAMS 2025.

## One concept we do not already embody

**The antifragility coefficient `αᵤ`**: measure antifragility as the *direction and rate of change of
a resilience metric `u` across successive disruptions*, not as the response to one stressor.

For successive dips, ResMetric computes the average change in `u` and maps it to a coefficient with
three interpretable regions:

- `αᵤ = 0`: `u` is monotonically decreasing — **fragile**.
- `0 < αᵤ < 1`: upward and downward changes are mixed; the value is a membership-like measure of
  monotonic improvement.
- `αᵤ ≥ 1`: `u` is monotonically increasing; larger values mean faster improvement.

The associated response experiment is dip-dependent: detect each disruption, calculate robustness,
recovery rate (`1 / dip length`) and recovery level/adaptive capacity, then calculate `αᵤ` over the
ordered sequence. This is a useful Taleb distinction: a convex response or a successful isolated
recovery is not yet antifragility; the system must improve after repeated shocks.

The case study supplies an important falsifier. The authors report that the inferred antifragility
changes materially when switching dip detection from local-maxima detection to linear-regression
segmentation; with the latter, a system with only one detected dip has no computable `αᵤ`. Thus the
metric must publish dip count and detector method, or a high score can be an artifact of event
segmentation. The paper also notes that a system can have superior overall performance while a
naive `ᾱᵤ` ranks another system as “more antifragile”.

## Why this is absent from the genome

The search of `scripts/` and `docs/reviews/` found adjacent but different mechanisms:

- `scripts/mesh-chaos-verify` measures a dose-response curve and its saturation/non-monotonicity;
  it does not calculate improvement across repeated disruptions.
- `scripts/mesh-chaos` has an explicitly held `--adaptive` idea and records individual outcomes, but
  no ordered resilience series and no `αᵤ`-style trajectory coefficient.
- `scripts/mesh-resource-guard` has depth-weighted accumulated hazard, Parisian dwell, and drawdown
  ruin; these measure current exposure/ruin, not whether recovery quality improves after repeated
  shocks.
- Existing antifragility reviews cover curvature, tail placement, dose ladders, performativity,
  and holdout recovery dispersion; none names or computes `αᵤ`.

This is therefore a new measurement axis, not another threshold on an existing ruin reading.

## One concrete application

Apply the metric to **`scripts/mesh-chaos`**, in its held `--adaptive` mode:

1. For each opt-in experiment, record `experiment_id`, target/failure class, dose, recovery time,
   coupled-health outcome, and a declared baseline quality `u` (for example, normalized recovery
   quality = `1 - recovery_seconds / timeout`, clipped to `[0,1]`).
2. After at least two comparable experiments, compute `αᵤ` over the time-ordered recovery-quality
   series; publish `dip_count`, segmentation rule, mean `u`, and `αᵤ` together.
3. Require a positive `αᵤ` to coexist with non-degrading coupled-system health before describing
   the sequence as antifragile. If there is one dip, mixed target classes, or incomparable doses,
   emit `UNRESOLVED`, never a fabricated antifragility score.

The first landing should remain report-only and isolated behind the existing opt-in and kill switch.
The decisive fixture is: recovery improves over three repetitions, but the detector finds only one
dip under its alternative segmentation method; the result must be `UNRESOLVED`, exposing that the
apparent antifragility claim has no trajectory evidence.

## Disposition

**Keep.** It supplies a concrete repeated-shock metric (`αᵤ`) and a measurement-level falsifier for
the genome’s existing “survived a shock / stress-response curved” claims. No tool edit was made in
this review turn.
