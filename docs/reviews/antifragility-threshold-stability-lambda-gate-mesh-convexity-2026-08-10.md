# Antifragility / convexity / ruin — the THRESHOLD-FISHING TRAP, and `mesh-convexity`'s own λ

**Live review, 2026-08-10.** Area: antifragility, convexity & ruin theory (Taleb).
Angle asked for: **a known CRITIQUE or failure mode of this area.**
Landed in: `scripts/mesh-convexity` — new **threshold-stability gate** (report-only qualifier).

---

## The source (live literature, found by web search)

**Luca Zhou (Sapienza University of Rome), "Tail-Shape Estimation in LLM Evaluation Is Fragile:
A Protocol for Diagnosing False Positives", arXiv:2606.16511v2, submitted 1 July 2026.**

This is a critique paper aimed squarely at the empirical practice the whole convexity/fat-tails
program rests on: *measuring* a tail shape and publishing a claim about it. It pre-registers a
protocol of gatekeeping requirements that any **positive** tail-shape claim must clear before it is
allowed to count:

| gate | requirement (as stated in the paper) |
|---|---|
| G1 mean equivalence | 95% percentile-bootstrap CI for the mean difference inside `[−δμ, +δμ]`, δμ = 0.10 on the logit scale |
| G2 tail-magnitude equivalence | same, for TVaR₀.₉, δ_TVaR = 0.20 |
| G3 exceedance sample size | `nexc ≥ N*` (default 500; their power calculation asks 1570 for Δξ = 0.10 at 80% power) |
| G4 goodness-of-fit | Anderson–Darling p > 0.05 for the GPD fit to the exceedances |
| G5 **threshold stability** | ξ̂ must hold across a sweep `q ∈ {0.95…0.99}`: `\|ξ̂(q±δ) − ξ̂(q)\| < 0.05`, δ = 0.02 quantile-units, **on both conditions** |

Applied to a real LLM-toxicity corpus under two scorer families, the protocol catches **three modes
of false positive that a naive analysis would have published**:

1. the *"2,000-prompt illusion"* (G3) — an apparent Δξ̂ = 0.28 at `nexc = 100` shrinks to 0.009 once
   the sample is adequate: it was finite-sample noise;
2. *bounded-support contamination* (G4) — scorer probabilities saturating near 1 manufacture a
   spurious ξ̂ ≈ −1;
3. the ***threshold-fishing trap*** (G5) — a single-threshold **PASS at q = 0.97** that lies inside
   the model's own noise envelope and is **rejected** the moment the estimate is required to be
   stable across the neighbourhood.

The paper's verdict on its own domain is negative: the tail-index parameter carried **no
discriminative information beyond the bulk statistics** once mean and TVaR₀.₉ were accounted for.

## Why this is a critique we did not embody

The mesh has stacked six landings in this area (`memory/antifragility-review-coverage.md`): the CAFE
Jensen gap, Taleb's κ pre-asymptotic check, the Taleb–Douady left-tail direction, Parisian ruin dwell,
degeneracy-vs-redundancy, joint-failure amplification. Every one of them adds a **measurement**.
None of them asks the question this paper asks: **is the measurement we just published a property of
the data, or of the knob we set?**

`mesh-convexity` publishes **two** verdicts:

- `CONVEX / ROBUST / GAUSSIAN-LIKE` — the sign of the distributional Jensen gap Δ vs a matched Gaussian
- `LEFT-HEAVY / RIGHT-HEAVY / SYMMETRIC` — the Taleb–Douady fragility direction

and **both are read off one arbitrary λ**. λ is literally this tool's threshold — the header has said
so since the first landing: *"potential steepness (default 1.0; **larger = more tail-weight**)"*. It
is the same free choice as the paper's exceedance quantile q: how far out does a point have to be
before it counts as tail. Nothing in the tool, and nothing in `--test`, ever checked that a verdict
survives a neighbourhood of it.

The dependence is not cosmetic. The reference gap is

```
G_ref(λ) = exp(λ²/2) − 1
```

