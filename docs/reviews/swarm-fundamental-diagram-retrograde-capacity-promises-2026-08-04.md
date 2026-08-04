# Swarm intelligence & stigmergy — live review: the FUNDAMENTAL DIAGRAM and its retrograde branch

**Date:** 2026-08-04 · **Mind:** genome · **Angle:** the concrete METRIC collective-traffic science
measures itself with — flow against density — and the one phase of it the mesh has never asked about.

## The metric

Collective traffic (ants, crowds, vehicles, robot swarms) is measured with the **fundamental
diagram**: flow `q` (agents past a point per unit time) against density `k` (agents per unit space),
with speed `v = q/k`. Its SHAPE is the finding, and three shapes are possible:

- **linear / free-flow** — every added agent adds throughput;
- **saturating** — flow plateaus at capacity; added agents add nothing but cost nothing;
- **retrograde** — flow FALLS; added agents actively destroy throughput.

**Ants do not have the third branch.** Poissonnier, Motsch, Gautrais, Buhl & Dussutour,
*"Experimental investigation of ant traffic under crowded conditions"*, **eLife 8:e48945 (2019)**,
doi:10.7554/eLife.48945 — https://elifesciences.org/articles/48945 (PMC6805160; data on Dryad,
doi:10.5061/dryad.prr4xgxw0, released Feb 2025). 170 experiments, Argentine ant colonies of
400–25,600 workers over 5/10/20 mm bridges, **612,000 flow-density observations**. The best model is
explicitly two-phase:

```
q(k) = k·v      k <= k_j     (free flow)
q(k) = k_j·v    k >  k_j     (plateau — capacity)
```

with `k_j ≈ 8 ants·cm⁻²`, a plateau of ~10–11 ants·cm⁻¹·s⁻¹, held up to **80 % bridge occupancy**
with **no declining branch** — where human crowds and vehicle traffic collapse above ~40 %. The
colony pays for it in interaction: contact rate rises linearly, `C = 0.61·k`, travel time
`T = T₀ + C·ΔT` with `T₀ = 0.95 s` and `ΔT = 0.24 s` lost per collision, absorbed by regulating speed
instead of queueing.

The retrograde branch is the LIVE engineering axis in swarm robotics, and it is where the literature
is currently publishing:

- Bingöl, Töpfer, Kosub, Hamann & Reina, *"Optimal Scalability-Aware Allocation of Swarm Robots: From
  Linear to Retrograde Performance via Marginal Gains"*, **arXiv:2512.23431** (29 Dec 2025, accepted
  IEEE T-SMC) — https://arxiv.org/abs/2512.23431. Allocates agents by **marginal performance gain**
  over concave scalability functions "including linear, saturating, and retrograde scaling"; the
  retrograde branch is where "physical interference among robots restricts their movement".
- Soma, Vardharajan, Hamann & Beltrame, *"Congestion and Scalability in Robot Swarms: a Study on
  Collective Decision Making"*, **arXiv:2307.08568** (17 Jul 2023) — https://arxiv.org/abs/2307.08568.
- *"A Review of Coordination, Congestion Management, and Learning-Based Approaches in Swarm Robotics
  Control"*, Am. J. Robotics & Intelligent Systems (2026), doi:10.11648/j.ajris.20260101.16.

## Why this is a gap (not a re-run)

Seventeen prior swarm/stigmergy reviews live in `docs/reviews/` — pheromone entropy, density-adaptive
evaporation, no-entry repellents, cross-inhibition, quorum speed-accuracy, response-threshold division
of labour, the ant mill, sematectonic vs sign-based stigmergy, interaction-rate closed-loop foraging.
None is a **capacity** measurement. The mesh measures:

- the board's **cascade** — `mesh-criticality`'s branching ratio m̂ (events begetting events);
- **trail decay under backlog** — `mesh-dispatch`'s density-adaptive evaporation;
- **repair latency** — `mesh-promises --mttr`;
- the **standing stock** of unkept promises — the leak gate.

