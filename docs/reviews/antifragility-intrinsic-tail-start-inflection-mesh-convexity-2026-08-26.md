# Antifragility / convexity / ruin — live review: WHERE DOES THE TAIL START? The boundary every tail claim assumes and none of ours measured

**Date:** 2026-08-26 · **Node:** mesh-home · **Mind:** genome · **Lane:** LITERATURE (live review), idea-queue
**Area:** antifragility, convexity & ruin theory (Taleb) · **Angle asked for:** a known CRITIQUE or failure mode
**Landed in:** `scripts/mesh-convexity` → new read-only `--tail-start` axis. Uncommitted; steward lands.

---

## The source

**Rafael Cabral, Maria de Iorio, Andrea Cremaschi — "Where does the tail start? Inflection Points and
Maximum Curvature as Boundaries", arXiv:2409.06308v1 [math.ST], submitted 10 Sep 2024; published in
*Stat* (Wiley) 2025, doi 10.1002/sta4.70071.**

Found by web search; **verified by fetching arxiv.org/html/2409.06308v1 with `curl` and reading the
full text**, not from a search summary. Sections used: 2.1 (the definitions), 3 + 3.1 (the estimator,
its bandwidth, and its measured MSE), 4.4 (the Student-t closed forms and the counter-movement
statement), 5 (Discussion). Taleb's *Statistical Consequences of Fat Tails* (arXiv:2001.10488) is cited
by the paper as its own reference point for the heavy-tail program — this sits squarely inside the area,
not adjacent to it.

## The critique

Every tail claim in this area is a claim about *the tail*: κ, the Hill/GPD tail index, the Jensen gap
under a convex potential, the Taleb–Douady left-tail direction. All of them need to know where the tail
**starts**. Standard practice picks a quantile — the top 5%, the 95th percentile, a sweep over
q ∈ [0.95, 0.99] — and this choice is treated as a nuisance parameter rather than a modelling claim.

Cabral et al. show that for a unimodal density the boundary is **not a choice at all**. It is fixed by
the density's own derivatives:

| point | definition (paper eq. 4, 5) |
|---|---|
| inflection point | PInf_r = argmax_{t>θ} \|f′(t)\| — equivalently the root of f″ right of the mode θ |
| point of maximum convexity | PMConv_r = argmax_{t>θ} f″(t) |

and the natural reading is **F(PMConv_r)**, the *quantile* the boundary falls at, which is invariant
under location and scale and therefore comparable across series.

**The conventional threshold is calibrated to the Gaussian.** The paper: for a Gaussian,
F(PMConv_r) = **0.9584**, and PMConv_l/PMConv_r "are very close to the 5% and 95% quantiles, which are
commonly used to define extreme values or outliers". For a Cauchy the boundary is the **3/4** quantile
exactly and PInf_r the **2/3** (sec 4.4). So choosing q = 0.95 in order to study fat tails places the
boundary using precisely the assumption under test.

**And the error has the wrong sign — this is the part that bites.** Verbatim, sec 4.4:

> "as ν decreases, the modal regions defined by [PInf_l, PInf_r] and [PMConv_l, PMConv_r] shrink, and
> the delimiting points for the tails get closer to the mode. On the other hand, the modal region
> defined by the 5% and 95% quantiles **widens** as the distributions become more heavy-tailed"

The two rules move in **opposite directions** under fattening. A fixed 5/95 rule does not mis-place the
boundary by a constant — it swallows *more* of the true tail into the "bulk" the fatter the tail gets.
It fails hardest exactly where a fragility measurement matters most. The closed forms make it exact:
for Student-t_ν, PInf_r = √(ν/(ν+2)) and PMConv_r = √(3ν/(ν+2)), both falling toward the mode as ν → 1
while the 5/95 span diverges.

## Why this is not a landing we already have

The mesh has **fifteen** prior reviews in this area (κ pre-asymptotics, Parisian ruin, the omega model,
the generalized drawdown, single-big-jump, log-rate convexity, sharp-restart, Taleb–Douady left-tail
direction, degeneracy-vs-redundancy, joint-failure amplification, criticality boundary, plug-in buffer,
bounded inflection, threshold stability, ergodicity breaking). The nearest neighbour is the one that
looks closest and is in the *same file*:

