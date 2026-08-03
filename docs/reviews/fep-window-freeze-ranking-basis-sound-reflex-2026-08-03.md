# FEP / active inference — LIVE literature review, 2026-08-03 (second pass)

**Lane:** free energy principle & active inference (Friston), angle = an **operational mechanism**
we could implement, not philosophy.
**Standing hazard:** `fep-active-inference-coverage` says the *concept map* is saturated. That is a
claim about a fixed list; this task asks what is being *published*. Searched, not refused — same
call as the 2026-08-03 first pass, and it landed again.

---

## The result

**Alireza Furutanpey, Schahram Dustdar, "Principled Direction-Free Intrinsic Motivation through
Model-Free Epistemic Free-Energy Estimators", arXiv:2607.16858** — cs.LG, submitted 18 Jul 2026.
<https://arxiv.org/abs/2607.16858>

Abstract, verbatim (fetched 2026-08-03):

> Across environments with mixed sources of uncertainty, unsupervised reinforcement learning
> requires intrinsic motivation that does not precommit to a particular direction of surprise.
> Surprise minimization is scoped by design to "unstable" environments. Prediction-error curiosity
> rewards total expected surprise, including irreducible noise. Bandit or mixture switching between
> surprise-minimizing and surprise-maximizing rewards reintroduces non-stationarity by construction.
> We propose a single intrinsic reward, stationary within each window, derived from the novelty
> contribution of a preference-free Expected Free Energy objective, expressed in reward-maximization
> form. Our claim is that parameter information gain, the expected surprise of the next state minus
> its irreducible part, is the appropriate intrinsic signal in both high-entropy and low-entropy
> components of the state space. Maximizing it seeks exactly the surprise the model can explain
> away. In regions of unresolved dynamics, this epistemic term drives exploration. As dynamics
> become resolved, the epistemic term vanishes, while an aleatoric penalty favors lower-variance
> transitions, all without fitting an explicit next-state predictor. A pseudocount supplies
> epistemic value, a probe-based penalty captures aleatoric variance, and a short-horizon gate
> protects informative successors. A window-based freeze of all reward-defining objects yields a
> stationary Bellman operator, explicit bounds on learning targets, and a conditional
> uniform-concentration result for the nonparametric estimators under mixing, smoothness,
> bandwidth, and capacity assumptions. In active-inference terms, the agent is preference-free where
> novelty is retained, standard likelihood ambiguity vanishes under full observability, a nonstandard
> transition-entropy penalty is added, and surprise minimization emerges in resolved regions of the
> state space.

Also verbatim from the paper (fetched 2026-08-03): *"Within a window all reward-defining objects are
frozen: target heads, calibration, baseline, policy, hyperparameters λ,α,τ,h_g,β,σ₀ — all statistics
under stop-gradient."* And on the method's scope: *"model-free in the restricted sense that no
next-state predictor is fit or rolled out."*

### The mechanism we do NOT embody

Not the epistemic/aleatoric split — `mesh-novelty --progress` (Schmidhuber compression progress)
already separates LEARNING from NOISE from MASTERED, and `mesh-novelty --bayesian` already scores
belief-movement over rarity. **The un-embodied mechanism is the window-based freeze of the
reward-defining objects.**

It is a claim about *when the ruler is allowed to move*, and its content is: a selector whose scoring
basis is re-derived from data its own selections produce has no stationary objective, so a change in
its output is not attributable — you cannot tell "the material differed" from "the ruler moved". The
paper's remedy is neither a live basis nor a pinned constant: freeze all reward-defining objects
*within* a window, re-derive *at* the boundary.

That is directly opposed to a line of standing mesh doctrine. `CLAUDE.md` (sound studio) says
*"Rank against the live corpus: self-calibrating, cannot saturate"*, and `corpus_pct`'s docstring in
`scripts/mesh-sound-reflex` says the same. The 2026-07-24 ergodicity work (arXiv:2604.15669) fixed
**which population** to rank against — pooled vs own-organ vs stratified — and never touched **when**
that population may change. Both are non-stationarity; only one was measured.

---

## The application — `scripts/mesh-sound-reflex`

`corpus_pct(axis, v)` ranks a record's measured character against the live ledger; the percentile
indexes a fixed param pool (`act→f` grain length, `dyn→s` track speed, `rich→ss`, `move→w` window
divider, `cent→c` band). `~/.mesh/records.log` is a per-organ **sliding window**, appended and pruned
every sweep. So the ranking basis moves continuously, under records that do not.

**Landed (report-only): `mesh-sound-reflex --basis-drift`.** It re-ranks the last `K` records
(`SR_BASIS_K`, default 20) against the basis as it stood *before those K arrived* versus the basis
now, through the **same** `corpus_pct` a real derive uses (one implementation, not a second reader
that can rot apart from it — the rule `--ergodicity` already follows). It reports per axis the median
and max percentile movement and, the only number that touches behaviour, **how many records land in a
different param slot**.

Report-only is deliberate: freezing changes what gets ground. Measure first
(`[[crypticity-vs-excess-entropy-hollow-on-short-logs]]`).

### The artifact (live ledger, 446 rows, 2026-07-24 → 2026-08-03)

