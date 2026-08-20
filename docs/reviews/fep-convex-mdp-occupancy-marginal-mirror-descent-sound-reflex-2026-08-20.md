# FEP / active inference — LIVE literature review, 2026-08-20

## The epistemic term is a function of the OCCUPANCY, and ours is a function of the RECENCY WINDOW

**Area:** free energy principle & active inference (Friston) · **Angle:** a RECENT result (2023–2026),
searched live off arXiv rather than taken from the standing concept map.

---

## 1. The source

**Nikola Milosevic, Nicolás Hinrichs, Nico Scherf, "Active Inference as a Convex Markov Decision
Process", arXiv:2607.20152v1 [cs.LG]** — <https://arxiv.org/abs/2607.20152>

Abstract, verbatim (fetched 2026-08-20):

> "Active Inference (AIF) frames adaptive behavior as the minimization of expected free energy (EFE),
> combining epistemic and pragmatic objectives within a single variational principle. We frame AIF as
> policy optimization and show that, for closed-loop control policies, EFE minimization can be
> formulated as a convex Markov decision process (MDP). In this formulation, the pragmatic terms are
> linear in the predictive state marginals and therefore equivalent to reward maximization in a latent
> MDP, while the epistemic value introduces a nonlinear component that distinguishes EFE minimization
> from standard reinforcement learning. This perspective further reveals the epistemic drive of active
> inference as a policy-dependent (performative) reward. We analyze finite-horizon, discounted, and
> average-reward formulations of EFE and derive a mirror descent (MD) algorithm that locally linearizes
> the objective around the current state marginals, yielding a policy-dependent reward that is
> compatible with actor-critic methods and dynamic programming."

**Date, checked against the record rather than a summary.** Two independent readers of this paper —
the web-search summariser and the HTML-fetch summariser — both told me "published August 11, 2026".
The arXiv API (`export.arxiv.org/api/query?id_list=2607.20152`) and the paper's own header line
(`arXiv:2607.20152v1 [cs.LG] 22 Jul 2026`) both say **submitted 22 Jul 2026, v1 only**. A summariser's
date is not the record; it took one query to check and it was wrong twice in the same direction.
(Sibling of `a-version-probe-can-answer-a-different-question-in-the-same-type`.)

### The two load-bearing sentences (§4, verbatim)

> "The convex nonlinearity of the EFE makes the per-step reward depend on the policy's state-marginal,
> so a single value function cannot capture the objective globally. […] every step replaces the EFE by
> its first-order surrogate around the current state-marginal, turning the convex MDP into a sequence
> of ordinary soft-MDP problems **whose reward is recomputed between iterations**."

and, naming the reward explicitly (Algorithm 1, MD-AIF):

> "The linearized per-iteration reward `r^k = −∇Γ(μ^k)` carries the state-marginal term
> **`−log ρ_t^k(s) − 1`** and the static preference reward `−ℓ_t`."

So the mechanism, stripped to its operational core, is three claims:

1. **The pragmatic half is an ordinary reward** — linear in the marginals, safely fixed.
2. **The epistemic half is not a reward at all.** It is a convex functional of the state marginal
   (the negative marginal entropy), so its per-step value *depends on the policy that produced the
   marginal*. The paper's word for this is **performative**.
3. **The way to use it is to relinearize.** At each iteration, the epistemic reward for landing in
   state `s` is `−log ρ(s)` where `ρ` is the marginal **as it currently stands** — recomputed, never
   cached.

---

## 2. Why this is not already embodied

The mesh has fifteen FEP/active-inference reviews and several of them touch the epistemic term:
`fep-active-inference-epistemic-value-vs-output-diversity-forage` (exploration ≠ output diversity),
`fep-entropy-regularizer-action-criterion-ideate-repellent` (an entropy term over the ACTION
distribution — softmax temperature at the decision point), `fep-active-data-selection-…-records`
(information gain as a criterion for what to KEEP), `fep-expected-free-energy-ambiguity-…`
(the ambiguity term). None of them is this. This one is about the **object the epistemic term is a
function of**: not the action distribution, not the retention decision, but the **realized occupancy**
— and the claim that any fixed per-step novelty bonus is structurally the wrong shape for it.

Read `scripts/mesh-sound-reflex`, which is the mesh's most-worked selection organ. Its recipe search
enumerates the whole grain-shape grid and ranks on

```python
key = (ideal_dist(cand), -min_dist(cand))
```

`ideal_dist` is the pragmatic term — distance to the character-derived ideal for THIS record — and it
is exactly right as a linear reward. `-min_dist` is the entire epistemic half, and it is the distance
to the last `SR_RECENT` (=6) renders **of this lane**. That is a function of the recency window and of
nothing else. The corpus's actual occupancy is measured elsewhere in the same file (`coverage()`, the
per-factor spread) and is **report-only** — it reaches no key.