- `antifragility-threshold-stability-lambda-gate-mesh-convexity-2026-08-10.md` — the **threshold-fishing
  trap** (Zhou, arXiv:2606.16511). That gate asks whether a verdict **survives a neighbourhood** of the
  knob, and `mesh-convexity` now re-runs its whole bootstrap over λ × {0.5, 0.71, 1, 1.41, 2}.

That is a statement about the **width** of the sweep. It says nothing whatever about its **placement**.
A sweep sitting entirely inside the bulk, or entirely past the boundary, is perfectly "stable" and
perfectly wrong — stability about the wrong region. **Cabral supplies exactly the term that gate
assumes and never checks: where the neighbourhood should be centred.** The two compose, the same way κ
(which certifies the *denominator*) and the λ-sweep (which certifies the *numerator*) are orthogonal and
neither substitutes for the other.

The one other review with "inflection" in its name — `antifragility-bounded-inflection-recovery-curvature-mesh-resource-guard-2026-07-31`
— is about the convex→concave inflection of a **response curve** ("antifragility up to a point"), a
different object in a different file. Same word, different derivative of a different function.

## What landed: `mesh-convexity --tail-start`

Read-only, on-demand, acts never, writes nothing. Reads a numeric series on stdin.

**The estimator is the paper's own** (sec 3/3.1): Gaussian kernel, derivatives via Hermite polynomials,

    f_n^(r)(x) = (−1)^r / (√(2π) n h^(r+1)) · Σ_i H_r(u_i) exp(−u_i²/2),  u_i = (x − X_i)/h

with H₀ = 1, H₁ = u, H₂ = u² − 1, and the AMISE bandwidth of eq. (7). Pure stdlib (no numpy on this
node); the kernel is truncated at 6h, which is below float noise, and the grid is bisect-indexed, so a
900-point series costs ~1s and n = 1000 with the full bootstrap ~5s.

**Two deviations from the paper, both named in the code, and both push the SAME way.** The paper used
the *true* R(f^(r+2)) because it simulated from known laws; we substitute a normal-reference plug-in.
And the paper itself records that the AMISE bandwidth **over-smooths** f″ — "we would need a smaller
bandwidth than the one given by (7)". Both push the boundary **outward**, so the tail reads *thinner*
than it is and **FAT is the conservative verdict**. Measured directly: at n = 3000 the estimator returns
F̂(PMConv_r) = 0.962 for a Gaussian (analytic 0.9584) and 0.816 for a Cauchy (analytic 0.750) — the bias
is positive and *grows* with fat-tailedness.

**Which is why the verdict is read against a MATCHED-n GAUSSIAN REFERENCE, never the analytic constant.**
20 Gaussian samples of the same n are pushed through the identical estimator to form a 5–95% reference
band; the data's bootstrap CI is compared to *that*. The reference carries the same bias and cancels it
to first order. This is the `calibrate-a-derived-axis-against-the-live-corpus` rule applied to an
estimator rather than a corpus: the asymptotic constant is a fossil at any finite n.

### The three legs beside the boundary

1. **The fixed-rule contrast — the critique itself, measured on the caller's own series.** Prints the
   5/95 modal half-width and the intrinsic half-width (PMConv_r − mode), both in robust-sd units, and
   their ratio. A Gaussian reads **1.13×**; a Cauchy reads **3.03–3.33×**. That divergence *is* sec 4.4,
   and it is what `--test` gates on.
2. **The λ-placement leg — the missing term.** cosh(λz) is ~quadratic while |λz| ≪ 1 and exponential
   once |λz| ≫ 1, so the λ-potential's implied tail boundary sits at |z| ≈ 1/λ: **the shipped λ = 1.0
   asserts, with nothing behind it, that the tail starts at one standard deviation.** The leg reports
   λ\* = 1/z(PMConv_r) and whether the sweep window brackets it. **This correspondence is ours, not the
   paper's, and the output says so.** On a Gaussian, λ\* ≈ 0.6 → BRACKETED. On a Cauchy at n = 600,
   λ\* = **11.9** against a sweep window of [0.5, 2.0] → **ABOVE the sweep**: the stability gate was
   being asked about a region the data does not call the tail.
3. **Three refusals, typed apart on purpose.** `NOT-APPLICABLE` (no boundary *exists* for this shape),
   `UNRESOLVED` (one exists, this sample cannot place it), `NOT-ISSUABLE` (the λ leg alone, when the
   z-scale is destroyed). Collapsing them would tell a reader "no answer" where the truth is "wrong
   question" — the distinction the whole na-vs-absent doctrine turns on.