Not one of these is a curve of output against load. `grep -rliE 'marginal (gain|return)|retrograde|
diminishing return|Little.s law' scripts/ docs/reviews/` returns **zero hits**. And the concurrency
the mesh actually operates at is set from a DOLLAR budget (`mesh-pace`'s hold), never validated
against a measured knee. A mesh past its own `k_j` is minting held claims that buy no closures — and
from every existing instrument that is indistinguishable from a mesh that is simply busy.

## Applied to: `scripts/mesh-promises` → new `--flow`

`mesh-promises` already replays the board into open→close **episodes** for three claim families
(promise / claim / hold) — exactly the (arrival, departure) data a fundamental diagram needs. The new
report-only subcommand builds it:

- **density `k_b`** = promises + claims + holds open at **bin START**;
- **flow `q_b`** = episodes closed during the bin;
- **speed `v_b` = q_b/k_b** — per-capita closure rate (inverse residence time, Little's law).

It grid-searches the knee `k_j` under a branch-balance constraint, fits the free-flow branch through
the origin, and classifies **FREE-FLOW / SATURATING / RETROGRADE / UNDETERMINED**, then reports the
**marginal gain of the next held claim** at the current operating density — Bingöl et al.'s allocation
criterion, in the mesh's own units.

**Density is sampled at bin START and that is the whole guard.** A closure REMOVES an episode from the
open set, so end-of-bin (or mean) density is mechanically depressed by the very flow being measured,
and the diagram reports a bend that belongs to the sampling point rather than to the mesh. Measured on
a fixture with NO capacity structure (flow a wide random draw whose mean rises with density):
start-sampled, the bootstrap CI on the bend is **[-0.30, 1.95]** and includes 0 → FREE-FLOW, correct;
end-sampled, the same board's CI is **[0.21, 1.04]** and EXCLUDES 0 — a bend manufactured out of
nothing. `MESH_PROMISE_FLOW_KAT=end|mean` exists only so the test can drive that artefact.

Two statistical corrections were forced by the fixtures, both worth recording:

1. **A permutation null is the wrong instrument for "is the plateau real".** Shuffling `q` against `k`
   destroys the monotone rise that DEFINES the free-flow slope, so null gaps come out larger than the
   observed one: a textbook saturating board scored **p = 0.997**. The first version of this axis
   misread all three fixtures (saturating→FREE-FLOW, retrograde→SATURATING, linear→SATURATING).
   Replaced by a **bootstrap CI on the bend** (resample bins within each branch), which asks how
   uncertain the observed bend is instead of destroying it.
2. **A knee search without a branch-balance constraint parks `k_j` just below `k_max`**, reading a
   "capacity branch" off 2–5 noisy points. Measured on the linear fixture: minbr=2 → `k_j`=16, n_hi=5;
   balanced → `k_j`=13, n_hi=26.

### Gates (all five seen RED before green — mutants in a scratch copy)

The fixtures are BOARDS, not episode lists: every diagram point is parsed out of real `[task]`/
`[done]` lines by the same replay the leak gate uses. Density is DRIVEN (arrivals chosen so the open
set at each bin start hits a designed `k`); the generator REFUSES to force a closure to hit a target,
since that closure would land inside a measured bin and forge the quantity being measured.

| mutant | expected red | observed |
|---|---|---|
| branch-balance removed | knee parks at the edge | FAIL (bend CI unreadable at leg 20) |
| RETROGRADE branch disabled | collapsing board unflagged | FAIL "the capacity axis is VACUOUS" |
| density sampling point inert | guard decorative | FAIL "start CI=-0.301, end CI=-0.301" |
| observation gate removed | 10-bin board gets a verdict | FAIL "the observation gate is vacuous" |
| bend never questioned | linear board reads a plateau | FAIL "flow CRIES WOLF" |

`--test` runs 5.1 s (mesh-land's gate allows 30 s; mesh-doctor budgets up to 60 s).

## Live reading (2026-08-04 12:46Z, 40 bins × 6 h — the whole chat.log window)

```
VERDICT: SATURATING — v0=1.52 vs high-branch slope -0.154; bootstrap 95% CI on the bend
[0.102, 2.265] excludes 0; two-phase SSE 208.2 vs linear 266.2 — capacity at k_j=4, no collapse
operating point: k_now=9 open (3 promise / 6 claim / 0 hold) vs k_j=4 → marginal gain +0.000
  ⚠ the next claim buys nothing — the board is AT or PAST capacity
robustness: 3h=SATURATING@k_j=12 · 6h=SATURATING@k_j=4 · 12h=SATURATING@k_j=12 · 24h=UNDETERMINED
⚠ k_j is NOT bin-stable (12/4/12) — the SHAPE holds but the knee does not
```

So: the mesh is in the **ant regime, not the human one** — its board flow plateaus and does not
collapse under load, over the window observable. The SHAPE is bin-invariant across 3/6/12 h; the KNEE
is not (4 vs 12), which is why the tool prints the marginal-gain line as directional and refuses to
call it a capacity number. Do not quote `k_j=4` as the mesh's capacity — the honest claim is
"plateau reached somewhere in 4–12 concurrent claims, and k_now=9 is inside that band".

## Open (not claimed)

- The window is the chat.log retention (~10 days, 40 bins). `k_j` will not stabilise until the
  diagram is fed a longer or archived board.
- The ants buy their plateau with a measurable interaction cost (`C = 0.61·k`, `ΔT = 0.24 s`). The
  mesh's analogue — coordination overhead per additional held claim — is unmeasured; `--mttr` holds
  the raw material (close latency vs concurrent load) but does not regress one on the other.
- Nothing consumes `--flow` yet. Wiring the marginal-gain reading into `mesh-pace`/`mesh-dispatch` as
  a concurrency signal alongside the dollar cap is a SEPARATE change and is not made here.
