# Model recovery — a selector you have never inverted on known truth is not a measurement

*Live literature review, 2026-08-04. Predictive processing & the Bayesian brain, angle = a concrete
METRIC/EXPERIMENT the area uses to measure itself.*
*Landed: `scripts/mesh-precision --recover` (report-only, additive, uncommitted for steward).*

## The source (live, current)

**Hess, A. J., Iglesias, S., Köchli, L., Marino, S., Müller-Schrader, M., Rigoux, L., Mathys, C.,
Harrison, O. K., Heinzle, J., Frässle, S., & Stephan, K. E. (2025). "Bayesian Workflow for Generative
Modeling in Computational Psychiatry." *Computational Psychiatry* 9(1):76–99.**
[doi:10.5334/cpsy.116](https://doi.org/10.5334/cpsy.116) · open at
[PMC11951975](https://pmc.ncbi.nlm.nih.gov/articles/PMC11951975/).

This is the Zurich TNU's own workflow paper for exactly the model family this area runs on (Mathys is
the HGF's author; the worked example is a hierarchical perceptual + response model). It prescribes six
steps, and makes **recovery** the precondition for interpreting any fitted quantity — in two halves.

**MODEL recovery** — simulate a full dataset from each candidate, invert *all* candidates on it,
tabulate how often each wins. Verbatim:

> "All models could be identified well above chance level both when evaluating approximate LME winner
> frequencies as well as PXP values resulting from RFX BMS on the synthetic data set."

**PARAMETER recovery** — verbatim:

> "Parameter recovery was assessed by visually comparing simulated parameter values to MAP estimates
> obtained using the data-generating model and by calculating Pearson correlation coefficients *r*."

And the reason it is a *precondition* rather than a nicety, verbatim:

> "This step is an important part of Bayesian workflow because it establishes a boundary between the
> type of questions that can be addressed using the model space at hand, and those questions for which
> a meaningful answer cannot be expected."

Live and continuing, not a settled ritual — *Computational Brain & Behavior* 2026,
[doi:10.1007/s42113-025-00261-9](https://doi.org/10.1007/s42113-025-00261-9), is about *improving*
parameter recovery with outlier-insensitive loss functions; recovery is still an instrument under
active development.

## Where we'd been — and the gap

The mesh checks its instruments hard, but **only on the data side**: order surrogates
(`mesh-novelty --control`, 08-03), matched controls, permutation nulls, mutation-tested gates, honest
n/a. Never on the **model side**. No axis in the genome has ever simulated data from a *known*
generative model and asked whether its own estimator gets that model back — grep-clean for
`simulation-based calibration`, `posterior predictive`, `rank histogram`, model/parameter recovery
across `scripts/` and `docs/`.

`mesh-precision --bmr` is the place that hurts. It ships a three-way verdict — WARRANTED / MARGINAL /
PARSIMONIOUS — from a closed-form Gaussian Bayes factor, and its only evidence of correctness is five
hand-made fixtures at **n=9**. Nothing said at what sample size, or for what size of departure, the
verdict carries information *at all*. That is the MCC-VIABILITY shape from 08-04 (all 18 areas
read FERTILE — a label that discriminates nothing) wearing Bayesian clothes, and the arithmetic here
can produce it: the Occam term `½·ln(1+n/k)` grows with n while the accuracy term is driven by a
departure that need not.

## What landed — `mesh-precision --recover`

Report-only. Draws R replicate datasets of size N from each model — REDUCED (mean at the prior μ₀) and
FULL (mean at μ₀+δσ) — inverts every one with the **shipped** estimator, and reports the 2×3 confusion
matrix, both recovery rates, the no-decision (MARGINAL) rate, the Pearson *r* between true and
recovered standardized departure, and **δ_min@80** — the smallest departure the selector calls
WARRANTED 80% of the time at that N.

The estimator is defined **once** (`BMR_CORE`, exec'd by both `--bmr` and `--recover`), so the thing
measured is the thing that ships rather than a twin of it — and `--recover --check <tape>` exposes the
shared core on a real tape so a gate can assert the two paths agree (leg 3 below).

```
$ mesh-precision --recover --n 200
IDENTIFIABLE  — recovery reduced=0.90 full=1.00, no-decision=0.04, param r=0.987, δ_min@80=0.3σ
$ mesh-precision --recover --n 30
WEAK          — recovery reduced=0.72 full=0.69, no-decision=0.23, param r=0.907, δ_min@80=0.6σ
$ mesh-precision --recover --n 9
UNIDENTIFIABLE— recovery reduced=0.41 full=0.30, no-decision=0.54, param r=0.780, δ_min@80=1.1σ
```

## The live measurement

Real sense, not a fixture: the AP-signal series from `~/.mesh/wifi-imac.log` (last 30 samples), prior
μ₀=100.

| window | `--bmr` verdict | departure | `--recover` at that n |
|---|---|---|---|
| n=30 | **WARRANTED** (lnK=6.00) | −0.73σ | WEAK · δ_min@80 = **0.7σ** · no-decision 0.23 |
| n=9 (same tape, last 9) | **MARGINAL** (lnK=0.84) | −0.70σ | UNIDENTIFIABLE · δ_min@80 = **1.1σ** · no-decision 0.54 |

Same sense, same departure, opposite readings — and the reason is now a printed number rather than a
shrug. At n=9 the selector's own confusion matrix (R=400) is

```
true FULL (δ=0.5σ):    WARRANTED 127 | MARGINAL 214 | PARSIMONIOUS  59
true REDUCED (δ=0):    WARRANTED  24 | MARGINAL 217 | PARSIMONIOUS 159
```

— the modal answer under **both** truths is MARGINAL. The verdict most likely to be printed at the n
of the tool's own test fixtures is the one that says nothing. And the live n=30 departure (−0.73σ)
sits barely above δ_min@80=0.7σ: the WARRANTED it earns is a coin-flip's width from unresolvable.

## Weakest joint (stated, not hidden)

The simulation is **well-specified by construction** — data drawn i.i.d. Gaussian, which is exactly
what the estimator assumes. So every number here is a **best case**. Real tapes are autocorrelated
(the RSSI series above emphatically so), which deflates effective n; true identifiability on live data
is *worse* than reported, never better. Same failure mode as the
cooscillate-p autocorrelation trap — named here rather than discovered later.
Second joint: δ_min@80 is a statistic of R draws, so it moves ±0.1σ at R=200; the seed is fixed
(`--seed`) so a quoted number is reproducible, but it is a draw's answer, not a constant.

## Gates (all red-first verified)

Five new legs in `mesh-precision --test`; whole suite 0.96s (well inside `mesh-doctor`'s timeout).
Each mutant was run from a scratch copy and killed **exactly its own leg**, control green:

| mutant | leg that went red |
|---|---|
| verdict always IDENTIFIABLE | `n=9 must read UNIDENTIFIABLE` |
| `--check` reclassifies independently | `--recover must invert the SHIPPED estimator` |
| `random.Random()` unseeded | `same seed must give the same recovery report` |
| n<3 renders a verdict instead of n/a | `n=2 must be UNKNOWN` |
| `par_r` hardcoded | `n=200 must recover the departure parameter at r≥0.9` |
| FULL model simulated at δ=0 | `n=200 must recover both models` |

(The first mutation pass was invalid and had to be re-run: `sed > file` drops the executable bit, so
every mutant went red for the wrong reason — every leg failing, all outputs empty. `chmod +x` the
mutant. A mutant can go red for the wrong reason.)

## The generalizable rule

**A selector you have never inverted on known truth is not a measurement — it is a label.** The mesh
already refuses to trust a difference whose sign is guaranteed by its arithmetic (matched control,
08-03); this is the other end of the same discipline — before trusting a *verdict*, generate data from
each model it claims to distinguish and check it comes back. Any tool that prints a classification
from a fitted quantity is eligible: `mesh-precision --bmr` (done), and, unmeasured,
`mesh-criticality`'s regime labels, `mesh-stress`'s bands, `mesh-forage`'s lane verdicts.

## Discarded on inspection (do not re-serve)

* **Simulation-based calibration (SBC)** — the natural sibling, but Hess et al. themselves only name it
  as "principled (but computationally expensive)" and do not run it; the mesh has no sampler producing
  posterior draws to rank, so there is nothing to build a rank histogram from.
* **Robust volatility updates for HGF**, [arXiv:2605.00966](https://arxiv.org/abs/2605.00966) (2026) —
  fixes negative posterior precision in variance-coupled HGF parents. Real and live, but no organ:
  the mesh runs no HGF hierarchy whose volatility parent could go negative.
* **Furutachi & Hofer, "Rethinking Predictive Processing", *Annu Rev Neurosci* (2026)** — surfaced by
  search but **not read** (annualreviews.org returns 403 to WebFetch; only the indexed abstract was
  visible: a historical overview re-evaluating the empirical support for sensory prediction-error
  signals). Not cited as evidence here. Worth a second attempt if anyone has access — flagged as an
  unread lead, not a discard on the merits.
