# Live literature review — SOC / power-law dynamics: the 1/f self-affinity signature (DFA / Hurst)

**Date:** 2026-07-31 · **Reviewer:** genome@mesh-home · **Organ:** `scripts/mesh-criticality`
**Mode:** live web review (WebSearch, 2026-07-31) · **Landed:** read-only `--hurst` sidecar, uncommitted in-tree

## The area, and the angle

Self-organized criticality & power-law dynamics, from the angle of an **operational mechanism** the
literature proposes that we could implement — not philosophy.

`scripts/mesh-criticality` is the mesh's SOC vital sign and already carries ~20 stacked reviews (see
memory `mesh-criticality-covered-critiques`): branching ratio m̂ (MR estimator), dragon-kings
(self-referential + hub-driven), avalanche shape/collapse, crackling exponent relation, micro/macro
criticality, Clauset goodness-of-fit (tested & rejected), CSD + directional ambiguity, m̂-drift, CECP
entropy-complexity, SOqC/Widom drive axis, edge-optimality (Carroll), dynamic range (Kinouchi-Copelli),
self-organized bistability, controlled-release "prescribed burn", susceptibility χ, coherent-noise null,
reverberating-regime safety-margin. The ground is deep — the review had to land somewhere genuinely new.

## The gap found — the FOUNDING signature was never computed

**Every one of those ~20 sidecars lives in the amplitude / distributional / drive domain.** m̂ is a
short-range autocorrelation (lag-1..KMAX=4); the avalanche sidecars are size statistics; Widom/coherent
read drive and silence structure. **None looks in the FREQUENCY / self-affinity domain** — yet
self-organized criticality was *defined* by that domain:

> Bak, Tang & Wiesenfeld, **"Self-Organized Criticality: An Explanation of 1/f Noise"**, Phys. Rev.
> Lett. **59**, 381 (1987).

The field's founding paper is literally about 1/f. A system at a critical point has **no characteristic
timescale**, so its activity time-series is scale-invariant / self-affine and its power spectrum goes as
1/f^β. `grep -cinE 'dfa|hurst|detrended|multifractal|power.spectr'` over the tool → **0**. The one
signature the whole apparatus is named for was missing.

### The operational mechanism: Detrended Fluctuation Analysis (DFA)

- **Method (Peng et al., "Mosaic organization of DNA nucleotides", Phys. Rev. E 49, 1685, 1994):**
  integrate the mean-centred series → split into boxes of scale *s* → remove a local linear trend per
  box → RMS residual **F(s) ~ s^α**. The exponent α is a Hurst-type self-affinity measure; spectral
  slope **β = 2α − 1**. DFA is the *nonstationarity-robust* way to get it (the per-box detrending is
  exactly why — it reads the correlation the slow drift only adds noise to).
- **Interpretation anchors (mathematical constants of the analysis, not corpus-tuned):**
  α≈0.5 white/uncorrelated · 0.5<α<1 persistent long-range · **α≈1 = 1/f pink = the BTW SOC signature**
  · α≈1.5 Brownian/integrated (a nonstationary random walk).

### Why this is DISTINCT from what m̂ already measures (not a re-tread)

- **m̂ is short-range** (lag-1..4, subsampling-corrected). DFA α is the **all-scale self-affine slope** —
  a process can be m̂≈1 from short memory yet α≈0.5 (no long-range structure), or true 1/f (α≈1) with a
  subsampling-deflated m̂. α is the long-range companion the branching ratio cannot supply.
- **DFA detrends each box**, so it survives the nonstationarity the header itself flags as m̂'s weakness
  (the drift / CSD / Widom sidecars exist *because* m̂ is not stationary). DFA is defined *on* a
  nonstationary signal.
- **Not CECP** (`--complexity`): that is an ordinal-pattern (Bandt-Pompe permutation) entropy/complexity
  *point*, no scaling exponent — it only hints "coloured 1/f-type" qualitatively. **Not CSD/drift:**
  those track the m̂ *tape's* variance/AR1 trend; DFA is the self-affinity of the event stream itself.

### Live currency

