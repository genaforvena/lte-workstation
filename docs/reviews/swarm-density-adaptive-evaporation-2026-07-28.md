# Swarm intelligence & stigmergy — density-adaptive evaporation (live review 2026-07-28)

**Angle:** a RECENT (2023-2026) result about the pheromone-evaporation *rate* itself — the one knob
classic ACO/stigmergy holds CONSTANT, and which the current literature says must not be.
**Landed:** the never-taken eviction threshold in `scripts/mesh-dispatch` made **density-adaptive** —
it accelerates under a clogged board and stays patient on a quiet one (uncommitted; steward lands).

## The concept (named + cited)

Stigmergy = agents coordinate through marks left in a shared medium; a pheromone trail *evaporates*
so stale routes fade and the colony keeps exploring. In Ant Colony Optimization the **evaporation
rate is almost always a fixed constant** — and that is now recognized as the field's canonical
weakness. The 2023-2026 frontier makes the rate **adaptive to the state of the medium**, raising it
under congestion / stagnation so a saturated field sheds its stale high-intensity trails and restores
exploration:

- **EPAnt** — *"Ant colony optimization enhanced with ensemble of pheromone vectors using
  multi-criteria decision making"*, **Expert Systems with Applications, Oct 2025**. Runs an
  **ensemble of multiple evaporation rates** fused by MCDM, explicitly *"to enhance global search
  capabilities and resilience against premature convergence"* — i.e. a single fixed rate over-exploits
  and stagnates.
  <https://www.sciencedirect.com/science/article/abs/pii/S1568494625013146>
- **IACA (improved ACO for AGV path planning)** — *SAGE, Proc. IMechE Part D: J. Automobile Eng.,
  **2026***. Couples a reward/punishment pheromone update with an **adaptive evaporation factor** that
  adjusts with search state. <https://doi.org/10.1177/09544070251327268>
- Framing this as *"the evaporation rate is usually fixed … when the algorithm reaches stagnation the
  evaporation rate increases to eliminate the high intensity of pheromone trails"* is the standard
  statement of the mechanism (self-adaptive-evaporation ACO literature, IEEE SSCI lineage
  <https://ieeexplore.ieee.org/abstract/document/7007866/>).
- Robotics grounding — high **agent DENSITY** is exactly when constant-rate stigmergy breaks:
  *"Testing the limits of pheromone stigmergy in high-density robot swarms"* (Hunt, Jones, Hauert,
  **Royal Society Open Science, 2019**) shows a **faster decay rate** reduces the coverage/exploration
  collapse that appears once the swarm is dense (N ≳ 256).
  <https://royalsocietypublishing.org/doi/10.1098/rsos.190225>
- 2024 control-theory framing of evaporation as a *designable* differential-equation parameter:
  *"Stigmergy: from mathematical modelling to control"*, Royal Society, 2024.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC11371424/>

## Why this is somewhere we have NOT been

Our two prior swarm landings (2026-07-27) both act on the *positive* and *diagnostic* sides of the
trail: `mesh-forage` measures **pheromone-entropy** as a stagnation diagnostic, and the **no-entry
repellent** models the negative pheromone. Neither touches the **evaporation RATE** — and the mesh's
one real evaporation mechanism, `mesh-dispatch`'s never-taken eviction (`STALE_TICKS`, default 48
idle-exposed ticks ≈ 4h), was a hard **constant**. That is precisely the fixed-rate stigmergy the
recent work identifies as the weakness: an unclaimed `[task]` posted into a *quiet* board and one
posted into a *saturated* board evaporated on the identical 4h clock, so a clogged queue kept feeding
scan budget to trails no idle hand ever chose to forage.

## The concrete application (named file)

`scripts/mesh-dispatch` — the mind-allocation reflex. The board is the mesh's stigmergic medium; the
never-taken idle-exposure counter is trail intensity; `STALE_TICKS` is the evaporation half-life. The
change makes the **effective** eviction threshold density-adaptive:

- `effective_stale_ticks <backlog>` (pure, defined with its consts above the `--test` block so the
  smoke and live eviction share ONE definition): nominal `STALE_TICKS` while backlog ≤ `CONGEST_KNEE`
  (default 6); past the knee it drops linearly by `step=(STALE_TICKS−STALE_TICKS_MIN)/CONGEST_KNEE`
  per extra backlogged task, reaching the `STALE_TICKS_MIN` floor (default 24 ≈ 2h) at backlog = 2×knee
  and **never below**. A misconfig where `MIN ≥ TICKS` degrades to the constant — never a negative
  threshold that would evaporate everything.
- `CONGEST_BACKLOG` = the count of never-taken tasks currently accruing idle-exposure (task-scoped
  `@mint` EXP_MAP rows with count ≥ 1) — the *crowding of the medium* — computed **once per pass**
  (O(rows), not O(n²) inside the per-task scan).
- **Invariants preserved:** incident tasks stay evaporation-exempt (they exist to survive exactly
  these busy stretches); the READ-ONLY / busy-blind / not-due tick gates are untouched; small boards
  (backlog ≤ knee) behave byte-identically to before, so the whole existing suite stays green.

This **closes the loop `mesh-forage` opened**: mesh-forage *diagnoses* stagnation (pheromone-entropy),
dispatch now *responds* to it by decaying faster.

### Gate (seen RED then GREEN)

`mesh-dispatch --test` gains a unit check of `effective_stale_ticks` (nominal / floor-at-2×knee /
never-below-floor / misconfig-degrades) plus a **black-box** behavioural gate driven against the real
script in a sandboxed HOME: the *same* seeded idle-exposure (30) **evaporates** at backlog 12 (eff 24)
and **survives** at backlog 1 (eff 48), and an incident task past the floor still survives congestion.
Falsified by reverting the eviction to the constant `STALE_TICKS` → the congested assertion goes RED
(exposure 30 < 48 → never evaporates); verified. Full suite: `smoke: ok (188 assertions)`.

## Tuning knobs

`MESH_DISPATCH_STALE_TICKS_MIN` (floor, default 24) · `MESH_DISPATCH_CONGEST_KNEE` (default 6) —
both env-overridable per node; defaults are ACTIVE (not a disabled/unexercised knob).