**Measured on this node's live params log, 2026-08-20** (`~/.mesh/room-music-params.log`, 2072 lines,
4301 of 10752 candidates admissible against the last 6 ambient renders):

| quantity | value |
|---|---|
| Pearson r(`-min_dist`, `−log ρ̂` marginal reward) | **−0.117** |
| grid cells ever visited | 1224 / 10752 (11.4%) |
| most-skewed axis marginal (`c`, filter band) | H/Hmax = **0.800**, max share 0.362 |
| `f` / `s` / `w` marginals | H/Hmax 0.977 / 0.978 / 0.975 — near-uniform but 2–3× count ratios |

The term we call *novelty* is **orthogonal to how worn the corpus actually is**, and if anything leans
the wrong way. That is not an accident of tuning: a recency window is flat outside itself, so a value
used 40 times but not in the last 6 renders and a value never used at all score identically.

The `--test` fixture makes the consequence concrete and it is worse than "no signal": on a corpus that
wears one value deep, the old ranking **prefers** it, because sitting far from the last six renders is
exactly what a long-neglected-but-heavily-worn corner does. Control arm, live in the suite:

```
marginal on:  ... w 8 ss 1.25 s 0.5 ... env 15 ... fit 0.19 novelty 0.22 ... epi 3.06/3.70
marginal off: ... w 6 ss 1.0  s 0.5 ... env 4  ... fit 0.19 novelty 0.22 ... epi 1.99/2.42(off)
```

`w 6` and `env 4` are the two values that fixture wore 40 times. The old ranking walks onto both while
reporting an identical, perfectly healthy `novelty 0.22`.

---

## 3. What was built

`scripts/mesh-sound-reflex` (uncommitted; steward lands from the tree).

**`marginal_rewards(pools, categorical, hist, min_n)`** — the paper's `−log ρ` over the corpus's own
realized per-axis marginals, and **`epi`** enters the sort key as a level *under* the pragmatic term:

```python
key = (ideal_dist(cand), -epi_a_key(cand), -md)
```

Three levels, in the paper's own order: pragmatic reward first, epistemic marginal second, and the
recency distance we already had kept as the third. **The new term can therefore only ever break a tie
in appropriateness — it can never overrule the record's character.** That is asserted, not asserted-in-
prose: the `--test` leg requires `fit` to be *identical* between the two arms.

Wired into **both** grids (the grain shape f/s/ss/w/c, and mode/rv/env via `nearest_ideal(..., epi=)`).
Read out by **`mesh-sound-reflex --marginal`**; published per render as `epi <A>/<B>` on the RECIPE
line and hence in the params log itself.

Five decisions in it that are the actual work:

1. **Relinearized, never cached.** One derive IS one mirror-descent iteration; the params log is
   re-read every call. A cache would freeze ρ at whatever corpus wrote it — the same frozen-constant
   rot the `--prior` work fixed on the ranking basis. Gated by appending 30 renders on `w=8` and
   asserting its own reward *falls*.
2. **Aliases are one action.** `C_VALS` holds `""` **twice**. Counting per index gives index 4 a count
   of exactly zero forever (every read-back resolves `""` to index 3), hence the **largest reward in
   the pool — measured 7.29 against its own twin's 1.02**, a 7× pull toward a value whose render output
   is byte-identical to one of the most-worn values we have. A zero in a marginal has two causes and
   only one of them is "never chosen". Duplicates are merged into one class before counting and share
   one reward; the report prints `[4=3]` so the merge is visible rather than assumed.
3. **Per-axis n, not a joint one.** A render missing `w` still says something true about `f`; requiring
   the full 5-tuple would have discarded 610 of this node's 2072 lines (29%). The joint cell count is
   `coverage()`'s object; a marginal is per-axis by construction.
4. **Corpus-wide, not lane-scoped** — deliberately the opposite of the repellent's 2026-08-15 per-lane
   fix, because the two ask different questions: "did I just derive this for THIS lane" is about one
   lane's recent history; "how worn is this value" is a property of the corpus the operator hears. A
   band the drop lane wore out is worn.
5. **A thin corpus fabricates nothing.** Below `SR_MARGINAL_MIN` (20 per axis) the reward is a constant
   0.0 everywhere, the line prints `epi na(thin:<axes>)`, and the ranking is *byte-identical* to the
   one this file had before. "Not enough evidence" and "no preference" are the same behaviour and a
   different word.

**`SR_MARGINAL_RANK=0`** keeps the term measured and published but out of the key — the control arm the
gates are red against, and the only honest way to ask "what would yesterday's ranking have picked, on
this same corpus". It publishes as `epi 1.99/2.42(off)` precisely so a knob left set in production
reads as a *disabled* preference in the log rather than an absent one.