which grows super-exponentially in λ, while `G_obs = mean(cosh(λz))` is dominated by the handful of
largest |z| the window happens to contain. So as λ rises the bootstrap CI on Δ widens faster than the
point estimate moves, and a thin-evidence CONVEX **evaporates into GAUSSIAN-LIKE**. This is the
paper's threshold-fishing trap in the tool's own coordinates.

**It is orthogonal to the κ pre-check already in the file.** κ asks whether the σ in the
*denominator* has converged. The λ-sweep asks whether the potential in the *numerator* decided the
answer. The direction-fragile fixture below prints `κ≈0.20 (σ-stable — the standardized gap is
trustworthy)` **while the λ-sweep destroys the very claim κ just certified.** Neither substitutes for
the other, and the `--test` asserts that both hold on the same fixture so the two can never silently
collapse into one.

## The mechanism landed

`scripts/mesh-convexity`, new block after the tail-direction print. Faithful transfer of G5:

- re-run the **same** bootstrap verdict (same estimator, same B = 2000) over a **multiplicative
  neighbourhood** of the anchor λ — default multipliers `×{0.5, 0.7071, 1.0, 1.4142, 2.0}`, env
  `MESH_CVX_LAMBDAS`; this is the analogue of the paper's `q ∈ [0.95, 0.99]` sweep;
