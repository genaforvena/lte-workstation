# VSM live review — Beer's CyberFilter: the algedonic channel had no SLOPE hypothesis

**Area:** viable system model & management cybernetics (Stafford Beer)
**Angle:** an OPERATIONAL mechanism, not philosophy — specifically the one piece of Beer's apparatus that
was *running software* rather than a diagram
**Date:** 2026-08-18 · genome mind · live web review
**Landed:** `scripts/mesh-algedonic` — `cyberfilter()`, config block `CF_*`, six new fields on the report
line, `--cyberfilter` detail mode, 16 new `--test` legs. Read-only/advisory, nothing escalates.

---

## Why this lane needed a new place to stand

Eleven prior `vsm-*` reviews sit in `docs/reviews/` (ACP indices, System 2 anti-oscillation, System 3*
audit, the S3–S4 homeostat, residual variety, PII-2, power relations, error-budget autonomy, critic
weighting, social confidence, completing deficiencies). The organ this one lands in — `mesh-algedonic` —
is already the most instrumented tool in the genome: noisy-OR fusion plus **four** temporal sidecars
(`allostatic=` level, `csd=` variance+autocorrelation, `salience=` deviation-vs-baseline, `anticipate=`
peri-onset phase), a Mahalanobis joint read, a constrained-disorder read, and four information-theoretic
agency reads. Finding an unoccupied mechanism here required going at Beer from the *software* side rather
than the model side.

## The mechanism, and where it was found

**CyberStride's CyberFilter** — the statistical component of the software Beer's team ran on the Chilean
telex net, 1971–73.

> "CyberStride was the software suite developed by the teams around Stafford Beer that was running on the
> mainframe computer. One component of it was CyberFilter, a set of statistical tools for time series
> analysis… They used Bayesian Statistics for short-time forecasting of the key economic indicators… In
> case of alarming deviations, they would send feedback via the Telex machine back to the company,
> fulfilling the role of System Three in the VSM (algedonic feedback)."
> — Transform Social, *CyberSyn — An Ambitious Project of Socialist Economics*,
> <https://transform-social.org/en/texts/cybersyn/> (fetched 2026-08-18)

The specific method, from a live search across the Cybersyn sources (P2P Foundation wiki, Metaphorum,
Transform Social — the attribution to Harrison & Stevens is consistent across them, though the
Transform Social page above names only "Bayesian Statistics"): CyberFilter used the **Harrison–Stevens**
Bayesian short-term forecasting model, which **"calculates the probability of chance variation,
transient, changes of slope or step changes"** for each index, and only some of those outcomes were worth
an algedonic signal.

Primary literature for the method itself:

- P. J. Harrison & C. F. Stevens, **"A Bayesian Approach to Short-Term Forecasting"**, *Operational
  Research Quarterly* 22(4):341–362 (1971).
- P. J. Harrison & C. F. Stevens, **"Bayesian Forecasting" (with Discussion)**, *JRSS Series B*
  38(3):205–247 (1976), doi:10.1111/j.2517-6161.1976.tb01586.x —
  <https://academic.oup.com/jrsssb/article/38/3/205/7027485>. This is where the **multi-process** models
  are set out: class I (one model, uncertain parameters), class II (**uncertainty over the model class
  itself**, carried as posterior probabilities across a discrete set of candidates). Class II is the
  construction CyberFilter used.
- Eden Medina, *Cybernetic Revolutionaries* (MIT Press, 2011) — the historical account of Cyberstride.

Also surfaced and **not** used, with the one-line reason each:

- **CASE Framework**, arXiv:2608.10153 — already landed here on 2026-08-12
  (`vsm-error-budget-autonomy-modulation-vitality`); not new ground.
- **"Governing the Recovery of Stalled Systems-of-Systems: ADAPT"**, *Systems* 14(8):959 (Aug 2026),
  doi:10.3390/systems14080959 — genuinely fresh and genuinely operational (Anchor/Dependency/Allocation/
  Production/Traceability, with computable measures: trace completeness, branchlessness, critical-path
  depth, change blast radius). **Discarded for this pass, not on merit:** MDPI returned 403 to fetch, so
  only the abstract-level summary was readable, and landing a five-stage governance methodology off an
  abstract would be exactly the paraphrase-with-no-source failure. Worth a dedicated pass — the mesh has a
  live instance of its subject (the 6-day autoland jam,
  `a-revert-that-does-not-repair-proves-the-commit-innocent`).
- **Keating et al., "Integrated Risk and Resilience for Complex System Governance — Renewing the Value of
  Algedonic Signal Warnings"** (2025) — about *formalising weak signals into* algedonic alerts; the mesh's
  gap is downstream of that, in what the alert is computed FROM.

