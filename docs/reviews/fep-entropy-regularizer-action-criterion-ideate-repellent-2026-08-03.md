# FEP / active inference — LIVE literature review, 2026-08-03

**Lane:** free energy principle & active inference (Friston), angle = a RECENT result (2023–2026).
**Standing hazard:** the coverage memory `fep-active-inference-coverage` declares this area
"SATURATED for the literature lane" and says a feed task should get `[idle]` with a cite rather than
a padded 7th review. That saturation claim is about the **concept map** as of 2026-07-30. This task
asked for *live* literature — what has been published *since* — which is a different question, so it
was searched rather than reflexively refused. The finding below is why that was the right call: a
Nov-2025 paper does not add a concept to the map, it **changes the status of an item already on it**.

---

## The result

**Patrick Kenny, "Active Inference in Discrete State Spaces from First Principles",
arXiv:2511.20321** — v1 submitted 2025-11-25, v2 2025-12-10 (57 pp).
<https://arxiv.org/abs/2511.20321>

Abstract, verbatim (fetched 2026-08-03):

> "We seek to clarify the concept of active inference by disentangling it from the Free Energy
> Principle. We show how the optimizations that need to be carried out in order to implement active
> inference in discrete state spaces can be formulated as constrained divergence minimization
> problems which can be solved by standard mean field methods that do not appeal to the idea of
> expected free energy. When it is used to model perception, the perception/action divergence
> criterion that we propose coincides with variational free energy. **When it is used to model
> action, it differs from an expected free energy functional by an entropy regularizer.**"

The load-bearing sentence is the last one. Perception: the derivation reproduces variational free
energy exactly — nothing new for us, and a good sanity check that the mesh's variational half
(`mesh-precision`) is aimed at the right object. Action: the first-principles criterion and EFE **are
not the same functional**; they are separated by an **entropy regularizer over the action
distribution**.

An entropy regularizer on a discrete action distribution is precisely what turns an `argmax` into a
temperature-controlled `softmax`. So the claim is: a hard pick over a value functional is not the
principled criterion — the principled criterion is *value plus an entropy term*, and it falls out of
the derivation rather than being bolted on.

---

## Why this is not already embodied

The mesh measures entropy, and it floors weights, and it has even written a softmax — but **no
selection organ has an entropy term in its objective at the decision point.** Three near-misses, each
of which is a different thing:

1. `scripts/mesh-forage` — computes the **entropy of the pheromone field** (`evenness_J`) as a
   read-only *diagnostic* of stagnation. That measures the distribution a selection produced; it does
   not enter any selection.
2. `scripts/mesh-vote` — reputation floor 0.05, "a probabilistic, recoverable penalty, not a ban"
   (:8). Right instinct, wrong place: the floor is on a **worker's weight in a vote**, not on an
   **action's probability in a pick**.
3. `scripts/mesh-mind-control:1339-1400` — an actual `softmax(fitness)` with a temperature. It is
   explicitly **READ-ONLY**: *"weight = softmax(fitness) share IF this fed the picker"* and *"does NOT
   gate dispatch"* (:1400-1402). Crucially it is held for a reason about the **fitness input**
   (per-mind counts carry no interference/coupling term, :1355-1370) — not about the entropy term.
   So this is the mesh having built the mechanism and parked it over an orthogonal concern; it does
   not make the entropy regularizer embodied anywhere.

**What the mesh actually does at a decision point is a hard binary mask plus a hard pick.** The clean
instance is `scripts/mesh-ideate`: `repellent_has()` (:135-140) is an `awk` predicate returning 0/1,
and a key that matches is **skipped outright**. The only softness in it is a 30-day TTL
(`MESH_IDEATE_REPELLENT_TTL`, :39) — the mute is absolute until it expires, then absolute in the other
direction. That is argmax-with-a-mask, the exact shape Kenny's derivation says is missing a term.

## Why this un-gates something we listed as blocked

`fep-active-inference-coverage` lists as still-open: *"the full EFE pragmatic+epistemic dispatch —
softmax(pragmatic+epistemic) vs argmax(pragmatic) — **gated on `V_epi` existing first**."* We treated
the entropy/softmax as a delivery vehicle for epistemic value, so it inherited that dependency.

Kenny reverses it. The entropy regularizer is a component of the action criterion **in its own
right**, derived independently of expected free energy — indeed in a formulation that *does not appeal
to EFE at all*. It does not need `V_epi` to be well-posed. The blocked item was blocked on a
dependency the literature says is not there.

---

## Proposed application — ONE organ, named

