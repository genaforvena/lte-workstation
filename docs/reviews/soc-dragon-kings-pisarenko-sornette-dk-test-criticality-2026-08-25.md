# The largest event may not belong to the distribution every other verb fits

**Live review, 2026-08-25 — self-organizing criticality & power-law dynamics, angle as commissioned:
an OPERATIONAL mechanism, not philosophy.**
**Organ named and edited:** `scripts/mesh-criticality` (uncommitted; steward lands from the tree).

## What was already ours

Twenty-eight prior reviews sit in this area — the most worked ground in `docs/reviews/`, nearly all
landed on this same file. Checked before searching, so the review could not re-land:

| embodied | verb / review |
|---|---|
| branching ratio, subsampling-robust MR estimator | `--drift`, Wilting & Priesemann |
| Sethna exponent relation 1/σνz = (τt−1)/(τ−1) | `--crackling` |
| avalanche average-shape collapse | `--shape` |
| subsampling-deflated χ + coarse-graining recovery | `--coarse` |
| DFA / 1-f / Hurst · Taylor fluctuation scaling · allometric sublinearity | `--hurst`, `--taylor`, `--allometry` |
| SOB vs SOC · quasicriticality/Widom · dynamic range · rate-induced tipping | `--sob`, `--widom`, `--dynrange`, `--rtip` |
| coherent-noise generative null · record-dynamics aging null | `--coherent`, `--aging` |
| **equifinality — an exponent cannot identify a mechanism** | `--equifinal` |

So the *exponents* are thoroughly ours. What none of it questions is the premise underneath all of
them: that **one mechanism generated the whole distribution**.

## The mechanism, and where I found it

**V. F. Pisarenko & D. Sornette, "Robust statistical tests of Dragon-Kings beyond power law
distributions", *Eur. Phys. J. Special Topics* 205:95–115 (2012), arXiv:1104.5156.** Live
continuation applying the same tests: **Y. Chen et al., "Haicheng and Tangshan Earthquakes as
potential Dragon-Kings", arXiv:2504.21310 (April 2025)** — the literature is still running.

Sornette's dragon-king hypothesis: the very largest events in many heavy-tailed systems are **not**
the tail of the fitted law. They are produced by a *different* mechanism — a coupling or
amplification that only switches on at scale — and therefore sit **above** the power law rather than
on it. The consequence is operational, not taxonomic: a tail event is unforecastable by
construction, while a dragon king has its own mechanism and is diagnosable.

The **DK-test** makes it decidable on a small sample. Order the data x₁ ≥ … ≥ xₙ. If the bulk is
Pareto, ln(x/h) is exponential, so work in logs; by the Rényi representation the normalized spacings
zₖ = k·(wₖ − wₖ₊₁) are i.i.d. exponential, i.e. χ² with 2 df up to scale. Then

    T(r) = [ (1/r)·Σ_{k≤r} zₖ ] / [ (1/(n−r))·Σ_{k>r} zₖ ]   ~   F(2r, 2(n−r))   under H₀

with p(r) = 1 − F_cdf(T; 2r, 2(n−r)). H₀ is "all n come from one law"; H₁ is "the top r come from a
heavier one".

Two properties are why this test and not another, and both matter specifically here:

- **The p-value does not depend on the tail exponent.** It cancels in the ratio. Nothing has to be
  fitted first — which is decisive in this file, whose own comments call its marginal exponent
  estimates *"the underpowered half"* at mesh sample sizes. An exact test that never fits the thing
  it would be underpowered to fit.
- **It works on a few tens of observations**, and the authors explicitly recommend capping n at
  ~20–30 because zₖ = k·yₖ amplifies noise in the smallest spacings.

## What landed: `mesh-criticality --dragon`

Read-only, no alarm, same discipline as `--shape` and `--crackling`. It reuses the existing
`extract_avalanches()` sample, conditions on the (n+1)-th largest value as the threshold h (so h is a
reference point, never a fitted parameter), and scans r = 1…5. Three verdicts:

