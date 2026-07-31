# Autopoiesis live-review — the mortality manifold: a budget point-of-no-return for `mesh-pace`

**Date:** 2026-07-31 · **Lane:** genome (autopoiesis & the biology of cognition) · **Status:** landed, uncommitted (steward lands)

## The concept (live source)

**Connor McShaffrey & Randall D. Beer, "Viability Space Decomposition: A geometric partition of survival
outcomes in single- and multi-agent systems", arXiv:2605.16753 (submitted 2026-05-16).** Beer is the
same enactivist/autopoiesis lineage as the requisite-variety work already landed in `mesh-relay`; this
paper sits squarely in Maturana & Varela's **viability-constraint** tradition (an autopoietic system
persists only while it stays inside a bounded viability region).

Its operational core — verbatim from the abstract:

> "By constraining the dynamics of these agents to bounded viability regions, these models form a class
> of **extended dynamical systems where transient dynamics can lead to death, making traditional
> attractors and separatrices insufficient** for characterizing the global space of possible behaviors.
> To remedy this, we develop viability space decomposition … revealing how several new classes of
> manifolds (**mortality, ordering, and collapse**) permit a complete decomposition of state space into
> regions of qualitatively similar survival outcomes: a **viability portrait**."

The load-bearing new object is the **mortality manifold**: the surface past which death is already
**committed by the transient**, even though *no viability constraint is currently violated*. A system
can be comfortably in-bounds right now and yet be on a trajectory from which the wall is unavoidable.

## Why it is NOT already embodied

The mesh has two kinds of viability read, and the mortality manifold falls between them:

- **Level checks** — "are we in-bounds NOW": `mesh-resource-guard` NODE-PRESSURE, `mesh-load-gate` disk
  floor, `mesh-pace` `over_budget()` (spent ≥ cap). These fire only once the value has *already* crossed.
- **Regime-shift early warning** — `mesh-criticality` branching ratio (statistical CSD near a
  bifurcation). Not a deterministic commitment on a draining resource.

`mesh-resource-guard` *does* read a ramp (`[node-accelerating]`, super-exponential-collapse / dragon-king
detection on MemAvailable), so the **OOM** viability region already has a transient-aware read — landing
there would overlap. The **budget** region does not: `mesh-pace` knows `spent`, `cap`, and turn-burn, and
has `burden_state()` (RISING/FALLING **trend**, memoryless, *no projection*) and `over_budget()` (the OVER
endpoint). Nothing reads the region between "climbing" and "already over" — the committed-in-transient
manifold. It was blind.

## The mechanism — `scripts/mesh-pace --runway` (report-only)

A **budget viability portrait**. Two-sample the rolling-window `$`-spend (persisted, like the OOM-ramp
guard), derive net `$`-burn/h, and classify by *survival outcome*:

| class | meaning |
|---|---|
| `HEADROOM` | eta beyond the 5h window — rolling relief keeps spend under the cap; viable |
| `RECEDING` | net burn ≤ 0 — old spend ages off faster than new accrues; moving **off** the wall (this is the natural-drift point: survival = staying in-bounds, not racing a gradient) |
| `APPROACHING` | eta within the window but beyond the reaction budget — **a HOLD now still averts** the cap |
| `COMMITTED` | **the mortality manifold** — eta ≤ `MESH_PACE_REACT_S` (default 300s): the dispatch HOLD cannot bite in time, so the crossing is unavoidable at this burn |
| `OVER` | spent ≥ cap — death already realized (== `over_budget`; not a manifold read) |
| `UNKNOWN` | no cap armed / unreadable spend / no usable prior / interval too short — honest, never a fake alarm |

`COMMITTED` is the object the paper contributes: **distinct from `OVER`** (death realized) and **from
`APPROACHING`** (control authority still suffices). The distinction is control-authority-agnostic and so
cannot false-alarm on a slow approach: it fires only when even the corrective's *latency* outruns the
crossing.

Guards, all honest-fusion:
- **Min-interval** (`MESH_PACE_RUNWAY_MIN_DT`, default 120s): a rate over a sub-minute `dt` is noise, not
  a rate. A too-young baseline is *kept*, not resampled, so rapid back-to-back calls can't manufacture an
  inflated `$/h` (caught live during development: two calls seconds apart read `$188/h`).
- **Fail-safe**: no cap / unreadable spend / no prior / stale prior (older than the window) → `UNKNOWN`.
- **Report-only**: never touches `eff_gap`, `over_budget`, or the gate — spend behaviour and any
  anticipatory pre-hold stay the operator's call, exactly like `--burden`. No cron wiring (surfaced in
  `--status`, callable on demand).

## Verification (RED-first)

8 hermetic `--test` legs (r–y) drive `spent`/`cap`/`window`/prior via overrides. The **mortality-manifold
distinction** is the RED-first witness: collapsing the `eta ≤ react → COMMITTED` branch into `APPROACHING`
reddens leg (r) (`got 'APPROACHING'`) — the whole point of the axis (past the manifold a HOLD can't avert)
vanishes and every crossing reads as still-avertable. Restored → green. Leg (y) proves the min-interval
guard suppresses a would-be `COMMITTED` derived from a `dt < MIN_DT` noise-rate.

## Files

- `scripts/mesh-pace` — `_fmt_eta`, `runway_state`, `runway_line`; `--runway` case; `--status` line;
  `--test` legs (r–y); help/usage. Report-only, uncommitted.

## Coverage note

Autopoiesis map ([[autopoiesis-review-coverage]]): the "viability constraints, not a fitness gradient"
angle (natural drift) is touched here operationally via the `RECEDING`/viability framing without
re-opening the normativity review. Still open: structural determinism / instructive-interaction,
organization-vs-structure, languaging, the observer.
