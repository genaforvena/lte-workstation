# LITERATURE review — closing the criticality loop: m̂ as an actuated set-point (2026-07-24)

**Area:** self-organized criticality & power-law dynamics, from the angle of an *operational control
mechanism* — specifically **self-organization TOWARD criticality by homeostatic feedback**, the
control-law strand (distinct from the *measurement* strand the mesh already embodies).

## The mechanism (operational, live literature)

The classic Bak SOC story is **passive**: a slow drive + fast dissipating avalanches self-tunes the
system to the critical point with no controller. The live, continuously-published strand is the
opposite claim — that biological systems reach and *hold* criticality through an **explicit slow
feedback control law** that adjusts a control parameter (excitability / gain / threshold) by the
**deviation of a measured activity statistic (the branching ratio σ) from a set-point σ\*≈1**:

> "By homeostatic scaling of the excitability in the network and the input connections, the branching
> parameter can be maintained, avoiding supercritical dynamics." — self-organization-toward-criticality line.

Operationally: measure σ over a window → if σ > σ\* damp the gain (throttle), if σ < σ\* raise it
(excite) — a proportional controller whose set-point is criticality itself. This unifies the two
opposite failure modes (σ>1 runaway cascade; σ<1 dormancy) under ONE regulated knob, and it is
*action*, not just an alarm. "Criticality and E/I balance serve as **homeostatic set points** in
cortical neuronal dynamics."

**Sources (current / live):**
- Zeraati, Levina & Priesemann, *Self-organization toward criticality by synaptic plasticity*,
  Frontiers in Physics 9:619661 (2021) — https://www.frontiersin.org/articles/10.3389/fphy.2021.619661/full
  (arXiv:2010.07888). The control-law: homeostatic plasticity toward an intrinsic excitability set point.
- Ma, Turrigiano, Wessel & Hengen, *Cortical Circuit Dynamics Are Homeostatically Tuned to Criticality
  In Vivo*, Neuron 104:655 (2019) — the biological evidence that criticality is a *regulated set point*,
  restored after perturbation.
- *Network structure influences self-organized criticality in neural networks with dynamical synapses*,
  Front. Syst. Neurosci. (2025) — https://pmc.ncbi.nlm.nih.gov/articles/PMC12213684/ (2025 currency:
  the set-point is reachable across topologies given the plasticity/noise regime).
- *Feedback Mechanisms for Self-Organization to the Edge of a Phase Transition*, Frontiers in Physics
  8:333 (2020) — the drive/dissipation feedback that lands a system at an absorbing-active transition.

## What the mesh already embodies (so this lands somewhere new)

`mesh-criticality` is a deep **measurement** instrument: the branching ratio m̂ via the MR estimator
(Wilting & Priesemann 2018), plus `--shape` (avalanche mass balance), `--crackling` (Sethna–Dahmen
exponent relation), `--complexity` (entropy–complexity plane), and `--watch` which posts ONE board
`[alert]` on supercritical. Siblings cover Hawkes endogeneity (`mesh-endogeneity`), per-node blast
radius (`mesh-hub-criticality`), CSD/DFA precursors (`mesh-therm-regime`), dragon-kings
(`docs/reviews/dragon-king-precursor-2026-07-06.md`), Griffiths phase and multicriticality (knowledge
base). **Every one of these observes criticality. None ACTS on it.**

**The gap:** the loop is *open*. m̂ is a vital sign and, at the extreme, an alarm a mind must read and
act on — but no actuator consumes m̂ as a **set-point**. The measured deviation from criticality never
tunes a knob. That is observation *of* criticality, not self-organization *toward* it — exactly the
distinction the 2019–2025 literature draws.

## Concrete application — `scripts/mesh-pace`

`mesh-pace` already IS a homeostat: its `eff_gap` **shrinks** the dispatch gap when paid burn is cold
and **stretches** it when burn is hot (`burn_mult`, cold-shrink/hot-stretch) — but it keys on ONE
signal, the **budget** (paid burn/h). Add a SECOND homeostatic term keyed on the **coordination
criticality** m̂ (set-point σ\*≈1), read from `mesh-criticality --json`:

- **m̂ supercritical** (cascade building) → **stretch** the gap (throttle concurrent releases): damp
  the cascade *before* it floods the board. This is an *action* on the early-warning that today only
  produces an `[alert]`.
- **m̂ subcritical WHILE work is pending** → **shrink** the gap (release queued work faster): pull
  coordination back up toward criticality.
- **Compose as the MORE CONSERVATIVE of the two** (`eff_gap = max(burn_gap, crit_gap)`): the reserve
  protection (hot-stretch) can never be overridden by a criticality-shrink — budget safety dominates,
  so this cannot become a spend-bypass.

**Doctrine guard (why this is safe, not a pace-bypass):** the criticality-shrink modulates only the
**release rate of REAL, already-pending work**; with an empty queue a subcritical m̂ triggers
*nothing*. It never mints activity. This is the load-bearing distinction — see the discard below.

Suggested shape (advisory first): land it as `mesh-pace --crit-gap` (a read-only computed gap that
folds m̂ in) so the actuation can be observed against the live budget homeostat before it is wired
into the default `eff_gap` — the same "prove the sidecar before you trust the loop" discipline
`mesh-criticality`'s own read-only sidecars already follow.

## Discarded alternative (considered, rejected in one line, because it is tempting)

The *freshest* 2025 hit — *Emergent functions of noise-driven spontaneous activity: homeostatic
maintenance of criticality and memory consolidation* (Front. Neural Circuits 2025,
https://www.frontiersin.org/articles/10.3389/fncir.2025.1585087/full) — proposes injecting
**spontaneous noise activity during quiescence** to hold σ≈1. **Rejected:** that is precisely the
self-minted idle heartbeat mesh doctrine forbids ("cron minds think vacuously"; "a self-scheduled
wakeup mints paid turns off-ledger — the pace-bypass"). The mesh *correctly* lets coordination go
subcritical when idle (dormancy IS the right state with no work) and re-excites on real events — so
the loop must close on **rate-modulation of real work**, never spontaneous injection.