### The applicability class, and the one calibrated constant

Cabral sec 2.1 excludes a family outright: for the **exponential, Pareto, Weibull(β=1) and log-Gamma**
distributions the mode is *at the support edge*, PMConv_r = 0, f″ > 0 everywhere, and there is **no
inflection point at all** — "not providing a practical delimiting point between the modal region and
the tail". For those series no boundary exists, and returning a number would be inventing one. This
matters here: many mesh series (durations, gaps, byte counts) are exactly that shape.

The paper never proposes an *empirical* test for this — it derives the class analytically per
distribution. So one had to be built, and **three candidates were measured and discarded** across 5
monotone and 7 interior-mode families at n = 300/1000/3000:

| candidate | monotone class | interior-mode class | verdict |
|---|---|---|---|
| density-at-edge ratio f̂(x_lo)/f̂max | exponential 0.63–0.68, half-normal 0.61–0.65 | log-normal s=1 **0.55–0.66** | total overlap — discarded |
| PMConv_r displacement from the mode | Pareto-1.5 **0.028** | Cauchy **0.026** | total overlap — discarded |
| support-clipped mode grid index | exponential 14–22 | log-normal s=1 **9–14** | total overlap — discarded |
| **(mode − x_min)/h₀, in bandwidth units** | **0.93–3.01** | **1.72–2423** | separates, *with* an overlap |

The fourth separates. It still overlaps over roughly [1.7, 3.0] — **a log-normal with s = 1 genuinely
*is* nearly monotone**, so this is a property of the world and not of the estimator — so the band is the
measured overlap widened to the nearest 0.5, **[1.5, 3.5]**, and inside it the tool **abstains** rather
than guessing. The constant carries its calibration table in the source header. Fishing a threshold here
would have reproduced, inside this very landing, the exact defect the file's previous review is about.

### Resolution, measured, so nothing over-claims it

At n = 1000 the axis calls a Cauchy FAT and reads GAUSSIAN-LIKE for ν ≥ 5 and for a Gaussian; **ν = 2–3
is where it runs out of power**, returning a mix of FAT / GAUSSIAN-LIKE / UNRESOLVED. **It separates the
poles, not adjacent rungs.** Cabral's own simulation predicts this: MSE 0.245 for PMConv on a Cauchy at
n = 100, and PMConv is always noisier than PInf because it is one derivative further out.

## Gates

Six new arms in `mesh-convexity --test`, alongside the pre-existing suite:

1. **the two poles** — Gaussian → GAUSSIAN-LIKE, Cauchy → FAT;
2. **the critique as a DIRECTION, not a constant** — the fixed-rule contrast ratio must be >2× larger on
   the Cauchy than on the Gaussian. A tool reporting only the 5/95 rule, or only the intrinsic boundary,
   cannot produce this split;
3. **the matched-n reference band must actually be drawn** (else the verdict silently falls back to the
   analytic constant against a biased estimate);
4. **NOT-APPLICABLE is a shape verdict** — an exponential must refuse, must *name* the monotone class,
   and must print **no** boundary quantile; a bimodal series must refuse with a *different* reason;
5. **the n-refusal fires before any estimate is attempted**;
6. **the placement leg must MOVE with the data** — bracketed for a Gaussian, outside the window for a
   Cauchy. A λ\* that reads BRACKETED for both is hardcoded and the leg is vacuous.

## Bounds — what this does NOT do

- **It is a lens, not an actuator.** Nothing consumes `--tail-start` yet; the headline CONVEX/ROBUST
  verdict and the λ-sweep gate are **unchanged**, byte for byte. The placement leg *reports* that the
  sweep window can miss the boundary; it does not re-centre the sweep. Re-centring λ on λ\* is the
  obvious next step and is deliberately **not** taken here — it would move a live verdict on the
  strength of one review.
- **The applicability band abstains over a real overlap.** A log-normal with s ≈ 1 will read UNDECIDED
  and that is honest, not a bug to tune away.
- **ν = 2–3 is unresolved at n = 1000.** Do not read a GAUSSIAN-LIKE at small n as evidence of thin tails;
  read the CI width.
- **The λ↔boundary correspondence (|z| ≈ 1/λ) is ours.** The paper says nothing about cosh potentials.
  It is stated as a correspondence in the output and in the source, and it should be treated as a
  heuristic siting, not a theorem.
