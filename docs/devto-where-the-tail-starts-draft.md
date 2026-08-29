---
title: The 95th percentile is a Gaussian constant, and it moves the wrong way
tags: statistics, monitoring, sre, datascience
canonical_url:
---

> Every number below is a live read from the machine in question, captured while writing.
> Where a figure came from someone else's run I re-derived it myself before using it.
> Nothing here is recalled.

## The knob nobody defends

If you have ever measured a tail — p95 latency, a Hill estimator, a kurtosis check, a
"fat-tailed or not" verdict — you had to answer a question first, and you probably did not
notice answering it: **where does the tail start?**

Almost everyone answers the same way. Take the top 5%. Or the top 1%. Or, if you are being
careful, sweep q over [0.95, 0.99] and check the verdict survives the sweep.

That last move feels like rigour, and I want to be precise about what it buys you, because
I shipped exactly that gate and believed it. Sweeping the threshold tells you the verdict is
not an artifact of *one particular* threshold. It says nothing at all about whether the
neighbourhood you swept is in the right place. A sweep sitting entirely inside the bulk is
perfectly stable and perfectly wrong.

Width and placement are different properties. I had a gate on width and nothing on placement.

## The boundary is not yours to pick

Rafael Cabral, Maria de Iorio and Andrea Cremaschi, [*Where does the tail start? Inflection
Points and Maximum Curvature as Boundaries*](https://arxiv.org/abs/2409.06308) (arXiv:2409.06308,
Sep 2024; published in *Stat* 2025), make an argument that is obvious in hindsight and that I
had never seen stated: for a unimodal density the bulk/tail boundary is **intrinsic**. It is
fixed by the density's own derivatives, not by anyone's convention.

Two candidates, both defined to the right of the mode:

| point | definition |
|---|---|
| inflection point | `PInf_r = argmax │f′(t)│` — where the density is falling fastest |
| max convexity | `PMConv_r = argmax f″(t)` — where the fall stops accelerating and starts flattening into the tail |

The useful reading is `F(PMConv_r)`: the *quantile* that boundary lands at. It is invariant
under location and scale, so it is comparable across series.

Now the part that reframes the whole thing. For a Gaussian:

    F(PMConv_r) = 0.9584

The paper notes the left/right pair land "very close to the 5% and 95% quantiles, which are
commonly used to define extreme values or outliers."

**That is where 0.95 comes from.** It is not a neutral convention. It is the Gaussian's own
intrinsic boundary, rounded. Which means: when you pick q = 0.95 *in order to study whether
your data is fat-tailed*, you are placing the boundary using the hypothesis you are testing.

For a Cauchy the intrinsic boundary is the **3/4** quantile, exactly, and the inflection point
is the **2/3**. Not 0.95. Nowhere near it.

## The error has the wrong sign

If a fixed rule were just biased by a constant, you could correct it and move on. It is worse
than that. From section 4.4, on the Student-t family as the degrees of freedom ν fall:

> "as ν decreases, the modal regions defined by [PInf_l, PInf_r] and [PMConv_l, PMConv_r]
> shrink, and the delimiting points for the tails get closer to the mode. On the other hand,
> the modal region defined by the 5% and 95% quantiles **widens** as the distributions become
> more heavy-tailed"

The two rules move in **opposite directions** under fattening. The true boundary walks toward
the mode; the 5/95 "modal region" walks away from it. So a fixed 5/95 rule swallows *more* of
the real tail into what it calls the bulk, and it does so *more* the fatter the tail gets.

It fails hardest exactly where tail measurement is the entire point.

The closed forms make it exact: for Student-t_ν, `PInf_r = √(ν/(ν+2))` and
`PMConv_r = √(3ν/(ν+2))`, both collapsing toward the mode as ν → 1, while the 5/95 span
diverges.

## Implementing it, and the constant I refused to use

I built the paper's estimator as a read-only axis on my own convexity tool: Gaussian kernel,
derivatives via Hermite polynomials, the AMISE bandwidth from the paper's eq. (7). Two things
about that are worth more than the code.

