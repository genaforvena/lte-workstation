# Bayesian Model Reduction — does the data warrant the parameter? (predictive processing / free-energy)

*Live literature review, 2026-07-28. Cross-domain transfer to a distributed sensor mesh.*
*Landed: `scripts/mesh-precision --bmr` (report-only, additive, uncommitted for steward).*

## The mechanism (operational, not philosophy)

Predictive processing under the free-energy principle scores a model by its **variational free energy**:

> **F = complexity − accuracy**, where complexity = KL[posterior ‖ prior].

**Bayesian Model Reduction (BMR)** is the field's operational use of this: given a fitted **full** model,
evaluate — *in closed form, without re-fitting* — the free energy of a **reduced** model in which one
free parameter is pinned back to its prior. If **F_reduced < F_full**, Occam's razor **keeps the prior**:
the parameter did not earn its complexity. BMR is the actual mechanism the literature uses for structure
learning, post-hoc model selection, synaptic pruning, and as a metaphor for abductive reasoning and sleep.

This is a question **none of the mesh's existing predictive-processing organs ask**. They all assume the
parameter is worth fitting and only grade **how well** (precision = inverse variance) or **how surprising**
(prediction error). BMR asks the prior question: **should we fit it at all, or default to the prior?**

**Sources** (surveyed current, 2024–26):
- Friston, Parr & Zeidman, *Bayesian model reduction*, [arXiv:1805.07092](https://arxiv.org/pdf/1805.07092) (2018).
- Friston & Penny, *Post hoc Bayesian model selection*, NeuroImage 56(4) (2011).
- Unit-information prior (the BIC-consistent default): Kass & Wasserman, JASA 90 (1995);
  evidence bands: Kass & Raftery, *Bayes factors*, JASA 90 (1995).
- Current: BMR as Occam / structure learning in active inference
  ([arXiv:2311.10300](https://arxiv.org/pdf/2311.10300), 2023–25;
  [Frontiers Neurorobotics latent-pruning](https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2022.795846/full)).

## Where we'd been — and the gap

Predictive processing is the mesh's **most-saturated** review area; confirmed embodied before landing:
precision-weighting + marginal/contextual surprise + HGF **volatility** (`mesh-precision`, `mesh-novelty`),
salience-vs-novelty (`--probe` + novelty axis), **circular inference / n_eff** (`--independence`),
**predictive information** (`--num` pred_info), calibration (`mesh-reliability`), omission-as-error
(`mesh-pulse`). Every one grades a parameter *assumed worth having*. **Not embodied:** the
complexity↔accuracy **trade-off** that decides whether a departure from a prior is worth tracking at all.

## The transfer

`mesh-precision --bmr <tape> [--prior μ0] [--prior-n k]` compares, for a numeric stream, the **full**
model (mean free, inferred from data) against the **reduced** model (mean pinned at the prior expectation
μ0), using the closed-form Gaussian log-evidence:

```
K = ln p(D|full) − ln p(D|reduced) = ½·ln(π₀/(π₀+Λ))  +  ½·Λ²z²/(π₀+Λ)
      ( = accuracy − complexity )     └ Occam COMPLEXITY ┘   └ ACCURACY gain ┘
```

with per-point precision π = 1/var, data precision Λ = nπ, prior precision π₀ = kπ (the
**unit-information prior**, k = 1 pseudo-observation, BIC-consistent), and departure z = x̄ − μ0. Verdict
on the natural-log Bayes factor (Kass & Raftery bands): **WARRANTED** (K > 1 — the departure earns the
parameter, a data-driven estimate is justified) · **PARSIMONIOUS** (K < −1 — Occam keeps the prior; a
consumer *may* prune) · **MARGINAL** (|K| ≤ 1 — keep watching). Deterministic (var = 0) data is
special-cased: at the prior → PARSIMONIOUS (nothing to fit); off it → WARRANTED (a certain departure).

Report-only and advisory, exactly like `--independence`, `pred_info`, novelty, and `frame_coverage`: it
recommends what a consumer **may** prune, and touches **no verdict or weight** downstream.

## The live finding (mesh-home, `.mesh/disk-latency.log` write latency, n = 60)

```
vs prior μ0 = 0    →  WARRANTED   (departure 6.30σ · accuracy 1171.67 − complexity 2.06 · lnK 1169.61)
vs prior μ0 = 6.7  →  MARGINAL    (departure 0.32σ · accuracy   3.04 − complexity 2.06 · lnK    0.98)
```

The **same 60 samples** yield opposite readings by the prior — because BMR scores the data-**vs-prior
relation**, not the data alone. Against μ0 = 0 ("no latency expected") the ~7 ms write latency is
unmistakably real and worth tracking. Against the established **6.7 ms baseline**, the recent mean (7.059)
sits only **0.32σ** away: the accuracy the drift buys (3.04) barely exceeds the Occam penalty it costs
(2.06), landing at **lnK 0.98 — just under** the K = 1 bar. So BMR correctly **refuses to update the
baseline** for a small drift that has not yet earned it — the parsimony mechanism working, visibly, on a
real stream.

## The productive tension (stated, not resolved)

BMR is in **opponent tension with `mesh-sensorium --balance`** (which I landed the exteriority sibling of
earlier today). RR resiliency *wants* redundant streams — an input that rides along, changing no verdict
now, is failover insurance for when the primary dies. Occam/BMR reads that **same** ride-along input as
**complexity to prune**. Both are right on their own axis. So `--bmr` is a **diagnostic**, never a prune
command: it names which parameters are currently carrying the verdict vs riding along; whether to prune
one trades against resiliency, a decision that stays with the consumer. This is the same
opponent-processing shape `mesh-needs` makes visible for explore↔exploit — a tension to watch, not a knob
to max.

## The gate (RED-first verified)

`mesh-precision --test` drives the real `--json --bmr` path against fixtures pinning both signs: data
clustered **at** the prior → PARSIMONIOUS; the **identical** data far from the prior → WARRANTED (opposite
verdict, same numbers — proving the axis is the data-vs-prior relation); frozen-at-prior → PARSIMONIOUS;
n < 3 → UNKNOWN (no fabricated comparison). **Falsified:** inverting the free-energy sign
(`K = accuracy − complexity` → `complexity − accuracy`) flips both the WARRANTED and PARSIMONIOUS fixtures
and the gate goes RED (exit 1); restored → `smoke-test: ok`.

## Distinctness

Not a duplicate. `--independence` (circular inference) asks whether corroborating senses are *redundant*
(n_eff); `pred_info` asks whether variance is *structure vs noise*; CV/precision grade *how reliable* a
parameter is. **None** asks the parsimony question — whether the departure from a prior is worth a
parameter *at all* — which is BMR's, and the free-energy principle's, distinctive operational move.
Verdict-preserving and advisory, so it needs no sign-off.