- **Only one organ touched.** Every *other* fixed-quantile tail threshold in the mesh is untouched by
  this landing and remains a candidate for the same critique.

## Artifact

`scripts/mesh-convexity` — `--tail-start` axis + doctrine header + six `--test` arms. Uncommitted in the
tree; steward lands.

## Mutation-verified

Seven mutants driven from a scratch copy; the harness **aborts loudly** if a mutation site is not found,
so a green can never mean "the mutant was never applied". All seven went RED, each at **its own**
assertion — the arms are independent, not one assertion doing all the work:

| mutant | arm that caught it |
|---|---|
| `ratio-blind` — the contrast uses the 5/95 rule for **both** terms, so the ratio is always 1 | fixed-rule divergence (gauss 1.00× / cauchy 1.00×) |
| `na-prints-quantile` — the monotone refusal falls through and prints a boundary anyway | "a NOT-APPLICABLE reading still printed a boundary quantile" |
| `mono-band-off` — MONO_LO → 0, the monotone class is never refused | exponential must read NOT-APPLICABLE |
| `minn-off` — no sample-size refusal | n = 20 must refuse before estimating |
| `lambda-hardcoded` — λ\* pinned to the anchor so placement cannot move with the data | Cauchy's λ\* read BRACKETED by the same window as a Gaussian's |
| `ref-band-analytic` — no matched-n reference drawn, verdict falls back to 0.9584 | Gaussian no longer reads GAUSSIAN-LIKE |
| `multimodal-blind` — the bimodal refusal collapses onto the monotone reason | "two different 'wrong question' answers collapsed onto one word" |

The Cauchy fixture's **n = 1500 is set by measurement, not by seed-picking**: across 12 independent
seeds the axis returned FAT 11/12 at n = 900 (one UNRESOLVED) and 12/12 at n = 1500, 2500 and 4000. The
fixture sits at the smallest n whose resolution was observed complete.

Full suite (pre-existing arms + the six new ones) green in the genome tree and green again from the
deployed `~/.local/bin/mesh-convexity`; 14.8 s.

## The live artifact — and what it says about a verdict we already publish

Run on a real series from this node, not a fixture: the **egress round-trip times**
(`avg=` from `~/.mesh/egress-health.log`, n = 10084).

    $ mesh-convexity --tail-start < rtt.txt
    tail-start: NOT-APPLICABLE   n=10084
      → multimodal: 2 density peaks above 20% of the mode — the construction is defined for a
        UNIMODAL pdf and a bulk/tail split is not the right question for this shape

The **same series**, through the tool's existing headline path:

    convexity: CONVEX   (Jensen-gap Δ vs matched Gaussian)  (σ-stable)
      n=10084  λ=1.0  excess-kurtosis=+67.986
      κ≈0.16 (σ-stable — 2nd moment converged; the standardized gap is trustworthy)
      tail-direction: RIGHT-HEAVY   (Taleb-Douady fragility side)
      threshold-stability: STABLE   (λ-sweep gate, arXiv:2606.16511)

**Four confident claims about "the tail" — CONVEX, σ-stable, RIGHT-HEAVY, and a threshold-stability
gate reading STABLE — on a series that does not have one tail to be stable about.** The λ-sweep passes
because the verdict survives its *neighbourhood*; nothing in it asks whether a single bulk/tail split is
the right question for this density. That is the placement gap, found on live data on the first series
it was pointed at.

**The bimodality is real, not a KDE artifact** — it is visible in the raw histogram without any
smoothing: a peak at 50–69 ms (391, 304 counts in 10 ms bins), a trough at 100–129 ms (126, 143, 155),
and a second peak at 130–159 ms (558, 437, 416), with the fat right shoulder beyond. Two egress-path
regimes. **No claim is made here about their cause** — attributing them to the RTL8822BU wedge or to
the phaedra exit node would need a joint read against `mesh-link-heal` and is not done in this review.

The honest reading of the contrast is narrow and worth stating exactly: `--tail-start` **does not
refute** CONVEX or RIGHT-HEAVY. A mixture of two regimes really can be leptokurtic and really can carry
its convex weight up-tail. What it removes is the *unexamined* premise that those numbers describe one
tail with one boundary — and it removes the STABLE qualifier's implicit reassurance, because stability
of a sweep says nothing when the region being swept is not one region.