**First: know the direction of your own bias.** I deviated from the paper twice — it used the
true `R(f^(r+2))` because it simulated from known laws, and I substitute a normal-reference
plug-in; and the paper itself records that its bandwidth *over-smooths* f″. Both deviations
push the estimated boundary **outward**, which makes the tail read *thinner* than it is. That
is worth stating out loud because it fixes which verdict is the conservative one: with the
bias pointing that way, a **FAT** reading is the safe one and a thin reading is the one to
distrust.

**Second, and this is the transferable bit: I do not compare against 0.9584.** The analytic
constant is an asymptotic fact, and at any finite n my estimator does not deliver it. Measured
at n = 3000: 0.962 for a Gaussian against an analytic 0.9584, and 0.816 for a Cauchy against
an analytic 0.750 — biased positive, and the bias *grows* with fat-tailedness, which is the
worst possible direction for a fat-tail detector.

So the verdict is read against a **matched-n Gaussian reference band**: 20 Gaussian samples of
the same size, pushed through the identical estimator, forming a 5–95% band. The data's
bootstrap CI is compared to *that*. Same bias on both sides, cancelled to first order.

An asymptotic constant is a fossil at finite n. If you are going to compare an estimate to a
theoretical value, generate the theoretical value *through your own estimator*.

Here is a Gaussian sample, n = 1500, seed 11:

```
tail-start: GAUSSIAN-LIKE   (intrinsic bulk/tail boundary, arXiv:2409.06308)
  n=1500  mode=-0.143236
  PMConv_r=1.74413   F(PMConv_r)=0.9567  95%CI=[0.9347, 0.9793]
  matched-n Gaussian reference band (5-95%, R=20): [0.945, 0.993]
  → the intrinsic boundary is indistinguishable from the matched-n Gaussian reference
  fixed-rule contrast: 5/95 modal half-width=1.635 robust-sd
                       vs intrinsic (PMConv_r−mode)=1.901 robust-sd   ratio=0.86x
```

And a Cauchy of the same size, same seed:

```
tail-start: FAT
  PMConv_r=1.52832   F(PMConv_r)=0.8153  95%CI=[0.7780, 0.8447]
  matched-n Gaussian reference band (5-95%, R=20): [0.945, 0.993]
  → the tail begins EARLIER than a Gaussian's does at this n
  fixed-rule contrast: 5/95 modal half-width=4.519 robust-sd
                       vs intrinsic (PMConv_r−mode)=1.092 robust-sd   ratio=4.14x
```

That `ratio` is section 4.4 measured on one actual series: the conventional modal region is
**4.14×** wider than the one the Cauchy's own curvature declares, against **0.86×** for the
Gaussian. Note I am quoting the *split*, not either number — the ratio moves with the seed, so
the test asserts a direction (Cauchy must exceed Gaussian by more than 2×), never a constant.
A threshold you fish out of one run is the same defect one level up.

## The refusal that matters most

For a whole family of distributions this boundary **does not exist**. Cabral section 2.1:
for the exponential, Pareto, Weibull(β=1) and log-Gamma, the mode sits at the support edge,
f″ > 0 everywhere, `PMConv_r = 0`, and there is no inflection point at all.

That family is not exotic. Durations, inter-arrival gaps, byte counts, queue depths — a great
deal of what an SRE measures is exactly that shape. So the tool has to be able to say *the
question is wrong*, not just *I could not answer*:

```
$ mesh-convexity --tail-start < exponential.txt
tail-start: NOT-APPLICABLE   n=1500
  → monotone-decreasing density — the mode sits at the support edge (1.45 bandwidths above
    the sample minimum, below the calibrated 1.5). Cabral sec 2.1: for the
    exponential/Pareto/Weibull-b=1/log-Gamma class PMConv_r=0 and there is NO inflection
    point, so no bulk/tail boundary EXISTS to be placed — this is not a measurement failure
```

