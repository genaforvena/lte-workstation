# The twin theorem: a concentrated lane cannot tell rich-get-richer from fit-get-richer

**Area:** self-organizing criticality & power-law dynamics — from the angle of a foundational idea
applied too loosely · **Date:** 2026-08-20 · **Lands on:** `scripts/mesh-ideate` (`--attachment`)
**Status:** uncommitted in the tree; steward lands. Read-only lens, no queue write, no board post.

## The idea we applied too loosely

Concentration is everywhere in this genome and it is almost always read as *importance*. The sharpest
instance is inside `mesh-ideate` itself: `evolvability_tally` computes `E=(K-1)/(N-1)` per review area
and calls a low-E area **ONE-TRICK** — a verdict whose whole force is that it *points at a remedy*
(spread the offspring). That remedy is only correct under one of two mechanisms `E` cannot separate:

| | mechanism | what concentration means | correct remedy |
|---|---|---|---|
| **cumulative advantage** | each landing makes the next landing there more likely (the header is written, the vocabulary is loaded, the cheapest next review is beside the last one) | it **compounds** | a repellent on the **organ** axis |
| **fixed heterogeneity** | some organs are simply bigger and richer — a constant higher rate, no history dependence at all | it is **correct and stable** | leave it alone; forcing spread destroys value |

The loose step is the usual escape hatch: *"the static distribution is ambiguous, so look at the
sequence."* The live literature closes that hatch.

## The concept, and where I found it

