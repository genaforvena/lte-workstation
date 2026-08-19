# Live literature review — complex adaptive systems / edge of chaos: the LEVEL axis

**Date:** 2026-08-19 · **Lane:** genome · **Organ:** `scripts/mesh-criticality` (new `--levels` sidecar)

## What I searched, and where I landed

The mesh's criticality lane is heavily worked: `docs/reviews/` already carries ~20 files on this area
(SOqC/quasicriticality and the Widom line, self-organized bistability, dragon-kings and their
precursors, Kinouchi–Copelli dynamic range, the reverberating safety margin, DFA/1-f, subsampling
deflation, record-dynamics and coherent-noise nulls, allometric scaling, Carroll's "edge of chaos is
not universally optimal", Roig–Muñoz–Morales driven separability, Taylor fluctuation scaling). So the
usual 2023-2025 SOC results — including Kinouchi's self-organized *quasi*criticality and its
dragon-king stochastic oscillations, which the first search surfaced — are already embodied.

Two genuinely fresh candidates came out of the sweep:

1. Calvo, Roig, Corral López, Camacho-Mateu, Cuesta & Muñoz, *"Microbiome association diversity
   reflects proximity to the edge of instability"*, [arXiv:2601.22918](https://arxiv.org/abs/2601.22918)
   (30 Jan 2026) — an estimator of distance to the edge of instability read off the **width of the
   pairwise-covariance distribution**, no avalanches required.
2. Bessone & Plantec, *"Emergent Macro-Criticality from Micro-Critical Agents"*,
   [arXiv:2605.01818](https://arxiv.org/abs/2605.01818) (v1 3 May 2026, v2 17 Jun 2026).

I took (2), because it is the axis every one of the ~18 existing lenses is structurally blind to, and
(1) partly overlaps the existing `--suscept` / proximity-crosscheck work. (1) is left on the table.

## The concept we did not embody: the two levels do not map onto each other

Bessone & Plantec study a multi-agent system with spatially constrained interactions. Each agent
carries its **own** reservoir dynamical system (the microscopic level) and interacts with neighbours
by switching a light on/off, which forms a dynamical interaction network (the macroscopic level).
Sweeping the microscopic parameter around dynamical criticality **against** the macroscopic
interaction topology, they find, verbatim from the abstract:

> "near-critical dynamics within individual agents is not sufficient to produce collective critical-like
> avalanche statistics. Instead, scale-free behavior depends on the effective connectivity of the
> macroscopic interaction network, which controls activity propagation. As a result, macroscopic
> critical-like dynamics are enabled by microscopic regimes that deviate from criticality, with the
> required deviation depending on the properties of the interaction network. […] slightly subcritical
> micro-level regimes support near-critical dynamics across a wider range of macroscopic parameters."

Three claims, all new to this genome:

- **Micro criticality is not sufficient for macro criticality.** Tuning the units to the edge does not
  put the collective at the edge.
- **Effective connectivity, not unit tuning, is what controls propagation.** The macro branching ratio
  is a property of the interaction graph first.
- **The two levels get DIFFERENT set-points, and the robust corner is the asymmetric one.** Slightly
  subcritical micro widens the macro range over which the collective stays near-critical; stacking
  both levels at 1 is the *narrow* corner.

`mesh-criticality` reads exactly one level — the pooled board tape — and every sidecar refines that one
reading. `--margin` already knows the healthy set-point is slightly subcritical, but it places that
margin at the **macro** level; the paper places the deviation at the **micro** level and lets macro sit
at the edge. Nothing in the tool has ever measured a unit.

The nearest existing thing is the SUPERCRITICAL gate's two identity discriminators — same-slug
redispatch repeat (`rdx`) and sender-hub fraction (`hub`). Both read **mass**: how much of the window
one slug or one sender occupies. Occupying a window is not the same claim as begetting one's own next
event, so a busy cron reflex and a self-retriggering one are indistinguishable to `hub`.

## What was built: `mesh-criticality --levels`

`scripts/mesh-criticality`, new read-only sidecar (no alarm, no board post):

- **micro** = the median own-series branching ratio across posters. A poster's own event stream is
  binned on the same grid as the pooled one and run through the same MR slope.
- **κ (macro connectivity)** = the mean number of **distinct OTHER** posters that post within
  `CRIT_LV_COUPLE_S` (300s) after an event — the cross-unit fanout that carries activity between units.
  Judged against a **sender-label-shuffled null** (timing, rate and per-unit counts all preserved, only
  *who* permuted, seeded): `CONCENTRATED` (below the band — structured pathways) / `AT-CHANCE` (κ is the
  rate, not the topology) / `BROAD`.
- **Verdicts:** `MICRO-SUB-MACRO-POISED` (the paper's robust corner) · `STACKED-CRITICAL` (both levels
  near 1 — the fragile corner: the safe macro band is narrowest exactly there, so the mesh sits one
  connectivity increment from tipping while every single-level lens still reads "poised") ·
  `CONNECTIVITY-DRIVEN` (macro hot, units cold: the runaway lives in the propagation topology —
  dispatch fanout, who-answers-whom — and debouncing any single reflex cannot touch it) · `UNIT-DRIVEN`
  (macro hot with hot units: a per-reflex flap, fanout innocent) · `UNITS-HOT-MACRO-COLD` · `BOTH-COLD` ·
  `MICRO-UNREADABLE` · `INSUFFICIENT`.

**The operational payoff is that it splits WHERE a hot board's fix goes** — a question no existing lens
in this tool can answer.

## Three things the build measured that the paper does not say

**1. The per-unit MR fit invents self-excitation out of noise, and the fixture makes the answer known.**
A macro branching stream of m=0.9 split round-robin across 12 posters is a thinning of itself, and
the MR *slope* is the subsampling-robust statistic — so every unit's own m̂ should come back ≈0.9.
It came back **2.363 median (SUPERCRITICAL)**. The mechanism is not thinning noise: round-robin makes
each poster **rate-limited** to ~one post per bin whatever the macro burst does — which is what most
real board posters are — so the unit series is effectively 0/1 and its lags read
`r = [0.012, 0.151, 0.137]`: r₁ an order of magnitude **below** r₂. Tightening `mr_estimate`'s
drop-non-positive-lags rule did **not** fix it (2.363 → 2.713; requiring all lags positive selects the
upward-fluctuating units). The fix that works is a **shape gate**: r_k ∝ m^k must *decay* with lag, so
a series whose autocorrelation is non-positive or non-decaying is refused as unfittable and counted.
Seen red then green; mutating the gate out restores m̂=3.54 on the fixture and the leg fails.

**2. Applying that gate turned this sidecar's own live verdict from a confident label into a refusal —
which is the honest state.** Before the gate the live board read `MICRO-SUB-MACRO-POISED` with micro
median 0.758 (and an IQR of [0.261, 1.014] — already the tell). After it, only **3 of 93 posters**
carry a branching-shaped own-series: 56 are thin (<15 events in 72h) and 34 are non-decaying or
anti-correlated, i.e. cron-clocked or rate-limited. So the board's posters are individually too sparse
to carry a branching estimate at all, and the paper's robust corner **cannot be claimed here**. The
verdict is `MICRO-UNREADABLE`, not `INSUFFICIENT`, because the macro level *is* read: collapsing the
two would file a live connectivity reading as "no data".

**3. The board is an evicting tape, and a window longer than it manufactures the very reading you
want.** `~/.mesh/chat.log` is capped (3000 dated lines here, ~81h). Asking for a longer window does not
buy history — it prepends structurally-empty bins, a step function that is perfectly autocorrelated at
every lag, flattening the MR slope and pushing m̂ **up toward 1**. Measured on this node, same tape,
same instant: **72h (inside coverage) → macro m̂=0.716, `BOTH-COLD`; 168h (past the wall) → macro
m̂=0.924, `MICRO-SUB-MACRO-POISED`.** An eviction artifact wearing the word "poised". The window is now
clamped to the tape's real coverage and the clamp is reported in the output line.

## Live reading (2026-08-19, this node)

```
criticality levels: MICRO-UNREADABLE (micro m̂ median=n/a IQR=n/a [UNKNOWN] over 3 fittable posters,
  macro m̂=1.162 [SUPERCRITICAL], κ=3.375 distinct-other posters per event within 300s
  [CONCENTRATED vs shuffled null [3.838,3.961] med=3.900], units=93 thin=56 unfittable=34,
  events=2724, bins=865, window=72h)
```

The one **positive** finding the lens does deliver: κ=3.375 sits **below** the sender-shuffled null
band [3.838, 3.961] → `CONCENTRATED`. Board activity does not fan out to whichever posters happen to be
awake; it follows structured pathways. That is a statement about the interaction topology which no
existing lens in this tool makes, and it is the level the paper says controls propagation.

Caveat carried honestly: the pooled macro m̂ over a 72h window moved 0.913 → 1.162 within minutes of
wall-clock across runs (`mesh-chat-sync` merges peer lines at earlier timestamps, so the window's
*contents* change, not just its edge). That volatility is a property of the pre-existing pooled
estimator, not of this sidecar, and is not investigated here.

## Gates (`--test`, 7 legs, each seen RED under mutation)

1. Two sender assignments over **one** event stream must give byte-identical macro m̂ — the premise that
   the pooled level cannot see the topology.
2. κ must separate blocked-runs from round-robin by >3× (1.567 vs 10.496).
3. κ counts **distinct OTHER** posters: a single-poster tape has fanout exactly 0. (Pinned separately —
   an identity-blind counter survives leg 2, since both fixtures shift together.)
4. The shuffled null must land the two fixtures on opposite sides (`CONCENTRATED` vs `BROAD`) at equal
   rate and equal per-unit counts — otherwise the verdict came from the rate.
5. The shape gate: the rate-limited fixture must be one the loose MR rule over-fits (m̂>1.5) **and** the
   gated one refuses. Both halves asserted.
6. A read macro level with an unreadable unit level must be `MICRO-UNREADABLE` with **no** micro number;
   a tape with no sender-attributed events must be `INSUFFICIENT`. Distinct labels, no collapse.
7. A window past the tape must clamp to coverage, report it, and read bin-for-bin identical to asking
   for exactly the covered span.

Mutants run from a scratch copy: M1 (split the stream), M2 (drop κ's self-exclusion), M3 (don't shuffle
the null), M4 (remove the decay gate), M5 (collapse `MICRO-UNREADABLE`), M6 (remove the clamp) — all six
caught. Full suite green on clean source.

## Not wired

`--levels` is read-only and unwired by design: it emits no alarm and posts nothing. Wiring it to the
SUPERCRITICAL gate's fix-routing (CONNECTIVITY-DRIVEN vs UNIT-DRIVEN) needs the micro level to be
*readable* first, and on this board it is not.
