# Autopoiesis & the biology of cognition (live review): causal symmetrization — operational closure has a DYNAMICAL signature, and ours is absent

**Date:** 2026-08-04
**Area:** autopoiesis / biology of cognition (Maturana & Varela), from the angle of a **recent empirical result** (2025-12) rather than the philosophy.
**Landing:** a mechanism we do NOT embody — **causal symmetrization**, the direction-ratio of predictive coupling between a system's *structure* and its *activity*. Landed as `scripts/mesh-closure --symmetry` (report-only).
**Live verdict on this genome:** **ACTIVITY-DRIVEN** — g(A→S)=0.054 p=0.021 vs g(S→A)=0.006 p=0.675. The mesh has structural closure without the dynamical signature of operational closure.

---

## The paper

> **Anthony Gosme, "Causal symmetrization as an empirical signature of operational autonomy in complex systems", arXiv:2512.09352** (v2, submitted 2025-12-09) — https://arxiv.org/abs/2512.09352

Found by searching the live literature for post-2023 work on operational/organizational closure; it is the only recent entry that turns closure into a **measurement on time series** rather than a graph property. (Also surfaced and passed over: arXiv:2601.04501 *The Minary Primitive of Computational Autopoiesis* — a constructive toy, no metric; and arXiv:2606.23122 *A Matter of Time*, which we **already landed** this morning as `--timescale`.)

The move: an operationally-closed system is *defined* by **reciprocal constraint between form and function**, so closure should leave a **directional** fingerprint in the joint dynamics of (structure, activity).

- Data: 50 large-scale collaborative software ecosystems, **11,042 system-months**.
- Structure index **Γ** = structural survival × content survival — persistence of an edit at a horizon, with a relocation penalty λ=0.8 and deletion scoring zero (robust for λ ∈ [0.6, 1.0]).
- Coupling: bivariate **VAR** (ADF stationarity check, first-difference if needed, AIC lag selection, max 6), and the **ratio of Granger strengths** structure→activity ÷ activity→structure.
- Result: exploratory regime (Γ < 0.4) has ratio **0.71** (activity-driven); mature regime (Γ ≥ 0.7) has **0.94** (bidirectional) — *causal symmetrization* — alongside a **1.77-fold variance collapse** (σ² 0.0146 → 0.0083). A composite viability index V = A_norm × Γ reaches AUC 0.88 vs 0.81 for activity alone, discriminating "structural zombie" systems: high activity, decaying architecture.
- The authors are careful, and so are we: symmetrization is a **necessary statistical signature consistent with** operational closure, "without implying biological life or mechanistic closure", and Granger "establishes predictive precedence, not generative mechanism".

## Why this is new here

Every closure claim the mesh has built is an assertion about **structure**:

| already embodied | what it asks |
|---|---|
| `mesh-closure` (graph, 2026-07-28) | does A's product reach B? (mention-based enablement graph) |
| `mesh-closure --timescale` (2026-08-04) | is that product *conserved* at B's clock? |
| `mesh-vitality allopoiesis_gap` | how long does the land→deploy loop stay open? (latency) |
| `mesh-vitality heteronomy_index` | who *pays* for cognition? (sympoiesis, by dollar) |
| `mesh-vitality assembly_signature` | does the commit corpus evidence selection? |
| `mesh-cooscillate` lead/lag | are two **sensor** streams anticipatorily or reactively coupled? |

None of them asks the dynamical question: **over time, does the constraint network predict the work, or only follow it?** A genome can score CORE on every static edge — ours scores CORE=180, LOOPS=89 — and still be purely activity-driven: tools changed only when work demands, never themselves shaping what gets done next. That system has structural closure and no operational closure, and until now nothing here could tell the two apart. (0 prior `grep -i granger|directional coupling|transfer entropy` hits in `scripts/`.)

## The transfer

Two series from the genome's own git history (default 6h bins over 70d → n=240):