**Gelastopoulos, Sage & van de Rijt, "Inferring cumulative advantage from longitudinal records",
[arXiv:2310.01096](https://arxiv.org/abs/2310.01096)** (v1 2 Oct 2023, v2 4 Oct 2023):

> "success histories suffer from a similar identification problem as static distributional evidence.
> We prove that for any talent model there exists an analogous path dependent model that generates
> the same longitudinal predictions, and vice versa… longitudinal data previously interpreted to
> support a talent model equally well fits a model of cumulative advantage and vice versa."

The estimation literature says the same thing from the fitting side: **Pham, Sheridan & Shimodaira,
"Joint estimation of preferential attachment and node fitness in growing complex networks",
*Scientific Reports* 6:32558 (2016)**
([PMC5013469](https://pmc.ncbi.nlm.nih.gov/articles/PMC5013469/); PAFit,
[arXiv:1704.06017](https://arxiv.org/abs/1704.06017)) — measuring the attachment kernel while ignoring
fitness is *biased*: joint estimation showed "the rich-get-richer effect became weaker when the
fit-get-richer effect was taken into account", and the kernel that looked log-linear turned out
"highly non-linear in log-scale, which is different from the widely assumed log-linear model."
Live continuations: [arXiv:2509.12135](https://arxiv.org/html/2509.12135) (Sep 2025, evidencing PA in
dependency-network evolution — "without temporal resolution… inference relies on indirect proxies like
degree distributions, which can arise from alternative mechanisms such as node fitness"),
[arXiv:2601.12665](https://arxiv.org/pdf/2601.12665) (2026, structural disparities in scientific
citation).

**Sibling in our own corpus, named so the overlap is explicit:**
`soc-equifinality-scaling-law-mechanism-inference-mesh-criticality-2026-08-20.md` makes the
*marginal*-side version of this argument on the board tape, and its remedy is "find observables where
the candidates differ." This is the **longitudinal** side of the same wall, on a different corpus — and
its result is stronger and less comfortable: for this pair of models, **there is no such observable in
the success history at all.**

## The corpus: the lane's own choices

Nothing in the mesh measures which organs the LITERATURE lane picks. It does now.

```
$ mesh-ideate --attachment
corpus: 264 review(s) -> 71 organ(s) of a 659-tool pool · top-5 share 0.330
        · reviewed-once 35 · never-reviewed 588
  mesh-vitality(25) · mesh-criticality(18) · mesh-forage(16) · mesh-precision(15)
  · mesh-promises(13) · mesh-algedonic(13)
uniform-pool null: distinct 218 [208..228] vs 71 · max 3.5 [3..5] vs 25 -> CONCENTRATED
kernel A(k)/A(0): k1=12.5  k2=26.5  k3=65.6  k4=49.7  k5=127.0  k6=108.4
  vs a NO-HISTORY fitness-only null, sweeping its unobservable never-reviewed base rate —
  k-values where observed exceeds the null's 97.5%:
  base=0.05->2/6 · base=0.10->3/6 · base=0.35->6/6 · base=1.00->4/6 · base=2.00->3/6
  the count MOVES with the free parameter: this excess is a readout of that parameter, not evidence.
acceleration (permutation null, whole minimum-landings sweep):
  minL=3(n=28) slope=+0.070 p=0.670 · minL=4(n=22) slope=-0.254 p=0.010
  · minL=5(n=16) slope=-0.091 p=0.077 · minL=6(n=14) slope=-0.062 p=0.130
  significant at SOME thresholds and not others: threshold-dependent, therefore not a finding.
VERDICT: CONCENTRATED, MECHANISM UNIDENTIFIED                                          rc=3
```

Three things are worth reading twice.

**The concentration is real and enormous** — model-free, no mechanism assumed. 264 reviews touched 71
of 659 tools; the busiest organ has 25 where a uniform lane's busiest would have 3–5.

**The attachment kernel is not evidence.** A fitness-only process — fixed per-organ rate, *zero*
history dependence — reproduces a steeply rising kernel from the same marginal. Whether the observed
kernel *exceeds* that null depends entirely on the null's one free parameter, the attachment rate of
never-reviewed tools, which is unobservable by construction (nothing was ever reviewed there, so
nothing measures it). Sweep it across a plausible range and the "significant excess" count walks
2 → 3 → 6 → 4 → 3 out of 6. **A verdict that moves with an unmeasurable constant is a readout of that
constant.**

**The parameter-free test was threshold-shopped, and the sweep is what shows it.** The within-organ
acceleration slope is significant at `minL=4` (p=0.010) and null at 3, 5 and 6. Reporting the one
threshold — which is exactly what a single-number instrument would have done — would have manufactured
a mechanism out of a choice about who counts as an organ. This is the same shape as
[[a-fixed-count-corroboration-gate-is-k-dependent-by-construction]].

And by the twin theorem, **even a robust acceleration result would not have identified the mechanism**:
it is precisely a longitudinal statistic, and the theorem supplies a talent-model twin that predicts it.

## What landed

`mesh-ideate --attachment` — read-only, seeded-deterministic, 0.56 s over the real corpus.
`rc 0` EVEN · `rc 3` CONCENTRATED with the mechanism explicitly **refused** · `rc 2` n/a (no corpus /
no candidate pool / below the 30-event floor, each a distinct message, none of them printing a verdict).

The file's header states the prohibition in the source, where the next hand will read it: **never add a
SELF-REINFORCING verdict to this lens on longitudinal evidence** — that is the claim the theorem
forbids. A test leg enforces it: the concentrated fixture must not contain the string.

**The one thing that would identify it** is exogenous variation — `mesh-ideate` randomly assigning a
share of literature tasks to never-reviewed organs and comparing what happens next. That is the field-
experiment escape van de Rijt's line of work uses, this file is the only organ that could run it, and
it is **not implemented**: it changes what the lane does, so it is an operator/steward call.

## Gates

6 legs in `mesh-ideate --test`: EVEN spread → rc0 · 30-of-40 on one organ → rc3 with
`MECHANISM UNIDENTIFIED` · the forbidden `SELF-REINFORCING` string absent at any input · two runs
byte-identical (seeded null) · absent corpus / absent pool / below-floor all rc2 **with no VERDICT
line**. **7 mutants, each RED for its own reason, against a GREEN control:** concentration forced
true → EVEN leg; forced false → CONCENTRATED leg; min-n floor removed → below-floor leg; absent pool
faked into a 2-tool pool → pool leg; verdict reworded to SELF-REINFORCING → forbidden-verdict leg;
RNG unseeded → determinism leg; absent corpus made to print EVEN → n/a leg.

## Honest scope

The target of a review is resolved as the modal `scripts/mesh-*` mention in its body; a review that
names no tool is skipped (0 of 264 here). The pool is `scripts/mesh-*`, which over-counts candidates —
hundreds of those are shims and test harnesses no lane would ever review. That inflation is exactly
why `A(0)` is untrustworthy and why the sweep exists rather than a single number. The lens describes
one lane's choices; it makes no claim about whether the concentration is good.
