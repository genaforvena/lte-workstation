# Driven criticality: the mesh has sixteen lenses on ONE transition and zero on the one it names itself after

*Live literature review, 2026-08-18 — complex adaptive systems / edge of chaos (Santa Fe lineage), angle:
a foundational idea we applied too loosely. Organ: `scripts/mesh-criticality`.*

## The misread

`scripts/mesh-criticality` opens by defining its own verdict:

> `m≈1 CRITICAL (self-similar, power-law cascades — maximally responsive without runaway)`

and the mesh has read that as **the edge of chaos** since the tool was written. It is not. Those are two
different phase transitions:

| | order parameter | the question it answers |
|---|---|---|
| **absorbing-state** transition | branching ratio m̂ | quiescent ↔ active: does activity **propagate**? |
| **edge of chaos** | largest Lyapunov exponent | contracting ↔ expanding: does a perturbation **decay or amplify**? |

The literature is explicit that they need not co-occur. Kanders, Lorimer & Stoop tuned a recurrent spiking
network from subcritical through critical to supercritical **avalanche** behaviour and found the largest
Lyapunov exponent stayed **positive throughout** — the avalanche axis swept its entire range while the
dynamical axis never moved
([Chaos 27, 047408, 2017](https://pubs.aip.org/aip/cha/article/27/4/047408/322534/Avalanche-and-edge-of-chaos-criticality-do-not)).
Hochstetter et al. then showed which of the two buys the property we invoke it for: in neuromorphic
nanowire reservoirs it is the **edge-of-chaos** measure, not the avalanche measure, that tracks task
performance ([Nat. Commun. 12, 4008, 2021](https://www.nature.com/articles/s41467-021-24260-z)).

Count the lenses in the file: `--shape`, `--crackling`, `--complexity`, `--compress`, `--widom`,
`--dynrange`, `--sob`, `--suscept`, `--coherent`, `--margin`, `--aging`, `--hurst`, `--coarse`, `--dtc`,
`--allometry`, plus m̂ itself. Sixteen. Every one reads the **same absorbing-state axis** from a different
angle — bin width, subsampling, drive, exponent coherence, stationarity, noise amplitude, system size. Not
one asks whether a perturbation here decays or amplifies. Sixteen necessary conditions on one transition do
not become a second axis by being numerous, and the sentence they are used to support is a property of the
other one.

## The concept we did not embody

**Marginal driven stability**, and the **finite-resolution neighbourhood separability index** that locates
it — Adrián Roig, Miguel A. Muñoz & Guillermo B. Morales, *"Driven criticality links universal computation
and optimal representations"*, [arXiv:2607.21232](https://arxiv.org/abs/2607.21232) (submitted 23 Jul 2026,
revised 27 Jul 2026).

Their claim: for a **driven** system the relevant edge is not the autonomous system's Lyapunov edge but
marginal *driven* stability, and it is located by two measures that must be read **together**:

1. an **input-conditioned maximal Lyapunov exponent** — R1 contracting (MLE<0, input memory lost), R2
   marginal (MLE≃0⁻), R3 expanding (MLE>0, mixing and saturation);
2. a **finite-resolution neighbourhood separability index** — for nearby but *disjoint* input
   neighbourhoods A and B,

   ```
   Δ_AB = ‖m(X_A) − m(X_B)‖₂ − [ r(X_A) + r(X_B) ]
   ```

   centroid distance minus the two response-cloud radii. Δ>0 certifies the neighbourhoods stay
   distinguishable **at finite resolution**; Δ<0 is cloud overlap. NSI = mean of the positive margins.

Separability, chaotic-series prediction and representation geometry all optimise in the *same narrow
window* — which is exactly why both halves are needed: a marginal exponent **without** separability is not
the good regime, it is a system that neither forgets nor distinguishes.

Nothing in the mesh embodied this. Grepping all 223 prior reviews: no `Lyapunov` in a criticality context,
no `damage spreading`, no `Derrida`, no `separation of timescales`, no `NSI`.

## What was built (`scripts/mesh-criticality --separability`, uncommitted)

The board **is** a driven system. Bin it exactly as m̂ does; let `v_t = A[t−H:t]` be the **condition** and
`w_t = A[t:t+H]` the **response**. Neighbourhood pairs are anchors `2ε < d ≤ 4ε` apart — nearby, and
*disjoint by construction*, so no point can lie within ε of both. This is **damage spreading read off the
tape instead of injected**: the history supplies the nearby initial conditions, so nothing has to be
perturbed on a live mesh to measure the axis.

Three things carry the design:

- **ε is a quantile of the tape's own pairwise condition distances**, never an absolute. A fixed ε rots the
  moment board volume moves.
- **A Theiler window is load-bearing.** Consecutive condition windows overlap by H−1 bins, so adjacent
  pairs are close *because they are the same data*, and their responses are close for the same reason. Left
  in, they mint a verdict out of the embedding alone. Every pair with |i−j| ≤ 2H is excluded, from the gain
  pairs and from neighbourhood membership.
- **The verdict is a comparison with a null, never a raw number.** A purely stochastic series also
  separates neighbours instantly. Both statistics are recomputed over the *same pair sets* with the
  response index **shuffled** — destroying the condition→response relation while preserving both marginals.

Verdicts: `SEPARABLE` / `UNSEPARATED` / `NO-STATE-DEPENDENCE` / `INSUFFICIENT`. Read-only; it never touches
m̂, the regime, or the SUPERCRITICAL alarm — the restraint every sidecar in that file keeps.

### Honest negative: the MLE half did not transfer, the NSI half did

A raw ratio ‖Δw‖/‖Δv‖ is **not** the input-conditioned exponent on a driven integer count series: every
response carries a noise term whose size is independent of ‖Δv‖, so the ratio measures noise/ε and reads
EXPANDING on anything stochastic. Moving the noise into a regression **intercept** fixes that much and not
the rest. On fixtures whose true gain is known by construction (a reflecting AR(1) driven at
a = 0.25 / 0.60 / 1.00 / 1.45, σ=3 — the fixtures `--test` asserts on), the fitted slope reads

```
0.00 / 0.11 / 0.61 / 0.35
```

— attenuated by regression dilution (‖Δv‖ and ‖Δw‖ are norms of differently-aligned vectors) and
**non-monotone** once folding decorrelates the far pairs. A slope that is neither calibrated to 1 nor
monotone in the true gain cannot carry a contracting/marginal/expanding verdict, and forcing one would be
precisely the plausible-constant failure the rest of that file is written to avoid. So the gain is
**reported** with its CI and its noise floor, and carries exactly one verdict — its comparison against the
shuffled null (slope 0), which is a comparison and not an absolute threshold. Same restraint the `--dtc`
sidecar already keeps for RAD.

The NSI half is different in kind: **Δ_AB subtracts the two cloud radii, so drive noise is absorbed by
construction.** On the same four fixtures `sep_frac` reads

```
0.00 / 0.00 / 0.79 / 0.00
```

— separable only in the marginal window, unseparable on *both* sides of it, exactly the paper's claim.
Stated limit: at H=2 and low noise the expanding fixture still reads SEPARABLE (two steps of 1.45 gain is
amplification, not yet mixing) — the horizon bounds what "mixed" can mean here.

### The gate, seen red

Four mutants, run from a scratch copy:

| mutant | result |
|---|---|
| Theiler window disabled | **FAIL** — "disabling the Theiler window changed neither the verdict nor the gain — the window is decorative" |
| effect floor removed (`NSP_SEP_MIN=0`) | **FAIL** — the mixing fixture reads SEPARABLE on sep_frac=0.020 — 2 positive margins out of 102 |
| gain-vs-zero null gate removed | **FAIL** — i.i.d. counts stop reading NO-STATE-DEPENDENCE |
| radii subtraction dropped from Δ_AB | **FAIL** — the marginal fixture stops reading SEPARABLE |

The Theiler guard **passed its mutant on the first attempt** and was not a gate: it compared
`driven_separability(_drive(1.45,3), theiler=0)` against `driven_separability(_drive(1.45,3))` — two
*different* random draws, so the two results differed on noise alone and the assertion could never fire.
Fixed by drawing the series once and feeding the same tape both ways.

Unmutated `--test`: `smoke-test: ok`, 2.1s (inside `mesh-autowire`'s 30s test timeout).

## What it says about this node — measured

Live, `~/.mesh/chat.log`, 2026-08-18, alongside `m̂=1.448 [SUPERCRITICAL]`:

| bins | H | verdict | sep_frac | disjoint pairs | gain CI |
|---|---|---|---|---|---|
| 60s | 2 | INSUFFICIENT | — | 0 | — |
| 300s | 2 | NO-STATE-DEPENDENCE | — | 0 | [−0.130, 0.347] ∋ 0 |
| 300s | 3 | **UNSEPARATED** | **0.000** | 88 | [0.149, 0.455] |
| 600s | 2 | **UNSEPARATED** | **0.000** | 100 | [0.036, 0.354] |
| 900s | 2 | **UNSEPARATED** | **0.000** | 90 | [0.060, 0.344] |

At every resolution where the axis is testable at all, **not one of ~90–100 disjoint neighbourhood pairs
produces separable response clouds**. There is weak state-dependence at the coarser bins (the gain CI
excludes 0), and it buys nothing: distinct present board states do **not** lead to distinguishable futures
at this resolution. The board's forward behaviour is dominated by drive, not by its own state.

Corroboration from a lens already in the file, pointing the same way by a different route: `--complexity`
reads `CECP=MEMORYLESS-POISSON-LIKE n=361 H=0.99 C=0.01` on the same window — the inter-arrival *ordinal*
patterns carry no temporal memory either. Different claim, same direction. `Bin=GLUING` and
`Edge=EDGE-UNPRODUCTIVE` are consistent with a board whose bins are stitching independent arrivals together.

So the operative sentence: **`m̂=1.448 SUPERCRITICAL` is a true statement about activity propagation and
carries no evidence whatsoever about the edge of chaos on this node** — and now the tool says so in its own
voice instead of leaving the reader to import the neuroscience connotation.

## What is not claimed

- This does not falsify m̂ or any of the sixteen lenses. Every one of them still measures what it says.
  What is corrected is the *sentence they are used to support*.
- `NO-STATE-DEPENDENCE` deliberately does not name a regime: an independently-driven board and a strongly
  contracting one are indistinguishable on this tape, and the label says so rather than picking one.
  Blindness, not calm.
- n is one node's board over 72h. The `sep_frac = 0.000` result is stable across three (bin, H)
  settings, which is stronger than a single reading, but it is not a fleet claim.

## Unwired next

The natural continuation is the paper's own setting: pool the neighbourhood pairs **across nodes' boards**
rather than ranking one tape against itself — the same "pool across tapes" note `--dtc` already carries for
RAD. Not attempted here.

## Sources

- [Kanders, Lorimer & Stoop, "Avalanche and edge-of-chaos criticality do not necessarily co-occur in neural networks", Chaos 27, 047408 (2017)](https://pubs.aip.org/aip/cha/article/27/4/047408/322534/Avalanche-and-edge-of-chaos-criticality-do-not)
- [Hochstetter, Zhu, Loeffler, Diaz-Alvarez, Nakayama & Kuncic, "Avalanches and edge-of-chaos learning in neuromorphic nanowire networks", Nat. Commun. 12, 4008 (2021)](https://www.nature.com/articles/s41467-021-24260-z)
- [Roig, Muñoz & Morales, "Driven criticality links universal computation and optimal representations", arXiv:2607.21232 (2026)](https://arxiv.org/abs/2607.21232)
- [Muñoz-adjacent live continuation read while searching: "Beyond the Edge of Chaos: Stability-Expressivity Transfer in Reservoir Forecasting", arXiv:2607.17909 (2026)](https://arxiv.org/abs/2607.17909) — the best forecasting spectral radius does *not* coincide with the Lyapunov edge; noted, not transferred.
