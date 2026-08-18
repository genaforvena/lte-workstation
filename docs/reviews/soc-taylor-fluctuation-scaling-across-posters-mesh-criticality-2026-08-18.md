# SOC & power-law dynamics (live review): **Taylor's law of fluctuation scaling** — the power law that lives ACROSS units, not along time, and the two nulls that must be carried with it

**Date:** 2026-08-18
**Area:** self-organizing criticality & power-law dynamics, from the angle of a RECENT result (2023–2026).
**Landing:** a mechanism we do NOT embody — **Taylor's power law of fluctuation scaling**, variance ∝ mean^b
across a POPULATION of units, with (a) the 2025 result that its OLS estimator is **asymptotically biased
exactly in this board's T/S regime**, and (b) the 2015 result that **block-sampling any right-skewed
distribution mints the law with no interaction at all**.
**Verdict:** concept ACCEPTED as new and load-bearing. **LANDED as code** — `scripts/mesh-criticality
--taylor`, read-only, no alarm (uncommitted, for the steward). Live measurement + its caveat below.

## The instrument

Taylor's law: over a collection of units *i*, `var_i = a · mean_i^b`. It is a power law, but it does not
live along time — it lives **across the population at one time**. `b = 1` is the independent-Poisson line
(a unit's clumping does not depend on its rate); `b → 2` is proportional/multiplicative fluctuation
(everything moving together); `b < 1` is under-dispersed (clocked). The intercept carries what the slope
cannot: `a` is the variance-to-mean ratio at unit rate.

**Recent result (the estimation side).** Truquet, Cohen & Doukhan, *Inferring the parameters of Taylor's
power law of fluctuation scaling*, **Proc. R. Soc. A 481(2326):20250248 (2025)**; preprint
*Inferring the parameters of Taylor's law in ecology*, **arXiv:2408.16023** (v1 2024-08-28, v2 2025-01-21).
Result: when the series length `T` and the unit count `S` grow together with `T/S → const`, the usual
normalized OLS statistics are **asymptotically biased** and the analytic confidence interval is wrong; a
bias correction is required. Found via a live web search on Taylor's-law/fluctuation-scaling 2025–2026;
the Royal Society landing page is paywalled (HTTP 403 to a plain fetch), the arXiv preprint is the readable
copy.

**The generative null that must ride with every TL number.** Cohen & Xu, *Random sampling of skewed
distributions implies Taylor's power law of fluctuation scaling*, **PNAS 112(25):7749–7754 (2015)**
(read at `pmc.ncbi.nlm.nih.gov/articles/PMC4485080/`): drawing blocks of i.i.d. samples from **any**
right-skewed distribution with finite first four moments produces TL with slope `b ≈ γ₁/CV` — skewness over
coefficient of variation — with **no interaction, aggregation or correlation whatsoever**. So a fitted `b`
is evidence of nothing until it is placed beside γ₁/CV of the pooled data.

## Why this is new ground for us

`scripts/mesh-criticality` is 4000+ lines and carries sixteen lenses (m̂/MR, shape, crackling, CECP,
dynamic range, susceptibility, coherent-noise, margin, DFA/Hurst, coarse-graining recovery, dtc, aging,
allometry, separability, widom, sob). **Every one of them reads the POOLED board tape as ONE time series
and asks whether activity PROPAGATES ALONG IT.** Grep over `scripts/`, `docs/` and the 849 files in
`~/.mesh/knowledge/` finds **zero** occurrences of "Taylor's law" or "fluctuation scaling": the
across-units plane has never been read. It is not a variant of the coherent-noise null (that one asks
whether an exogenous common stressor explains the tail, via the Omori aftershock train) and not a variant
of allometry (that one asks how total activity scales with system SIZE, and currently refuses to report
for want of range). It asks a third question: **how does a unit's fluctuation scale with its own rate?**

What it buys, operationally, that m̂ cannot give: m̂ says whether activity propagates. `b` says **how the
board's fluctuation budget scales with load** — `b > 1` means the busier a poster is the clumpier it is, so
peak congestion grows as (mean traffic)^b, superlinearly, as the genome grows (26 → 295 cadence-carrying
reflexes since 2026-06-17); `b ≈ 1` means peaks grow with the mean and a pooled heavy tail is
**superposition of independent sources**, not a shared cascade budget; `b < 1` means a cron-clocked
population that cannot mint a cascade of its own. The mesh already has the population and needs no new
sensor — every board line carries its poster, and `sender_id()` already parses it.

## What shipped — `scripts/mesh-criticality --taylor`

Read-only sidecar, no alarm, no board post, not in `--json` (same shape as `--allometry`/`--separability`).
Bins the window per POSTER, fits `log var` on `log mean` by OLS across posters, and judges:

- `CLOCKED-SUBPOISSON` — b below the null band.
- `FLAT-POISSON` / `FLAT-OVERDISPERSED` / `FLAT-CLOCKED` — b inside the band, split by where the
  **intercept** falls against its own band.
- `CLUMPING-SUPERLINEAR` — b above the band, below `CRIT_TL_PROP` (1.80).
- `PROPORTIONAL-COMMON-MODE` — b ≥ 1.80.
- `INSUFFICIENT` — names what is missing (T, S) and is never a number.

Three design points, each earned:

1. **The band is SIMULATED THROUGH THE SAME ESTIMATOR**, at the same T, the same S, and the same per-unit
   means — never the textbook `b = 1` and never an analytic CI. That is the Truquet/Cohen/Doukhan result
   taken seriously: the board's regime is T/S ≈ 2–7 (measured), exactly `T/S → const`, so the analytic CI
   is not trustworthy. Simulating the null through the same fit makes whatever bias the estimator carries
   apply to data and null alike, where it cancels. Measured side-note, and it is the honest one: at this
   board's T the OLS bias itself is **tiny** — the Poisson null's own median slope is 0.998–1.000. The
   simulation is load-bearing not for the bias but for the **band WIDTH**, which is what turns b = 1.118
   into a verdict instead of an eyeball, and which is invisible without it (at T = 30 the width is 0.138,
   at T = 480 it is 0.042, and at S = 5 units it is [−0.32, 2.63] — a population that small can support
   no verdict at all).
2. **The intercept is judged too.** A population where every unit posts in clumps of a FIXED size has
   `var ≈ K·mean` for every unit: slope 1, dead inside the Poisson band, intercept K. Judged on `b` alone
   the tool would file that board as FLAT-POISSON and call its bursts Poisson noise. Hence
   `FLAT-OVERDISPERSED`.
3. **Cohen & Xu's γ₁/CV is printed on every reading**, with its own verdict field
   (SAMPLING-ARTIFACT-CONSISTENT / FALSIFIED), because a TL slope that merely reproduces the pooled skew
   is not a claim about the mesh.
   `dropped` is printed for the same reason: a unit with zero variance cannot be log-transformed and is
   dropped, and that drop is **not neutral** — a perfectly flat unit is the most CLOCKED one there is, so
   every drop biases b UPWARD, and a fit that hid them could never find CLOCKED-SUBPOISSON. That last
   sentence was, until the drop-bias gate below, only a comment — so it is now ASSERTED, and the
   magnitude is larger than the prose suggested: on a fixture of ten Poisson units plus ten perfectly
   constant ones, the same population fits **b=1.028 when its clocked half is dropped and b=-1.320 when
   a single bin of each is perturbed by +1 so they become fittable**. The drop alone moves the verdict
   from FLAT-POISSON to the far side of CLOCKED-SUBPOISSON. (Asserted at the `_tl_fit` level on purpose:
   the event path cannot build an exactly-flat unit, because the trailing partial bin always adds
   variance — routing this leg through `taylor_fluctuation` would have tested nothing, which is itself
   why the four dispersion fixtures all report `dropped=0` and left the field unexercised.)

## The live reading (mesh-home, 2026-08-18)

```
CLUMPING-SUPERLINEAR  b=1.118  Poisson-null band=[0.988,1.013] med=1.000
S=73 units  T=289 bins  T/S=3.96  dropped=0  events=822
Cohen-Xu sampling b~γ₁/CV=4.84 [skew=35.47 CV=7.33] → SAMPLING-ARTIFACT-FALSIFIED
```

Stable across windows: 12h → b=1.165 (band [0.978,1.016]); 24h → 1.118 ([0.988,1.013]); 48h/600s →
1.093 ([0.993,1.007]). All three sit above their bands, and all three falsify the sampling-artifact
explanation by a wide margin (the pooled counts are skewed enough that pure block-sampling would predict
b ≈ 3.9–5.0; we measure 1.1).

**The caveat, measured rather than assumed.** The excursion above the band is small and it is
**concentrated in a handful of posters**. Per-poster dispersion over 24h/300s: `memory-recall` 23.20,
`mind-state` 2.41, `discover` 2.32, `vpn` 2.23 at the top; `hw-fault-watch` 0.85, `land` 0.89,
`needs@phaedra` 0.91 at the bottom. Refitting without the single clumpiest poster gives b=1.075; without
the top three, b=1.054 — still above the band, but the rank correlation between a poster's rate and its
dispersion is weak (Spearman +0.167 over all 73, falling to +0.077 with the top three removed). So the
honest statement is: **the board is superlinearly clumping, but only just, and the reading is carried by
its burstiest few posters, not by a population-wide trend.** Reported here because the verdict label alone
would over-claim it (`a-sub-axis-is-not-the-verdict`).

## Gates — seen RED, then green

`--test` legs (all inside the existing python `--test` body, fixtures at pinned seeds, no live artifact
touched): four dispersion laws in pure form must give four distinct verdicts (independent Poisson →
FLAT-POISSON; shared multiplicative driver → PROPORTIONAL-COMMON-MODE; fixed-period emission →
CLOCKED-SUBPOISSON; fixed-size clumps → FLAT-OVERDISPERSED **with its slope asserted to be inside the
band**, so the intercept leg cannot pass on a drifted fixture); a 5-unit population must render
INSUFFICIENT naming the unit count; the null band must WIDEN as T shrinks; the Cohen-Xu verdict must not
be constant across fixtures; and `dropped` must COUNT the zero-variance units it discards, with the
discard demonstrably biasing b upward.

Seven mutants run from a scratch copy, each red for its own reason, base green (an eighth — admitting
zero-variance units into `math.log10` — dies loudly with a domain error rather than passing):

| mutant | verdict |
|---|---|
| intercept branch deleted | `FAIL … must be caught by the INTERCEPT band → FLAT-OVERDISPERSED, got FLAT-POISSON` |
| band hardcoded to [0.90,1.10] | `FAIL … band must widen as T shrinks … T=30 width=0.200 vs T=480 width=0.200` |
| label collapsed to a constant | `FAIL … must read CLOCKED-SUBPOISSON, got FLAT-CLOCKED` |
| `S < CRIT_TL_MIN_S` refusal dropped | `FAIL … must be an honest INSUFFICIENT …, got {'label': 'FLAT-POISSON', 'b': 1.68, 'S': 5, 'null_lo': -0.32, 'null_hi': 2.63}` |
| sampling verdict pinned | `FAIL … γ₁/CV sampling verdict is constant across fixtures that differ in b by 1.04` |
| `dropped` returned as a constant 0 | `FAIL (ten zero-variance units must be COUNTED as dropped, not silently discarded: dropped=0 fitted=10 of 20)` |
| zero-variance units admitted with a floor variance instead of dropped | `FAIL (… dropped=0 fitted=20 of 20)` |

`bash scripts/mesh-criticality --test` → `smoke-test: ok` + `alarm-test: ok`, ~1.9s (well inside
autowire's timeout-30 gate). Other modes re-run unchanged (default, `--json`, `--shape`, `--allometry`,
`--separability`).

## Sources

- Truquet, Cohen & Doukhan, *Inferring the parameters of Taylor's power law of fluctuation scaling*,
  Proc. R. Soc. A **481**(2326):20250248 (2025) — https://royalsocietypublishing.org/doi/10.1098/rspa.2025.0248
  (preprint: https://arxiv.org/abs/2408.16023)
- Cohen & Xu, *Random sampling of skewed distributions implies Taylor's power law of fluctuation scaling*,
  PNAS **112**(25):7749–7754 (2015) — https://pmc.ncbi.nlm.nih.gov/articles/PMC4485080/
- Brown, Cohen et al., *Taylor's law of fluctuation scaling for semivariances and higher moments of
  heavy-tailed data*, PNAS **118**(46):e2108031118 (2021) — https://www.pnas.org/doi/10.1073/pnas.2108031118
  (the heavy-tail extension; not implemented here, the obvious next step if the board's tail deepens)

## Discarded on the way (named, so the next review does not re-walk them)

- **arXiv:2605.00207, *Activated random walk exhibits self-organized criticality* (2026)** — the first
  rigorous proof that a model meets the BTW conjecture, and it names slow MIXING as why the abelian
  sandpile is non-universal. Real and recent, but the mesh-side reading (an exponent fit before the
  process has mixed is a function of the initial state) is already covered by the `--aging`
  stationary-vs-aging sidecar.
- **arXiv:2604.15669, *Self-Organization to the Edge of Ergodicity Breaking* (Apr 2026)** — ergodicity
  breaking is already twice-reviewed here (`ergodicity-breaking-pooled-corpus-2026-07-24`,
  `review-non-ergodicity-ruin-repeated-shed-2026-06-21`).
- **arXiv:2411.10608 / EPL 149:31001 (2025), *Inter-Event Time Power Laws in Heterogeneous Systems*** —
  heterogeneity rather than memory as the source of an IET power law; overlaps the existing
  `--coherent` (Newman–Sneppen heterogeneous-threshold) null.
- **arXiv:2608.13500, *Symmetry Emergence in Self-Organized Criticality* (13 Aug 2026)** — the freshest
  result found, and genuinely new mathematics (the scaling limit of the toppling function solving an
  optimal-transport PDE), but its mesh transfer requires POKING the board to measure a response shape,
  and this lane is read-only.
