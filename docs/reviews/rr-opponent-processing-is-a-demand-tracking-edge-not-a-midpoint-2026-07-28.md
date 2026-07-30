# RR live review — opponent processing is a demand-tracking EDGE, not a balanced midpoint

**Date:** 2026-07-28 · **Area:** relevance realization & the frame problem (Vervaeke) ·
**Angle:** a foundational idea we *applied too loosely* · **Lands:** `scripts/mesh-needs --balance`

## The concept we MISread

The mesh already embodies "opponent processing" in several places, and `mesh-needs --balance`
operationalizes the explore↔exploit pair: it classifies past `needs.log` runs into poles and prints a
verdict. Until today that verdict was:

- `EXPLOIT-PINNED (b<0.10)` → *"the opponent balance has collapsed to one pole"* (a FAULT)
- otherwise → `balanced (both poles active)` (HEALTH)

That is the loose read. It treats the **balanced midpoint as the target** and single-pole dominance as
pathology. The live literature is explicit that this is exactly backwards.

> "The organism doesn't settle at a balanced midpoint; it remains poised responsively at the boundary
> between competing strategies, perpetually sensitive to when shifts are needed."
> — Frontiers Psych 15:1362658 (2024), *Naturalizing relevance realization*
> (https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full)

> "agents continually reassess what strategy does or does not work in a given situation, and adjust
> [their] goals and priorities accordingly" — *ibid.*

The 2025 paper makes the same point via precision-weighting: the trade-offs are **dynamically tuned to
demand**, not held at a set ratio.

> Andersen, Miller & Vervaeke (2025), *Predictive processing and relevance realization: exploring
> convergent solutions to the frame problem*, **Phenomenology and the Cognitive Sciences**,
> doi:10.1007/s11097-022-09850-6 · https://link.springer.com/article/10.1007/s11097-022-09850-6

**The correction:** in RR, the opponent set-point is an EDGE that MOVES with environmental demand.
Exploit-heavy is not a collapse — it is the *correct* posture when demand is high (deficits chronic,
the world genuinely calling for exploitation). It is a fault only when demand is LOW and the system is
stuck at a pole anyway. And the state a midpoint-verdict is blind to is not one-pole dominance at all:
it is the **dark room** — no demand *and* no explore, neither pole engaged, frozen — which a
"rest dominates → fine" reading scores as health.

This sits UPSTREAM of the tool's old verdict the way `mesh-criticality`'s landed
"edge-optimality-is-task-dependent" sits upstream of its m̂ estimator: both correct a mistaken *target*,
not a mistaken measurement. It is distinct from the already-embodied opponent pairs
(efficiency↔resiliency `mesh-sensorium --balance`; explore↔exploit *classification* itself): those
measure *where* the balance sits; none asks whether that position is **justified by current demand**.

## What landed

`scripts/mesh-needs` — read-only, exit 0, no behavior change to injection:

- New pure-awk helper `_demand_verdict` computes **demand density** `d = exploit/total` (share of runs
  that hit a real deficit) alongside the explore index `b`, and emits a token:
  - `TRACKING-HIGH` — exploit-heavy (`b<0.10`) **and** demand high (`d≥0.5`) → RR-correct edge.
  - `DARK-ROOM` — no demand (`d≤0.10`) **and** no explore fired → frozen, the missed pathology.
  - `MIXED` — otherwise.
- `--balance` verdict is now demand-aware: an exploit edge under high demand is reported as
  **RR-CORRECT tuning, not a collapse**; exploit-pinned under *low* demand is the genuine collapse; and
  `DARK-ROOM` is named where the old verdict said "balanced".
- `--test` gains a RED-first gate on `_demand_verdict` (`5 1 0`→`TRACKING-HIGH 83`, `0 9 0`→`DARK-ROOM 0`,
  `3 3 2`→`MIXED 38`); verified it goes RED when the demand threshold is broken, then restored.

**Live finding it already surfaced:** on this node the last 87 runs are 100% `rest` (demand=0%),
explore dormant — the new line reads *"the posture cannot MOVE with demand; a fixed midpoint, not the
poised edge RR requires."* The old verdict called this the explore-pole-off state and stopped; the RR
read names it as a lane that has no demand signal to track at all.

## Sources

- Frontiers in Psychology 15:1362658 (2024), *Naturalizing relevance realization: why agency and
  cognition are fundamentally not computational* —
  https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full
- Andersen, Miller & Vervaeke (2025), *Predictive processing and relevance realization*, Phenom. Cogn.
  Sci., doi:10.1007/s11097-022-09850-6 — https://link.springer.com/article/10.1007/s11097-022-09850-6
- Vervaeke, Lillicrap & Richards (2012), *Relevance Realization and the Emerging Framework in Cognitive
  Science*, J. Logic & Computation — http://sites.utoronto.ca/jvcourses/jolc.pdf