- **ACTIVITY** `A_t` = log1p(lines changed in bin t).
- **STRUCTURE** `S_t` = **Γ_t**, mean persistence of the edits made in that bin: **1.0** if the file is not touched again within horizon τ (48h), **0.8** if the only thing inside τ is a pure relocation (the paper's λ), **0** if rewritten. Renames are chained old→new so a moved file is not a dead file.

Then g(S→A), g(A→S) = ln(RSS_restricted / RSS_unrestricted) from a bivariate VAR, lag L by AIC over a fixed sample, and the symmetry ratio in the paper's orientation.

### The leakage guard (the load-bearing detail)

Γ_t is computed from what happens in **[t, t+τ]** — a forward-looking quantity. Published at bin *t* it carries future activity inside it, and g(S→A) is inflated **by construction**: a difference whose sign is guaranteed. So Γ is published at the bin where its horizon **closes** (t + τ/bin), the moment the verdict is first knowable.

This is not a hypothetical. Measured live, same code, guard on/off:

| | g(S→A) | p | g(A→S) | p | ratio | verdict |
|---|---|---|---|---|---|---|
| **unguarded** | 0.0497 | **0.020** | 0.0415 | 0.036 | 1.198 | **SYMMETRIZED** |
| **guarded** | 0.0063 | 0.675 | 0.0544 | **0.021** | 0.115 | **ACTIVITY-DRIVEN** |

The naive form reads its own look-ahead as structure causing work, and would have reported the mesh operationally closed on the strength of it.

## The live finding

```
mesh-closure --symmetry: causal SYMMETRIZATION of structure <-> activity
  n=240 bins  VAR lag L=3 (AIC)  deseasoned=1  differenced: S=0 A=0
  g(structure->activity) = 0.006272   p=0.6750   (exact circular-shift null, 239 shifts)
  g(activity->structure) = 0.054401   p=0.0208
  symmetry ratio (S->A)/(A->S) = 0.115
  VERDICT: ACTIVITY-DRIVEN
```

Ratio **0.115** — far below even the paper's *exploratory* 0.71 (their cut-points are not imported as thresholds; noted only for scale). The genome's constraint network **follows** the work: what got written predicts how durable the network's next edits are, and nothing measurable runs the other way.

**Robustness swept before it was believed** — bin ∈ {4,6,8,12}h × τ ∈ {24,48,72}h, 12 cells:

- 7/12 **ACTIVITY-DRIVEN**, 5/12 **DECOUPLED**, **never SYMMETRIZED, never STRUCTURE-DRIVEN**.
- g(A→S) > g(S→A) in **11 of 12** cells.
- τ=72h washes the axis out (fewer independent survival verdicts per bin) — the boundary of the measurement, not a finding.

So the direction of the asymmetry is robust; the significance of the weaker leg is not. That is exactly the claim the tool prints.

This is the **dynamical twin of the allopoiesis gap**: that metric measures how long the produce→land→deploy loop stays *open* in hours; this one says that even when it closes, the structure it produces does not measurably shape what the mesh does next.

## Implementation

`scripts/mesh-closure` **+386 lines** (uncommitted, for the steward). New: `--symmetry` and `--symmetry-series` (debug). Report-only — it never prunes, never edits cron, never gates, matching the rest of the tool.

Honesty bounds, all in the header:

- **Significance is an exact circular-shift permutation test** on the source series (all n−1 shifts, p = (1+#{g_k ≥ g_obs})/(1+n_shifts)) — not a parametric F-test. Both series are strongly autocorrelated, where a parametric p is anticonservative (the [[cooscillate-parametric-p-ignores-autocorrelation]] precedent). Deterministic: no seed, no sampling.
- **Diurnal common drive is removed first** (per-bin-of-day mean). The shift null does *not* save you here — measured on the test fixture, deseasoning off gives g(S→A)=0.323 p=0.013 and a confident, entirely spurious STRUCTURE-DRIVEN.
- Near-unit-root heuristic (lag-1 ρ ≥ 0.9 → first-difference), **not** an ADF test; reported as dS/dA so the reader knows which series was transformed.
- The verdict is **significance-based, not the paper's 0.71/0.94 cut-points** — importing a threshold across substrates is how a constant outlives its reader. The ratio is reported as a continuous index.
- Granger = predictive precedence, not mechanism.

### Gates (RED-first: 11 mutants, all seen RED)

`--test` grew five estimator legs driven by synthetic series of **known direction** (s2a → STRUCTURE-DRIVEN, a2s → ACTIVITY-DRIVEN, mut → SYMMETRIZED, ind → DECOUPLED, lag3 → STRUCTURE-DRIVEN at lag 3 only), a diurnal-drive leg, a hand-computed git-churn fixture pinning the series builder, an UNDETERMINED leg, and two strict-fixture legs. Runtime 2.7s.

| mutant | legs red |
|---|---|
| leakage guard removed (Γ published at the edit bin) | 6 |
| rename chaining disabled | 2 |
| relocation λ 0.8 → 0 | 1 |
| τ horizon ignored | 1 |
| direction swap in the estimator | 3 |
| verdict pinned to SYMMETRIZED | 5 |
| permutation p replaced by a constant 0.01 | 5 |
| min-N floor removed | 1 |
| strict fixture → silent fallback to live git | 1 |
| AIC lag selection pinned to L=1 | 1 |
| deseasoning removed | 2 |

Two of these were **green on the first pass and had to be earned**: the min-N leg used a 5-point series, which the regression rejects as singular anyway (the leg passed for the wrong reason — [[a-mutant-can-go-red-for-the-wrong-reason]] in the inverse direction), so it now uses 20 points, long enough to regress and short of the floor; and AIC lag selection was ungated until the `lag3` fixture was added, because every other fixture happens to select L=1.

The mutual-coupling fixture also had to be made **stable** (cross-coefficients 0.45, spectral radius 0.75): at 0.9/0.9 the two series explode into collinearity and the second regression degenerates to a false "no coupling" — a property of the fixture, not the estimator ([[a-resource-cap-masks-the-mutant-behind-it]] shape).

## What this does NOT claim

- Not that the mesh is unhealthy. ACTIVITY-DRIVEN is the paper's *exploratory* regime, which is where a system that is still being built belongs.
- Not a mechanism. Granger precedence over 240 bins of one repo's history.
- Not a gate. Nothing in the mesh acts on this number, and nothing should until the axis has been watched across several sweeps.

## Next (unwired, on purpose)

The obvious follow-up is a **trajectory**: the paper's finding is a *transition* between regimes, and a single ratio cannot show one. A windowed g-ratio over the tape would say whether the mesh is moving toward symmetrization or away from it. Left undone deliberately — 62 days of history is one window, not a trajectory.