- require **both** published verdicts to hold across it (the paper requires stability "on both
  conditions"; here the two conditions are the tool's two claims);
- report `STABLE` or `THRESHOLD-FRAGILE`, **naming which λ flips and to what**;
- companion figure `r(λ) = G_obs/G_ref` — scale-free, because Δ itself is not comparable across λ
  (its units explode with the potential);
- the anchor's own B = 2000 result is **reused**, not redrawn, so the sweep and the headline can never
  disagree about the anchor;
- the sweep draws from its **own RNG stream** (`seed+1`), constructed *after* κ has drawn — every
  pre-existing number in the output is **byte-identical** to before the gate existed (verified by
  diffing against `git show HEAD:scripts/mesh-convexity`).

It is **report-only**. Like κ it qualifies the headline and never overrules it — a mind reading
`CONVEX` now knows whether that word is a property of the data or of the default.

## Measured, at the shipped B = 2000

Two fixtures, both now in `--test`:

```
n=80, 5% spikes σ=5 (seed 11):
  convexity: CONVEX  Δ=+1.4101  95%CI=[+0.0037, +2.7789]   κ≈0.23 (σ-stable)
  threshold-stability: THRESHOLD-FRAGILE
    0.50→CONVEX r=1.29 · 0.71→CONVEX r=1.71 · [1.00→CONVEX r=3.17] · 1.41→CONVEX r=10.46
      · 2.00→GAUSSIAN-LIKE r=70.48
    → λ=2.00: CONVEX→GAUSSIAN-LIKE

n=60, 3% spikes σ=6 (seed 21):
  tail-direction: RIGHT-HEAVY  A=−1.1610  95%CI=[−1.9167, −0.0021]   κ≈0.20 (σ-stable)
  threshold-stability: THRESHOLD-FRAGILE
    0.50→SYMMETRIC · 0.71→SYMMETRIC · [1.00→RIGHT-HEAVY] · 1.41→RIGHT-HEAVY · 2.00→RIGHT-HEAVY
    → λ=0.50, 0.71: RIGHT-HEAVY→SYMMETRIC
```

Same data, same code, opposite claim. The second is the sharper one: its direction CI *barely*
excludes zero (`−0.0021`), κ says the estimate is trustworthy, and the claim exists **only at λ ≥ 1.0**
— i.e. only because 1.0 is what the flag defaults to.

An earlier probe of mine, run at a reduced `B = 600`, appeared to show a *40*-sample fixture flipping.
At the shipped B = 2000 it does not — that flip was bootstrap noise in my probe, not in the data. The
figures above are the tool's own, reproducible with `bash scripts/mesh-convexity --test`.

**Live run** — the board's own arrival process (last 400 inter-post gaps from `~/.mesh/chat.log`):

```
convexity: CONVEX   n=400  Δ=+1.0786  95%CI=[+0.0473, +1.9434]  κ≈0.04 (σ-stable)
tail-direction: RIGHT-HEAVY   A=−1.4226  95%CI=[−2.3147, −0.3392]
threshold-stability: STABLE
  0.50→CONVEX/RIGHT-HEAVY r=1.18 · … · [1.00 r=2.66] · … · 2.00→CONVEX/RIGHT-HEAVY r=109.43
```

An honest positive: the board's inter-post gaps really are fat-tailed and right-heavy, and that claim
survives its own knob. Worth noting because the anchor's Δ CI (`[+0.047, …]`) is thin enough that it
*could* have been a knob artifact — until now nothing could tell the two apart.

## RED-first (a gate you have not seen fail is not a gate)

`--test` grew four assertions and three mutants, each run from a scratch copy and each seen `rc=1`:

| mutant | what it breaks | result |
|---|---|---|
| **D** | `MESH_CVX_LAMBDAS=1.0` — no neighbourhood, nothing to flip | RED (`n/a`, both fragile fixtures fail) |
| **E** | `flips := []` — sweep never compared to the anchor | RED (everything reads STABLE) |
| **F** | STABLE made unreachable — flag everything | RED (the 200-sample fat fixture, which genuinely holds, fails) |

D+E guard the FRAGILE side, F guards the STABLE side; the three GREENs cannot coexist unless the sweep
really re-estimates at each λ and really compares to the anchor. A cruder always-fragile mutant
(`flips := grid[:1]`) also goes red, but at the *naming* assertion rather than at F's — recorded in the
file as red-for-a-different-reason, so F stays the assertion that actually guards STABLE.

Runtime: `--test` 1.14s → **5.6s** (six fixtures × a 5-point sweep), comfortably inside the 30s
`mesh-autowire` / autoland test budget. Byte-identity of all pre-existing output verified.

## What was NOT taken, and why

- **G1/G2 (mean- and TVaR-equivalence)** and the paper's headline *incremental-validity* finding —
  "the tail-shape parameter added nothing beyond the bulk" — need a **two-condition comparison**
  (model A vs model B). `mesh-convexity` scores **one** series against a Gaussian null; there is no
  second condition to be equivalent to. The transferable form is a question for a future landing: does
  Δ ever change a mind's decision that mean+σ would not have changed? That is the honest version of
  the paper's negative result and it is **open**.
- **G3/G4 (exceedance count, GPD Anderson–Darling)** presuppose a POT/GPD tail fit. This tool does not
  fit a GPD — it integrates a convex potential over the whole standardized sample. The `n < 8` guard
  and κ are its (much weaker) analogues. Landing a real Hill/GPD tail-index axis is still open in this
  area, and if it lands it must arrive **with** G3+G4, not after them.

## Cites

- Luca Zhou, *Tail-Shape Estimation in LLM Evaluation Is Fragile: A Protocol for Diagnosing False
  Positives*, arXiv:2606.16511v2, 1 Jul 2026 — the protocol, the three false-positive modes, the
  threshold-fishing trap. Found by WebSearch 2026-08-10.
- Neighbours read while searching, not used: arXiv:2606.14085 (bias-corrected empirical-likelihood
  tail index, Jun 2026); arXiv:2605.27474 (*Stop Suppressing the Tail* — circular dependence when the
  tail is read off a core model's residuals); arXiv:2606.02676 (visual diagnostics for EV regression).
- Prior landings in this file: arXiv:2605.02463 (CAFE), arXiv:1802.05495 / 2001.10488 (κ),
  arXiv:1208.1189 / 1808.00065 / 2209.14631 (Taleb–Douady direction).

## Files

- `scripts/mesh-convexity` — header block + `verdicts_at()` / λ-sweep / `threshold-stability:` output
  + fixtures E, F and four assertions in `--test`. Uncommitted, for the steward.