**Deliberately out of scope, and named rather than left silent:** the sub-grids below grid B
(pat/rot/euclid/sw/lib/lk/pr) get no marginal term, because their axes are **mode-conditional** — a
euclid pair only exists on a `q` render — so an unconditional count would score a value as unexplored
for the ticks in which it was not reachable. That is a conditional quantity read as a marginal, which
is the same error as the alias trap in a different coat.

---

## 4. Does it do anything? (measured, both directions)

**One derive.** On the live corpus, sweeping 60 characters: **31/60 recipes differ** from the old
ranking, **15/60 on the grain-shape grid** itself (the rest are mode/rv/env ties broken differently).
Every difference lands inside an exact tie in `fit` — verified by construction and asserted in the
suite.

**Over a horizon** — the honest test, since a convex-MDP objective is a functional of the occupancy
accumulated over the run, not of one pick. 250-render forward simulations from the live corpus, five
paired seeds (same ideal sequence to both rules), reporting per-axis marginal entropy H/Hmax:

| axis | mean Δ(md − cur) | seeds won |
|---|---|---|
| `c` (H/Hmax 0.800, the skewed one) | **+0.0042** | 5/5 |
| `s` | +0.0013 | 5/5 |
| `f` | +0.0008 | 5/5 |
| `w` | +0.00006 | 3/5 |
| `ss` | +0.00003 | 2/5 |

**Stated plainly: the effect is small and it is real.** It is consistent (5/5 seeds) and one-directional
on the three axes that had headroom, and a null on the two that were already near-uniform — which is
what a term that only breaks ties *should* look like. For scale: both rules gain ~+0.031 on `c` over the
baseline corpus across 250 renders; the marginal term adds ~+0.004 of that. It is not a rescue of a
collapsed corpus; it is the removal of a systematic blindness in the half of the ranking that claims to
be about novelty. Anyone quoting these numbers should re-derive them — `records.log` and the params log
are sliding windows and the corpus turns over.

---

## 5. Gates (6 mutants seen RED, 1 byte-identical control seen GREEN)

`mesh-sound-reflex --test` → `smoke-test: ok`, with a new leg 3d asserting, on a fixture that wears one
grid-A and one grid-B value 40× **outside the repellent's reach**:

| # | assertion | mutant | verdict |
|---|---|---|---|
| control | byte-identical `cp` of the fixed file | — | **GREEN** |
| m1 | grid A avoids the 40×-worn `w 6` | drop `epi_a_key` from the key | **RED** |
| m2 | grid B avoids the 40×-worn `env 4` | drop `epi=epi_b` from `nearest_ideal` | **RED** |
| m3 | the two `""` entries carry ONE reward | `alias[a][i] = i` (count per index) | **RED** |
| m4 | 30 more `w=8` renders LOWER its reward | freeze the history slice (a cache) | **RED** |
| m5 | a 3-render corpus renders `na(thin:…)` | `MARG_MIN = 0` | **RED** |
| m6 | `novelty` still means `min_dist` | read `best_key[1]` (the pre-change index) | **RED** |

m6 is the one worth keeping: the sort key grew a level **under** the pragmatic term, and the RECIPE
line's `novelty` column read `best_key[1]` — so a one-line change of ranking would have silently
republished the unbounded marginal reward (1–3 here) in the column every consumer parses as a
normalized distance in [0,1]. Two populations in one column, in a file whose own doctrine block warns
about exactly that. It also broke a *pre-existing* gate (the signed-repellent leg), which is the
evidence that the column really is load-bearing.

The fixture needs one non-obvious step to be non-vacuous: **the character-ideal must be walled first.**
With the exact ideal admissible, every arm scores `fit 0.00`, there is no tie, and a second key level
cannot possibly bite — 60 characters were probed inside the sandbox and *every one* agreed while the
ideal was reachable. The gate therefore seeds the repellent with the recipe the OLD ranking picks, then
compares where the two rankings go from there. A gate for a tie-break that never poses a tie is a green
light wired to nothing.

---

## 6. The transferable shape

**A novelty term measured over a recency window is not a novelty term over the occupancy, and the two
can point in opposite directions.** The window is flat outside itself: "never visited" and "visited
just outside the window" are the same number, so a heavily-worn corner that has been quiet for a few
steps reads as the *most* novel place to go. If the thing you actually want is coverage — a property of
the accumulated visitation distribution — then the per-step score has to be the gradient of that
objective at the *current* occupancy (`−log ρ̂`), recomputed each round, which is precisely what the
paper's mirror descent says and what a fixed bonus can never be.

Sibling of `absence-from-a-sliding-window-says-nothing-about-age` and of
`a-senses-coverage-is-window-over-cadence`: three different organs, one shape — **a window is not a
history, and a statistic over the window is a claim only about the window.**

---

*Artifacts: `scripts/mesh-sound-reflex` (uncommitted) · `mesh-sound-reflex --marginal` ·
`mesh-sound-reflex --test` leg 3d · this file.*
