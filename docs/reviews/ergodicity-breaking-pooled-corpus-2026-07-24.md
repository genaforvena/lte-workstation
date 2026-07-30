# LITERATURE review — the ergodicity assumption hidden in "rank against the live corpus" (2026-07-24)

**Area:** complex adaptive systems / edge of chaos (Santa Fe lineage), entered from the angle of a
**foundational idea we applied too loosely**.
**Reviewer:** genome mind · live web search + read of the primary source
**Verdict:** LAND — one un-embodied concept, one shipped (uncommitted) application with a red-then-green gate

---

## The idea, and where it is being published now

The Santa Fe "edge of chaos" strand is usually carried in the mesh as *criticality of a control law*
— we already have the measurement strand (`mesh-stress` allostatic load, branching-ratio thinking)
and the actuated-set-point strand (`docs/reviews/soc-homeostatic-setpoint-2026-07-24.md`). The live
literature has moved the order parameter. The current statement:

> **Self-Organization to the Edge of Ergodicity Breaking in a Complex Adaptive System**
> Nixie Sapphira Lesmana, Ling Feng, Kan Chen, Choy Heng Lai — arXiv:2604.15669, submitted
> 17 April 2026. <https://arxiv.org/abs/2604.15669>
>
> "…this coupled dynamics drives the system to a critical state residing on the transition boundary
> between ergodic and non-ergodic phases… providing a mechanistic link between the statistical
> physics of ergodicity breaking and the functional optimality of complex adaptive systems."

Their order parameter is not a Lyapunov exponent and not a branching ratio. It is an **ergodicity
coefficient**, defined in the paper as a median pairwise total-variation distance between the
distributions produced by independent runs:

> ε(λ) := median<sub>μ,ν∈Ω<sub>λ</sub></sub> ‖μ − ν‖<sub>TV</sub>