## What the mesh did not have — measured, not asserted

Beer's four hypotheses map onto four generative regimes for a monitored index. The mesh's algedonic
channel carried readings of the pain series' **level**, its **second moment**, its **deviation from a
trailing baseline**, and its **phase around a step onset** — but nothing that asks *which regime the
series is in*. The consequence is not a tuning problem. It is structural, and one fixture exposes it.

A **monotone ramp** of the fused pain from 0.100 to 0.580 over 48 samples — a 5.8× climb covering half the
distance from NOMINAL to CRITICAL — driven through the tool's own sidecar functions:

| sidecar | reading on the ramp | verdict |
|---|---|---|
| `band` | `WATCH` | calm |
| `allostatic_load` | `LOAD_WATCH 0.345 0 49` (0 high samples) | calm |
| `viability_csd` | `CSD_STABLE −0.0001 0.0075 48` | calm |
| `salience` | `SAL_CALM 1.321 0.340 48` (bar is z ≥ 3.0) | calm |
| `anticipation_index` | `ANT_UNKNOWN … 0 onsets` | cannot speak |

Five temporal readings, all calm, on the series doing the single most obviously fatal thing a viability
index can do. The two reasons are worth stating because they are not fixable by moving a threshold:

- **A ramp drags its own baseline.** `salience` measures deviation from the trailing median of the same
  window; on a ramp the median rises with the value, so the robust z is pinned around 1.3 forever.
- **A linear trend has equal variance in both halves.** `viability_csd` splits the window and compares
  variance and lag-1 AC between halves; a straight line gives `vtr = −0.0001`.
- And `anticipation_index` needs an onset — a ≥0.10 **step out of quiet**. A ramp, by construction, never
  produces one, so the phase read is permanently `ANT_UNKNOWN` on exactly the series it would matter for.

The SLOPE class was **absent** from this organ, not weakly covered.

## What landed

`cyberfilter()` in `scripts/mesh-algedonic` — a Harrison–Stevens multi-process class II filter over the
last `CF_N=48` pain samples. Four model classes compete:

| class | form | k |
|---|---|---|
| `STEADY` | y = μ | 1 |
| `SLOPE` | y = a + b·t | 2 |
| `STEP` | y = μ₁ (t<τ), μ₂ (t≥τ), τ scanned | 3 |
| `TRANSIENT` | y = μ with one free point, scanned | 3 |

`BIC_i = n_eff·ln(RSS_i/n) + k_i·ln(n_eff)`; posterior weights `w_i ∝ exp(−BIC_i/2)`, normalised.

**Three design choices that are the whole difference between this and a threshold:**

1. **AR(1) deflation of the effective sample size.** The pain series is autocorrelated and a plain BIC on
   it is anticonservative — a smooth wander buys SLOPE/STEP evidence it has not earned. `n_eff =
   n(1−φ)/(1+φ)`, φ the lag-1 AC of the **best-fitting** model's residuals (one `n_eff` for all four
   classes — giving each model its own would *reward* whichever leaves the most autocorrelated residual).
   Because `BIC_i − BIC_j = n_eff·(ln RSS_i − ln RSS_j) + (k_i − k_j)·ln(n_eff)`, deflating shrinks the fit
   difference **linearly** and the complexity penalty only **logarithmically** — the deflation can only
   ever make the richer class harder to call.
2. **A magnitude gate that is published, not hidden.** Evidence is not importance: a 0.0006/sample drift is
   statistically clean and operationally nothing. A winner whose fitted excursion is below
   `CF_MIN_RISE=0.10` is demoted to `CF_STEADY` — but the **ungated** evidence winner is emitted in its own
   field `cfwin=`, so a demotion reads as a demotion and never as "the filter saw nothing".
3. **The changepoint edge guard.** A spike on the newest sample is geometrically *also* a step with
   τ = n−1. `CF_EDGE=4` refuses changepoints that close to either end, which is the only reason STEP and
   TRANSIENT are separable at all.

Honest n/a throughout: `CF_INSUFFICIENT` under `CF_MIN_N=16` samples, `CF_FLAT` when the window's whole
spread is under `CF_FLOOR=0.02` (fitting a regime to a dead-flat series manufactures a slope out of float
noise), `CF_UNKNOWN` on UNKNOWN pain. Never an interpolated regime.

**Report-line fields** (appended before `axes=`, so every existing key-based reader is untouched;
`mesh-dnb` and `mesh-precision` are the only other consumers of this log and both parse by key):

```
cyberfilter=CF_STEADY cfw=0.655 cfwin=STEADY cfslope=+0.0003 cfeta=na cfn=48
```

