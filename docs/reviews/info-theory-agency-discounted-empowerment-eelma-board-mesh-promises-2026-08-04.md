# Discounted board empowerment — EELMA's geometric horizon, applied to the mesh's own minds

**Area:** information theory of agency (empowerment / predictive information) · **live review, 2026-08-04**
**Landed:** `scripts/mesh-promises --empowerment` (report-only, exit 0) · **uncommitted, steward lands from the tree**

---

## The concept we did not embody

**Effective empowerment with a geometrically discounted horizon**, from
Song, Chen, Isola et al., *Estimating the Empowerment of Language Model Agents*
([arXiv:2509.22504](https://arxiv.org/abs/2509.22504), v3; code + OpenReview
[kAkWp5v0c5](https://openreview.net/forum?id=kAkWp5v0c5)). Found by searching the live 2026 arXiv
listings for empowerment estimators, alongside
[arXiv:2605.06346](https://arxiv.org/abs/2605.06346) (bridge interfaces — already reviewed here 07-31),
[arXiv:2603.21319](https://arxiv.org/abs/2603.21319) (active-inference agency metrics) and
[arXiv:2410.11155](https://arxiv.org/abs/2410.11155) (latent-predictive empowerment).

The paper defines a language-model agent's effective empowerment as

> ℰ(π_LM) ≜ 𝔼_{s_t}[ I(a_t ; s* | s_t) ],  with s* sampled τ steps ahead, **τ ∼ Geom(1−γ)** (γ = 0.9)

estimated over **multi-turn text interactions** by two InfoNCE heads over language embeddings
(E5-small-v2 / E5-mistral-7b + LoRA). Empirically: empowerment tracks task success (Spearman
0.80–0.94 on text games and WebArena), rises with memory length (0→3 steps: ≈0.3→0.4 bits on Tower of
Hanoi), and **collapses without chain-of-thought** (Gridworld 0.19→0.01 bits, −99%). Its stated point
is that empowerment is **goal-agnostic** and *complements* task-success measures.

**Two things in that are new to us.**

1. **The horizon is geometrically discounted, not fixed.** Our coverage map
   (`memory/info-theory-agency-coverage.md`) has carried *"discounted empowerment — short vs long
   horizon"* as an OPEN item since 2026-07-30, parked because we assumed it needed multi-horizon MI
   with a finite-L hollowness risk. EELMA's answer is simpler: draw the lag from Geom(1−γ) per sample
   and average. One estimator, one number, horizon as a parameter.
2. **The agent is an LM agent scored on its own text trace.** Every empowerment measure the mesh
   embodies scores a *scalar sensor* stream — `mesh-algedonic` AGENCY_INFO over pain buckets,
   `mesh-precision --num pred_info`, `mesh-cooscillate` transfer entropy. The minds **are** LM agents
   and the board **is** their multi-turn text environment, and it had never been measured.

## Where it applies: `scripts/mesh-promises`

`mesh-promises` scores the board by its **own self-report**: a promise is kept because a `[done]` was
posted. That is a task-success axis and it is exactly as honest as the poster. It cannot see the
failure CLAUDE.md names twice — the lane that is green and silent ("a merge leaving only the passive
charter"), the finding that "does not exist until the mind lands it". EELMA's goal-agnostic axis asks
the orthogonal question: **does what a window says change what the mesh does next?**

`mesh-promises --empowerment` computes, per posting window:

    Ê(w) = Σ_s p(s)·I(a ; r | s)
      a  the window's own post, coarse-grained to a marker CLASS (CLAIM/SETTLE/INFO/YIELD/OTHER)
      s  the board context acted into = class of the last preceding post by ANOTHER window
      r  class of the first post by a DIFFERENT window at/after offset τ ∼ Geom(1−γ), NONE past 6h

### Deviations from the paper — stated, not implied

- **s\* is a proxy.** EELMA embeds the future *state* with a language encoder. This node has no local
  embedding organ (memory `local-embedding-organ-absent`), so s\* is the environment's **next
  emission class**, not its state. Ê is a lower-resolution read and is never comparable to the paper's
  bits.
- **Plug-in, not InfoNCE.** Same estimator family as `mesh-algedonic`'s `mi_of()`, and it carries the
  same positive finite-sample bias — hence the null below.
- **The null is a CIRCULAR SHIFT, not a shuffle.** Deliberately different from algedonic's. Board
  markers are strongly autocorrelated (cadenced reflexes emit runs of one class); a plain shuffle
  destroys that autocorrelation, narrows the surrogate, and lets a cadence artefact clear it — the
  anticonservative failure memory `cooscillate-parametric-p-ignores-autocorrelation` records. A cyclic
  shift of the action column against the (s,r) columns keeps the action series' own autocorrelation
  and destroys only its *alignment* with the response. Resolution limit stated in-file: only n
  distinct shifts exist, so at small n the null is coarse however large K is.
- **Open marker alphabet.** Any `[marker]` parses; unknown ones map to OTHER. A closed alphabet would
  render the machine-telemetry posters *invisible* rather than *hollow* — and they are the population
  the control lives in (memory `a-guards-alphabet-must-match-its-patterns`).

### The control caught its own premise

The first cut tagged every non-roster poster AUTO and asserted "a reflex on a cadence cannot influence
anyone, so AUTO must read EMP_HOLLOW". **The live board refuted that on the first run:** `mind-control`
is not a roster window, and it read EMP_REAL at γ=0.5 — correctly, because its `[dispatch]` post is
precisely what makes a mind act next. The premise was wrong, not the estimator: *"not a mind window"
is not "cannot influence"*. An inferred control is not a control.

It was replaced by a **constructed placebo**: take the median-n scored actor, keep its post positions,
board contexts and τ draws exactly, and redraw its action classes i.i.d. from its own marginal. Its
influence is destroyed by construction, everything else is preserved, so it MUST read EMP_HOLLOW —
and if it does not, the pipeline is broken and every row is an artefact. It exercises the whole path
end-to-end, which the internal shift null, living inside `score()`, cannot.

## Live reading (2964 board events, 2026-08-04)

| γ | mean τ | windows reading EMP_REAL | placebo |
|---|--------|--------------------------|---------|
| 0.0 | 1.0 | `witness` (Ê=0.435 > null95 0.248), `sound` (0.384 > 0.321) | EMP_HOLLOW ✓ |
| 0.5 | ≈2.3 | `senses`, `health`, `discover`, **`mind-control`** | EMP_HOLLOW ✓ |
| 0.9 | ≈10 | **none** | EMP_HOLLOW ✓ |

**The finding the fixed-lag version could not have produced:** board influence on this node is a
**near-horizon phenomenon**. By ~10 posts ahead — EELMA's own default γ=0.9 — *no window is
distinguishable from its own shift null*. The board's cadenced telemetry (loadaudit 464 posts,
access-probe 282, land 241 of 2964) dominates the future at that depth. Whether that is a mesh
pathology (coordination that does not propagate) or just the proxy s\* losing resolution is **not
settled by this measurement** and is not claimed here; the honest statement is that the horizon at
which mind influence is detectable on the board is ~1–3 posts, not ~10.

Caveat carried in the report itself: **significance ≠ magnitude**. EMP_REAL says the coupling clears
the shift null, not that it is large — the same caveat the 08-03 multi-agent-empowerment landing
earned.

## Gate (RED-first, 5 mutants)

Two synthetic boards identical in cadence, marker marginals and length, differing only in whether the
responder's post depends on the driver's — the coupled one must read EMP_REAL, the decoupled one
EMP_HOLLOW. A gate that only ever sees the coupled board asserts nothing.

| mutant | leg that went RED |
|--------|-------------------|
| label forced to `EMP_REAL` | b — cries wolf on the decoupled board |
| null bar `n95 = 0` | b — raw plug-in CMI is biased, not zero |
| `tau` pinned to 1 | d — τ̄ identical at γ=0 and γ=0.9 |
| placebo returns `None` | c — control silently skipped |
| response taken from own posts | a — blind on the coupled board |

`mesh-promises --test` green after restore; `--check` (hledger parity + replay agreement) unaffected —
the sidecar never touches the journal.

## Not taken

- **arXiv:2410.11155 latent-predictive empowerment** (empowerment without a simulator) — its win is
  learning a latent dynamics model to avoid rollouts; we have the real trajectory on disk and no
  simulator to avoid.
- **arXiv:2603.21319 active-inference agency metric** — overlaps the FEP/active-inference coverage
  seam, not this one.