- `DRAGON-KING` — the top r are a different mechanism, gated on the **Bonferroni-adjusted** p;
- `THIN-TAIL` — the largest event is *closer* to the bulk than Pareto predicts, which on mesh tapes
  usually means a cap, a timeout, or a truncated log — deliberately not folded into "no dragon";
- `POWER-LAW-TAIL` / `INSUFFICIENT` (<12 observations — "no verdict", not "no dragon").

The F cdf is implemented via the regularized incomplete beta, keeping the file's no-numpy/no-scipy
contract.

**Live on this node right now:**

```
criticality dragon-king: POWER-LAW-TAIL (n=16 of 17 avalanches, threshold h=1;
  r=1:p=0.0348 r=2:p=0.0999 r=3:p=0.1850; best r=1 p=0.0348, Bonferroni p=0.1045 over 3 ranks)
```

The board's largest avalanche is a borderline case: raw p=0.035 would call it a dragon king, the
multiplicity correction does not. Reported as such rather than rounded to a verdict.

## Why scanning r is not optional

Two dragons of *similar* size leave only a small gap between **themselves**, so the r=1 test is
blind to them. Measured on the fixture: with the top two events each multiplied by 50,
**r=1 gives p=0.62 while r=2 gives p=0.0002**. A test fixed at r=1 reports "no dragon" on two of
them. That is now an assertion, not a remark.

## Gates

`mesh-criticality --test: smoke-test: ok`, eight new arms on constructed samples whose truth is not
in doubt — exact Pareto order statistics xᵢ = h·(n/i)^(1/b), which carry **zero** sampling noise, so
any p away from the middle is the construction and not luck:

- **(a) the control, first** — a clean Pareto sample must read `POWER-LAW-TAIL` (p=0.487). Without it
  every arm below passes on a detector that shouts at everything.
- (b) a 50× outlier → `DRAGON-KING` at r=1;
- (c) two co-equal outliers → caught at r=2, **and r=1 asserted blind**, or the r-scan proves nothing;
- (d) **scale invariance** — ×1000 on every observation leaves every p identical to 1e-12, the
  property that lets the test skip fitting an exponent;
- (e) a clipped top → `THIN-TAIL`;
- (f) <12 observations → `INSUFFICIENT`;
- (g) the F cdf against exact values: F(1;d,d) = ½;
- (h) **multiplicity** — a 6× outlier straddling the correction (raw 0.036 / adjusted 0.180) must not
  be called a dragon king, with the fixture's own straddle asserted so the arm cannot go vacuous.

Four mutants driven red: r fixed at 1, Rényi normalization dropped, `THIN-TAIL` branch removed, and
**gating on the raw minimum instead of Bonferroni**.

That last one is the reason arm (h) exists. It initially survived every other arm — and it is not
academic: on the live board it flips the verdict from `POWER-LAW-TAIL` to `DRAGON-KING`. A
correction nothing asserts is a correction that can be deleted green.

I also had to move `THIN-TAIL` from `min(p over r) > 0.95` to `p(r=1) > 0.95`: a clipped top gives
p(1)=0.998 while the later ranks regress to 0.699, so the original condition could never fire — a
verdict nobody would ever have seen.

## Honest bounds

- **No dragon king was found.** The live board reads `POWER-LAW-TAIL` at n=16, and n=16 is at the
  low end of the authors' own recommended range — this is a weak non-detection, not a clean bill.
- The test assumes the **bulk** is Pareto (or exponential in logs). If it is neither, a rejection
  says "not one Pareto law", which is weaker than "dragon king". `--equifinal` already covers why
  the shape of the bulk is itself underdetermined here.
- Conditioning on the (n+1)-th value means the verdict depends on n; that is the authors' design, but
  it makes n a reported parameter rather than a detail, and it is printed in every reading.
- Applied to avalanche sizes only. The natural next subjects — `mesh-link-heal`'s outage durations,
  the spend series — are not wired, deliberately: `dragon_kings()` takes a plain list, so pointing it
  at another tape is a caller change, not a new test.