`cfeta` is **samples** to the next band edge above the current pain, published only for a rising slope —
an ETA on a recovering series is a fabricated deadline. `cfslope` is pain **per sample**. Both are index
time, not wall time: the log carries no reliable per-row cadence (cron skips, reboots), so a consumer
wanting minutes must multiply by its own known cadence, and is told so in `--cyberfilter` rather than left
to assume.

## Verification

`bash scripts/mesh-algedonic --test` → green. Nine discrimination fixtures:

| fixture | label | cfwin | slope | eta |
|---|---|---|---|---|
| monotone ramp | `CF_SLOPE_UP` | SLOPE | +0.0104 | 2 |
| falling ramp | `CF_SLOPE_DOWN` | SLOPE | −0.0104 | na |
| step 0.20→0.60 | `CF_STEP_UP` | STEP | — | na |
| interior spike | `CF_TRANSIENT` | TRANSIENT | — | na |
| **newest-sample** spike | `CF_TRANSIENT` | TRANSIENT | — | na |
| white noise | `CF_STEADY` (w=0.637) | STEADY | — | na |
| dead flat | `CF_FLAT` | NA | — | na |
| 0.03 sub-threshold drift | `CF_STEADY` | **SLOPE** | +0.0006 | na |
| 6-sample log | `CF_INSUFFICIENT` | NA | — | na |

Plus three legs asserting **the gap itself**: on the *same* ramp fixture, `viability_csd` must still read
`CSD_STABLE`, `salience` must still read `SAL_CALM`, and `anticipation_index` must stay below its onset
floor. If a future edit makes one of them see a ramp, the suite goes red and this block's justification
has to be re-derived rather than silently inherited.

**Mutation-tested, 10 mutants, 9 red:** CF_EDGE guard removed · SLOPE magnitude gate neutered · STEP
magnitude gate made impossible · CF_FLOOR flat guard removed · min-sample n/a removed · slope direction not
named · eta published for a falling slope · AR(1) deflation removed (`n_eff = n`) · posterior weight faked
as 1.0.

**Surviving and kept, named not dropped:** taking φ from the STEADY residuals instead of the best-fitting
model's. It survives because it can only make the filter **more** conservative — a trend-contaminated φ
reads high, collapses `n_eff` to its floor, flattens the weights, and so suppresses verdicts rather than
fabricating them. No fixture in this suite is marginal enough to be suppressed by it. That is a gap in the
fixtures, not a claim that the choice does not matter.

## Honest limits

**A driftless random walk is not a trendless series in the sense this filter tests.** Over 6 seeded walks
(sd 0.03/step, n=48, no drift), **5 still receive a SLOPE/STEP label**. What the deflation changes is the
weight beside it — e.g. 0.960 → 0.378 on one seed, and on another it flips the winner STEP → SLOPE. So
`cfw=` is not decoration: a consumer that reads the label and ignores the weight will be fooled by a walk.
This is stated in the tool's own `--cyberfilter` output and header, not only here.

**Nothing escalates.** `mesh-algedonic` is read-only by design and this block keeps that. The value of a
`CF_SLOPE_UP` with an eta is that it is now *computable and logged* — the escalation threshold has to be
calibrated against this node's real pain baseline first, which is exactly what the read-only logger exists
to accrue.

## The live reading right now

```
pain=0.575 cyberfilter=CF_STEADY cfw=0.655 cfwin=STEADY cfslope=+0.0003 cfeta=na cfn=48
axes=therm:0.0,hw:0.0,egress:0.0,stress:0.5,crit:0.15 known=5/5
```

Not a catch — and said plainly rather than dressed up. The live series is genuinely near-flat at an
elevated level (0.500–0.575 over the last 48 samples), which is also what `salience` says
(`SAL_HABITUATED`). The filter agrees with the existing sidecars on the live tape and diverges only on the
regime none of them can see. That is the correct behaviour for a new axis on its first day.

**Incidental, and it cost a wrong number:** the first live probe read `pain=0.300` because
`~/.mesh/algedonic.log` contains NUL bytes and plain `grep -o` answered *"binary file matches"* instead of
the last row — a live re-instance of `one-nul-blinds-plain-grep`. The tool's own reader opens the file
with `errors="replace"` and was never affected; the probe around it was. Any ad-hoc read of a mesh log
needs `grep -a`.

## Not landed

No consumer, no dash field, no escalation, no cron change — `mesh-algedonic` already runs `*/10` and the
new fields ride its existing line. Wiring `CF_SLOPE_UP` to anything that acts is a separate decision that
needs the operator, because it is the first thing in this organ that would fire on a series that has not
crossed any threshold at all.