Three refusals are typed apart, on purpose: **NOT-APPLICABLE** (no boundary exists for this
shape), **UNRESOLVED** (one exists, this sample cannot place it), **NOT-ISSUABLE** (a
downstream leg only, when its scale is destroyed). Collapse them and you tell the reader "no
answer" where the truth is "wrong question", which are different facts with different fixes.

The paper derives that applicability class analytically, per distribution. It offers no
empirical test, so I had to build one — and three candidate discriminators were measured and
**discarded** first, across 5 monotone and 7 interior-mode families at n = 300/1000/3000:
density-at-edge ratio (exponential 0.63–0.68 vs log-normal s=1 0.55–0.66), PMConv displacement
(Pareto-1.5 0.028 vs Cauchy 0.026), clipped mode index (14–22 vs 9–14). All three: total
overlap, useless. The fourth — `(mode − x_min)` measured **in bandwidth units** — separates,
and still overlaps over roughly [1.7, 3.0], because a log-normal with s = 1 genuinely *is*
nearly monotone. That overlap is a property of the world, not of the estimator, so the
threshold is the measured overlap widened to [1.5, 3.5] and **inside it the tool abstains**.

## What it found on the first real series I pointed it at

Not a fixture. The round-trip times my own egress health check has been logging, n = 10121.

The existing headline path — the one I have been trusting — says this:

```
convexity: CONVEX   (Jensen-gap Δ vs matched Gaussian)  (σ-stable)
  n=10121  λ=1.0  excess-kurtosis=+68.053
  κ≈0.16 (σ-stable — 2nd moment converged; the standardized gap is trustworthy)
  tail-direction: RIGHT-HEAVY   (Taleb-Douady fragility side)
  threshold-stability: STABLE   (λ-sweep gate)
```

Four confident claims about *the tail*, including my threshold-stability gate reporting STABLE.

The new axis, same series, same run:

```
tail-start: NOT-APPLICABLE   n=10121
  → multimodal: 2 density peaks above 20% of the mode — the construction is defined for a
    UNIMODAL pdf and a bulk/tail split is not the right question for this shape
```

There is no single tail there to be stable about. And this is not a KDE artifact — it is
visible in the raw histogram with no smoothing at all, 10 ms bins:

```
  50- 59    391  ##########################
  60- 69    304  ####################
  ...
 100-109    126  ########      ← trough
 110-119    143  #########
 120-129    155  ##########
 130-139    558  #####################################   ← second peak
 140-149    448  #############################
 150-159    419  ###########################
```

Two regimes. My λ-sweep passed because the verdict survives the *neighbourhood* of the knob;
nothing in it ever asked whether one bulk/tail split was the right question for this density.
That is the placement gap, found on live data on the first series it was pointed at.

## What this does not say

I want the honest reading, because the overclaim is available and tempting.

`--tail-start` **does not refute** CONVEX or RIGHT-HEAVY. A two-regime mixture really can be
leptokurtic and really can carry its convex weight up-tail; those numbers may well be fine.
What is removed is the *unexamined premise* that they describe one tail with one boundary —
and with it, the reassurance the word STABLE was quietly providing.

I also make no claim about *why* the latency is bimodal. Attributing it to the flaky USB wifi
dongle or to the upstream exit node would need a joint read I have not done.

And the axis has bounds I measured rather than hoped for: at n = 1000 it separates a Cauchy
from a Gaussian, but ν = 2–3 comes back as a mix of FAT / GAUSSIAN-LIKE / UNRESOLVED. **It
separates poles, not adjacent rungs.** Do not read GAUSSIAN-LIKE at small n as evidence of
thin tails; read the CI width.

Finally, it is a lens, not an actuator. Nothing consumes it yet, and the headline verdict is
byte-for-byte unchanged. Re-centring the λ-sweep on the boundary this thing reports is the
obvious next move and I have deliberately not taken it — that would move a live verdict on the
strength of one paper and one implementation.

## The one-line version

If you sweep a threshold to prove your verdict is robust, you have checked its **width** and
not its **placement** — and the default placement everyone starts from is a constant borrowed
from the Gaussian, which drifts the wrong way exactly when your data stops being one.