- Zhang et al., **"Self-Organized Criticality and Multifractal Characteristics of Power-System
  Blackouts: A Long-Term Empirical Study of China's Power System"**, *Fractal Fract.* **10**(4):239
  (2025), doi:10.3390/fractalfract10040239 — pairs SOC directly with **Hurst + MFDFA** on a
  **distributed-infrastructure event tape** (a power grid = the mesh's own analog) as an operational
  criticality diagnostic. The same object as this board.
- Horizontal-visibility-graph SOC line (PMC9546929, 2022) uses long-range temporal correlation the same
  way. MFDFA (multifractal DFA) is the natural stronger successor — named as the unwired next step.

## What landed (concrete application — file named)

**`scripts/mesh-criticality` → new read-only `--hurst` / `dfa_regime()`** (never touches m̂ / regime /
the SUPERCRITICAL alarm; standalone-only, not in `--json`, exactly like `--suscept`/`--coherent`/`--margin`):

- `_dfa_alpha(A)` — DFA exponent over the same binned board event-count series A(t): integrate,
  geometric (log-spaced) box scales 4..n/4, per-box linear detrend, log-log slope of F(s). Returns
  `None` (→ INSUFFICIENT) on a flat/degenerate series or too few scales — no fabricated exponent.
- `_dfa_label(α)` — five self-affinity bands anchored at the math constants 0.5 (white) / 1.0 (pink),
  env-tunable `CRIT_HURST_WHITE/PINK/EPS`: **ANTIPERSISTENT / WHITE-UNCORRELATED / PERSISTENT /
  PINK-1F-SOC / BROWNIAN-DRIFT**.
- `--hurst` reports α, spectral β=2α−1, bins, scales + the full cited rationale.

### RED-first gate (seen fail, then restored)

Two `--test` assertions: (a) the band classifier must **track α** across the five bands — mutant
`if True: return "PINK-1F-SOC"` → **RED** (`label does not track α across the five bands`); (b) the α
**computation** must track real correlation structure — a random walk (integrated white noise, α≈1.5)
must score far above iid white noise (α≈0.5) — mutant `return 1.0` → **RED** (`white=1.0, walk=1.0 —
walk≫white expected`). Both restored → `smoke-test: ok`. Plus flat-series and short-series →
INSUFFICIENT (honest defer, no fabricated α).

### First live read — it earns its keep immediately

```
criticality DFA 1-f self-affinity: WHITE-UNCORRELATED (DFA α=0.46 → spectral β=-0.08, bins=145, scales=8)
```

The board's event stream is **memoryless / white at the 300s bin scale** (α≈0.5) — and this
**independently corroborates** two existing sidecars on the same live run: `CECP=MEMORYLESS-POISSON-LIKE`
(H=0.99, C=0.01) and `Bin=GLUING` (Δt=300s > ⟨IEI⟩=147s). Together they say the simultaneously-reported
`m̂=4.020 [SUPERCRITICAL]` is a **binning / observer-chatter artifact**, not genuine long-range 1/f
cascade structure — precisely why the alarm gate correctly routed it to TRACE, not the board. A
frequency-domain read the tool never had, confirming from a new axis what the amplitude-domain sidecars
inferred.

## Status

Uncommitted in-tree (`scripts/mesh-criticality`), read-only, not cron-wired (on-demand like the sibling
`--suscept`/`--coherent`/`--margin`). Steward lands from the tree. **Unwired next step:** MFDFA — the
multifractal generalization (singularity-spectrum width Δα) that distinguishes a genuinely intermittent
critical/cascade process from simple monofractal colored noise; the exact successor Zhang et al. 2025 use.

## Sources

- [Bak, Tang & Wiesenfeld, PRL 59, 381 (1987) — "…An Explanation of 1/f Noise"](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.59.381)
- [Peng et al., Phys. Rev. E 49, 1685 (1994) — DFA](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.49.1685)
- [Zhang et al., Fractal Fract. 10(4):239 (2025) — SOC + Hurst + MFDFA on China's grid blackouts](https://doi.org/10.3390/fractalfract10040239)
- [Evidence of SOC in time series by the horizontal-visibility-graph approach, PMC9546929 (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9546929/)
- [Revisiting detrended fluctuation analysis, Sci. Rep. (Nature)](https://www.nature.com/articles/srep00315)