0 = the runs are one population; 1 = they are disjoint populations. The neighbouring literature
makes the same point in plainer language: in a non-ergodic system the **time average of one
trajectory is not the ensemble average of the population**, so a population statistic is not a
statement about any individual (Peters' line of work; see also the ergodicity-breaking parameter used
in single-particle tracking, e.g. arXiv:2603.22989, "Genuine and spurious (non-)ergodicity in single
particle tracking").

## What we do NOT embody

We embody criticality *of dynamics*. We do not embody **ergodicity as a property of the corpus a
statistic is computed over** — the question "is this pooled distribution a legitimate stand-in for
the distribution this particular sample was drawn from?"

Where this bites is not abstract. `scripts/mesh-sound-reflex`'s `corpus_pct()` ranks a new record's
five measured axes against the pooled `~/.mesh/records.log` ledger, and its docstring — promoted into
CLAUDE.md doctrine — says:

> "Rank against the live corpus: self-calibrating, **cannot saturate**."

That is an *ergodic claim stated as a structural one*. It holds if the ledger is one population. The
ledger is a **mixture of organs** (`drop` = operator drops, `scape` = the room's own ear, `ear`,
`note3`…) whose axis distributions are not the same distribution — and, worse, `records.log` is a
per-organ **sliding window pruned every sweep**, so the mixing proportions are not even stationary.
Under a mixture the pooled rank saturates in exactly the way the docstring denies: every record of
the minority organ lands in the same corner of the pooled CDF, and `pick()` returns a **constant**
for that organ regardless of what the record actually sounds like.

This is the same family as the constants the docstring already catalogues (`tone` whose median ==
max, `act > 0.55` that can never fire) — one level up. Those were *scale* errors, caught. This is a
*mixture* error, uncaught, and the fix for the scale error (rank instead of threshold) is precisely
what hid it.

## Measured on the LIVE ledger, not argued

`~/.mesh/records.log`, 2026-07-24, n=30 usable rows, organs `drop`=27 / `scape`=3. ε̂ per axis
(rank form, below), and where the three `scape` records land:

| axis | ε̂ | scape pct in the POOLED corpus | scape pct in its OWN corpus |
|------|-----|-------------------------------|------------------------------|
| dyn  | 0.284 | 0.93 / 0.90 / 0.00 | 0.67 / 0.33 / 0.00 |
| act  | **0.988** | 0.07 / 0.03 / 0.00 | 0.67 / 0.33 / 0.00 |
| rich | 0.235 | 0.77 / 0.67 / 0.33 | 0.67 / 0.33 / 0.00 |
| move | **1.000** | 0.03 / 0.07 / 0.00 | 0.33 / 0.67 / 0.00 |
| cent | **1.000** | 0.03 / 0.07 / 0.00 | 0.33 / 0.67 / 0.00 |

On `move` and `cent`, **every** `scape` record ranks below **every** `drop` record. Under
exchangeability that ordering has probability 1/C(30,3) = 2.5×10⁻⁴, so this is not a small-n
coincidence — though n(scape)=3 is small and the *magnitude* of the effect is not pinned by it.

The consequence, in the grinder's own units: `pick(W_VALS, p_move)` and `pick(C_VALS, p_cent)` both
took index 0 for all three records. **Two of the five recipe axes were dead constants for the whole
room-ear organ** — while the same three records spread 0.00/0.33/0.67 against their own history, so
the discriminating information existed and the pooled rank destroyed it.

Note what this means for a symptom we already had a detector for: `mesh-sound-reflex`'s
`starve_check` posted *"the lane is eating ONE organ… the MATERIAL is the problem"* at 19:50Z the
same day. The starve detector sees the symptom and blames intake. ε̂ names a mechanism the ranker
itself contributes.

## The application (shipped, uncommitted)

**File: `scripts/mesh-sound-reflex`** (genome source; not the deployed copy).

1. **The ledger read is now keyed by organ.** It could not notice it was pooling two populations
   while it discarded which population each sample came from.
2. **`eps_hat(axis)`** — median pairwise separation between organ sub-corpora. Estimator changed
   from the paper's binned TV to **|2·AUC−1|** (the rank form): our data is 1-D and our sub-corpora
   are single-digit n, where binned TV between two empirical distributions is biased hard toward 1 by
   sparsity alone and would call every axis a mixture. |2·AUC−1| is unbiased under exchangeability
   and *is* the quantity that breaks pooling — at 1.0 each organ occupies a fixed sub-range of the
   pooled CDF. Fewer than two organs clear the group minimum → returns **None = UNKNOWN**, not 0;
   the caller keeps pooling and `--ergodicity` prints `n/a` rather than a fabricated number.
3. **`corpus_pct` switches estimator on ε̂**, per axis:
   - ε̂ < `SR_ERG_EPS` (0.60) → **pooled**, unchanged. One population: pooling is the *better*
     estimator (more samples, less noise) and the correction must not fire.
   - ε̂ ≥ threshold and the record's own organ has ≥ `SR_ERG_OWN_MIN` (6) samples → rank **within
     its own organ** — the time average, which is what the literature says is the right object once
     ergodicity breaks.
   - ε̂ ≥ threshold but the own organ is too thin → **stratified** (equal-weight mean of within-organ
     ranks). Does not recover the record's own regime, but removes the dependence on the mixing
     proportions — the part that made the rank a function of *which organ was chatty*. Marked, never
     silent.
4. **`mesh-sound-reflex --ergodicity`** (and a block in `--status`) prints the per-axis ε̂, the organ
   ns, and which estimator answered — so the "cannot saturate" claim is re-derivable from the live
   ledger instead of asserted in a docstring. Same code path as a real derive: one implementation,
   not a second reader that can rot apart from it.

Live effect on the three real `scape` records (same repellent history both legs):

```
pooled     : w 4 c 80,15000 · w 4 c 80,15000 · w 4 c 80,15000     ← constant, whole organ
corrected  : w 4 c 300,12000 · w 5 (no band) · w 4 c 80,15000
```

**Gate (`--test` §2d), seen RED before green.** A synthetic two-organ ledger, disjoint on `move`,
identical on the other axes. Three assertions: ε̂ ≥ 0.9 on the mixed axis; the overlapping axis stays
on **pool** (a correction that fires on an ergodic axis is just a noisier ranker); and the quiet
organ's min and max records get the **same** `w` under pooled ranking and **different** `w` under the
correction. The first run went red honestly — and it caught a real bug in the test's own OFF leg:
`SR_ERG_EPS=9` as a command prefix in front of an in-process function call rebinds nothing (the
tunable is bound once at load time), so both legs had been running corrected and agreeing trivially.
That is the `export ≠ rebind a load-time global` scar, re-earned.

## What this review does NOT claim

The paper's result is that adaptive systems *self-organize toward* the ergodic/non-ergodic boundary
and are functionally optimal there. **We have taken only the measurement half** — ε as a diagnostic
that a pooled statistic is invalid — and none of the control half. Nothing here drives the sound lane
toward the edge of ergodicity breaking, and no claim is made that it should. Saying otherwise would
be exactly the loose application this review was sent to find.

The generalization is left flagged, not shipped: any mesh tool that computes a percentile/median over
a pooled log whose rows come from heterogeneous producers has the same exposure. `mesh-stress` is
already safe (it calibrates against *this node's own* curve — the time average, arrived at
independently). Others under `mesh-tools` that pool across producers have not been audited.

## Sources

- [Self-Organization to the Edge of Ergodicity Breaking in a Complex Adaptive System — arXiv:2604.15669](https://arxiv.org/abs/2604.15669)
- [Genuine and spurious (non-)ergodicity in single particle tracking — arXiv:2603.22989](https://arxiv.org/html/2603.22989v2)
- [Ergodicity Breaking in Geometric Brownian Motion — Phys. Rev. Lett. 110, 100603](https://link.aps.org/doi/10.1103/PhysRevLett.110.100603)
- [Robustness of biomolecular networks suggests functional modules far from the edge of chaos — bioRxiv](https://www.biorxiv.org/content/10.1101/2023.06.30.547297.full.pdf)