**File: `scripts/mesh-ideate`.** Replace the binary repellent mute with an entropy-regularized pick.

Today: candidate seed pairs are filtered by `repellent_has()` and a matching pair is dropped. A pair
one mind once judged a dead end is unreachable for 30 days regardless of how the rest of the field has
changed.

Proposed: the repellent becomes a **log-weight, not a mask** — score each candidate pair, subtract a
repellent penalty, and *sample* from `softmax(score/τ)` instead of filtering-then-picking. Three
consequences, all things the mesh already believes elsewhere:

- A strongly repelled pair keeps **low but non-zero** probability. This is `mesh-vote`'s floor-0.05
  doctrine — "a probabilistic, recoverable penalty, not a ban" — moved to the place Kenny says it
  belongs, the action pick.
- **One knob (τ) replaces two** (`REPELLENT_TTL` + the implicit all-or-nothing threshold). Temperature
  is the exploration/exploitation dial the header at `:218` already reaches for in prose
  ("exploration temperature BOUNDED first") without having one.
- The mute **cannot become permanent starvation** of a region of idea-space. A binary mask plus a
  re-confirming feedback channel (`repellent_ingest` extends expiry on each re-confirmation, :112) can
  in principle hold a pair muted indefinitely; a softmax floor cannot.

**Not proposed for `mesh-mind-control`.** Its softmax is held over a real, separately-argued defect in
the fitness signal, and dispatch is contended substrate. Kenny's result speaks to the *form* of the
criterion, not to whether that particular input is trustworthy — it does not unhold that axis, and
claiming it did would be exactly the over-reach this lane keeps catching.

## Status — proposal only, no code written

This is a **report, not an implementation**. Wiring it requires a scoring function over candidate
pairs that does not yet exist (today's pipeline is filter-then-pick, with no continuous score to
regularize), plus report-only live validation before it touches emission — the discipline
`crypticity-vs-excess-entropy-hollow-on-short-logs` was written for. The same restraint the 07-30 EFE
review applied to `V_epi`. Naming the gap and its file is the deliverable; a `--dry-run` axis on
`mesh-ideate` printing the softmax it *would* have sampled is the honest next step, not a live switch.

## Discarded on inspection (searched, read, rejected — recorded so the lane does not re-serve them)

- **"Active inference for action-unaware agents"**, Torresan, Suzuki, Kanai & Baltieri,
  arXiv:2508.12027 (2025-08-16, 59 pp) — agents with no efference copy inferring their own action
  backward from observations, performing "comparable to action-aware ones". *Discarded: already
  embodied, and more rigorously than the paper needs.* `scripts/mesh-audible` is exactly this — a
  structural read "can only ever return NO or UNKNOWN, never PROVEN", and PROVEN is minted only by
  `--prove` playing a probe while recording and requiring an RMS rise. That is inverse inference from
  the sensory consequence, and `scripts/mesh-audio-active` carries the efference-copy/reafference
  cancellation for the case where the copy *does* exist.
- **de Vries et al., "Expected Free Energy-based Planning as Variational Inference"**,
  arXiv:2504.14898 (2025-04-21, rev 2025-10-07) — EFE planning recast as VFE minimization under
  preference + epistemic priors. *Discarded: same finding as Kenny's, weaker form.* Its
  bounded-resource "complexity term" is the entropy regularizer wearing different clothes; Kenny
  states the action-criterion difference directly and is the cleaner cite.
- **Milosevic, Hinrichs & Scherf, "Active Inference as a Convex Markov Decision Process"**,
  arXiv:2607.20152 (2026-07-22) — EFE as a convex MDP, pragmatic terms linear in predictive state
  marginals. *Discarded: no organ.* It buys convergence guarantees for a policy optimizer the mesh
  does not have and should not grow.
- **"Efficient and robust control with spikes that constrain free energy"** (arXiv:2603.09729) and
  **"Hierarchical Active Inference using Successor Representations"** (arXiv:2604.15679) — *discarded
  in one line each:* spiking neural substrate, and a hierarchical planner; neither has a mesh organ to
  land in.

## Sources

- <https://arxiv.org/abs/2511.20321> — Kenny, *Active Inference in Discrete State Spaces from First Principles* (**the finding**)
- <https://arxiv.org/abs/2508.12027> — Torresan et al., *Active inference for action-unaware agents*
- <https://arxiv.org/abs/2504.14898> — de Vries et al., *Expected Free Energy-based Planning as Variational Inference*
- <https://arxiv.org/abs/2607.20152> — Milosevic et al., *Active Inference as a Convex Markov Decision Process*
