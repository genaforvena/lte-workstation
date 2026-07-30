# CAS / edge of chaos — the bin-width (Δt) artifact, a failure mode we committed by construction

**Live review, genome, 2026-07-27.** Area: complex adaptive systems & the edge of chaos (Santa Fe).
Angle: a **known critique / failure mode** of this area — and one `mesh-criticality` was itself
committing.

## The critique

The criticality / edge-of-chaos programme is dogged by a standing critique: its signatures
(power-law avalanche distributions, branching ratio ≈ 1) are often **artifacts of the analysis
procedure**, not evidence of a real critical point. Touboul & Destexhe showed *two non-critical
systems pass all the standard criticality tests*; the lack of a single univocal test is a core
methodological weakness ([*Is there sufficient evidence for criticality in cortical systems?*, eNeuro
2021, ENEURO.0551-20.2021](https://www.eneuro.org/content/8/2/ENEURO.0551-20.2021);
[arXiv:2002.08813](https://arxiv.org/pdf/2002.08813)).

The **most basic, best-documented instance** of that failure mode is **time-bin-width (Δt)
dependence**. Avalanches are defined by concatenating events that fall within a bin Δt, so:

- **too-small Δt** splits one cascade into fragments → a **subcritical-looking** bias;
- **too-large Δt** *glues* successive cascades together → a **supercritical / large-avalanche** bias;
- the fitted size exponent **τ drifts monotonically with Δt**.

The field's fix is not a fixed bin — it is to set **Δt = the mean inter-event interval ⟨IEI⟩** of the
data. Only then does a critical branching process yield its unbiased exponents (τ≈1.5, τt≈2, γ≈2)
— the very convention Beggs & Plenz used (J. Neurosci. 2003, the paper `mesh-criticality` already
cites for τ≈−3/2). Sampling/overlap deepens it: [Levina & Priesemann, *Sampling effects and
measurement overlap can bias the inference of neuronal avalanches*, arXiv:1910.09984](https://arxiv.org/pdf/1910.09984).

## Why it applies to us — a fixed "sweet spot" is the artifact, not the cure

`mesh-criticality` discretizes board events into a **fixed** bin, `CRIT_BIN_S=300s`, and its own
header enshrined it as *"the validated sweet spot."* Its lineage is vast — slope-vs-shape (Touboul),
dragon-kings, micro-macro, CSN power-law goodness-of-fit, subsampling (via the MR estimator) — but it
**never checked whether that Δt is anywhere near ⟨IEI⟩.** And ⟨IEI⟩ on this board is *not stationary*:
it swings by orders of magnitude between a quiet night (minutes) and an incident storm (seconds). So a
single fixed 300s bin is **GLUING during exactly the floods the alarm exists to catch** (the
37-`[evaporated]`-in-one-bin false-supercritical incident is that gluing artifact in miniature) and
**FRAGMENTING during a quiet drift**. The ⟨IEI⟩ was even already computed for the `--complexity` axis
— just never compared to the bin.

## Concrete application (landed)

**File: `scripts/mesh-criticality`** — added a read-only **`bin_sanity()`** reading, additive and
non-breaking (never touches m̂, the regime, or the SUPERCRITICAL alarm — same restraint as the CSD /
Shape / Crackling / CECP sidecars):

- Computes the live **⟨IEI⟩** over the window and the ratio **Δt/⟨IEI⟩**, labelled **CALIBRATED**
  (ratio ∈ `[CRIT_BIN_LO,CRIT_BIN_HI]`=`[0.5,2]`) / **GLUING** (Δt≫⟨IEI⟩ → avalanche stats biased
  large) / **FRAGMENTING** (Δt≪⟨IEI⟩ → biased small) / **INSUFFICIENT**.
- Emitted on the default line (`Bin=… Δt=…s ⟨IEI⟩=…s ratio=…`) and in `--json` (`bin_sanity`). It is
  an **honesty flag on every avalanche-derived axis** (Shape, Crackling, the rejected `--powerlaw`):
  when `Bin≠CALIBRATED`, those axes are in the biased regime and must be read with that caveat. The
  m̂ point estimate (MR, subsampling-robust) is the sturdier number; the guard says *when* the softer
  avalanche axes are trustworthy.
- `--test` gains a **RED-first falsifier**: synthetic streams at three densities against the fixed
  300s bin must read GLUING / CALIBRATED / FRAGMENTING respectively (and n<3 → INSUFFICIENT); if the
  label ever collapses to a constant the test fails. **PASS.**

Live at landing: `Bin=CALIBRATED Δt=300s ⟨IEI⟩=205s ratio=1.46` — right now the fixed bin sits near
⟨IEI⟩, but the guard now surfaces that *per window* instead of trusting the static sweet spot.
(Corroboration from the tool's own chorus: `CECP=MEMORYLESS-POISSON-LIKE H=1.00 C=0.00` — the timing
looks memoryless, so today's `m̂=0.91 CRITICAL` is, by the tool's own caveat, plausibly a coincidence.)

**Left unwired (honest scope):** an ⟨IEI⟩-**adaptive** bin is the natural next step, deliberately not
taken — changing Δt moves m̂ and the alarm, so it needs its own vetting against the real m̂ series,
the same bar every other proposal in this header holds to.