```
$ mesh-sound-reflex --basis-drift
BASIS window K=20  recent=20  older=426  ledger=446
BASIS act   -> f  pool=6 n=18 med|dp|=0.016 max|dp|=0.028 slot_flips=1
BASIS dyn   -> s  pool=8 n=18 med|dp|=0.004 max|dp|=0.010 slot_flips=0
BASIS rich  -> ss pool=7 n=18 med|dp|=0.004 max|dp|=0.010 slot_flips=0
BASIS move  -> w  pool=4 n=18 med|dp|=0.012 max|dp|=0.019 slot_flips=1
BASIS cent  -> c  pool=8 n=18 med|dp|=0.003 max|dp|=0.007 slot_flips=0
BASIS total slot_flips=2 over 20 records x 5 axes
```

Drift is a function of how long the window is — how much turnover the basis absorbed:

| `SR_BASIS_K` | records re-ranked | slot flips | flips / (K × 5 axes) |
|---|---|---|---|
| 20 | 20 | 2 | 2.0 % |
| 50 | 50 | 7 | 2.8 % |
| 100 | 100 | 49 | 9.8 % |
| 200 | 200 | 166 | **16.6 %** |
| 300 | 300 | 396 | **26.4 %** |

Over a ~200-record span, **one param slot in six** differs purely because the corpus turned over.

Second, independent artifact — the same fact from the other end, one **fixed unchanged record**
(`2026-07-30T18:32Z drop`, `dyn=0.399 act=0.580 move=1.000 cent=3083.7`) re-ranked against the basis
as of each day, through the **live** estimator (`strat`, which the ergodicity report shows is what
dyn/act/move/cent are actually on: `eps` 0.645/0.748/0.929/0.974 ≥ `SR_ERG_EPS` 0.60):

```
as-of            n    p_dyn    p_act   p_move   p_cent
2026-07-24      30    0.352    1.000    0.815    0.852
2026-07-27      88    0.219    0.994    0.831    0.944
2026-07-29     246    0.283    0.988    0.846    0.963
2026-08-03     429    0.319    0.959    0.829    0.961
p_dyn  span 0.133   pick()/8 -> [2,2,1,2,2,2,2,2,2]   distinct=2
p_cent span 0.111   pick()/8 -> [6,6,7,7,7,7,7,7,7]   distinct=2
```

The record never changed; its slot did. Note this survives the ergodicity correction — `strat` removes
the dependence on *which organ was chatty*, not the dependence on *when you asked*. (Honest caveat:
this second table reconstructs the historical basis as a **cumulative prefix**, whereas the real basis
was the pruned sliding window. Pruning evicts old mass, so the true basis moved *more* than shown,
not less. That table came from a one-off scratch script and is **not** the durable artifact — the
durable, re-runnable one is `--basis-drift` above.)

### The gate (`--test`, block 2f) — two legs, each the other's red

- **DRIFT** — 30 older records with `move` in 0.11–0.40, then 20 arriving in 0.61–0.80. Reports
  `move med|dp|=0.220 max|dp|=0.400 slot_flips=8` of 20. Asserts `> 0`.
- **STABLE** — 30 older + 20 recent with the **identical empirical distribution** (10 values, ×3 and
  ×2). Reports `slot_flips=0`. Asserts `== 0`.

Run each assertion against the other's ledger and it fails — seen both ways, not a gate nobody has
watched go red. One thing the build taught, worth keeping: the first stable fixture cycled 15 values
into 30/20 rows, which leaves unequal multiplicities between the halves; that **alone** moved `move`
by up to 0.060 and flipped 2 of 20 slots. *A control that is only approximately stationary measures
its own resampling noise* and silently raises the floor the drift leg must clear.

Full suite green: `bash scripts/mesh-sound-reflex --test` → `smoke-test: ok`, rc=0.

---

## What is NOT proposed (yet)

Actually freezing the basis. The obvious next step is `SR_BASIS_FREEZE` — snapshot `ORGAN_VALS` to
`~/.mesh/records-basis.json` at a window boundary, rank every record in the window against the
snapshot, re-derive only at the boundary. Two reasons to hold:

1. It changes what gets ground; the report above is the prior measurement that decides the window
   length, and a 20-record window costs 2 % while a 300-record one costs 26 % — the number the knob
   needs.
2. Doctrine already carries the opposite scar — *"a median pinned as a constant ROTS"* (CLAUDE.md).
   The freeze is the reconciliation of that scar with this finding (frozen *within*, re-derived *at*
   the boundary), and stating it is cheap; shipping it without the window length measured is exactly
   the pinned constant that rotted before.

## Not applicable, one line each

- **Probe-based aleatoric penalty** (random unit-sphere projections, variance across sampled
  successors) — the mesh has no next-state distribution to sample per action; `mesh-novelty
  --progress` already carries the reducible-vs-irreducible split in the form this substrate supports.
- **Short-horizon epistemic gate** (`h_g`-step lookahead under a frozen probe policy) — requires a
  rollout model; the reflex's decision is one-shot per record, no successor to protect.
- **Pseudocount epistemic value** `κγ²tanh²(1/√(N+1))` — this is the recency repellent
  (`SR_EPSILON` / last-N combo distance) in a different algebra; already embodied.

## Coverage-map delta

`fep-active-inference-coverage`: add **window-based freeze of reward-defining objects** (2607.16858)
as *measured, report-only, freeze deferred*. Do not re-serve the epistemic/aleatoric split
(`mesh-novelty --progress`), the pseudocount (repellent), or the short-horizon gate (no rollout).
