# Live-literature review — active inference: EXPECTED PRECISION γ over policies (the probe's confidence, not just its choice)

Date: 2026-07-29 · lane: genome (idea-queue LITERATURE task) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

The mesh has landed the Free Energy Principle / Active Inference (Friston) **perception** and
**epistemic-value** canon almost exhaustively:

- **precision-weighting** (inverse-variance sensor reliability) — `scripts/mesh-precision`
- **prediction-error / Shannon-surprise**, epistemic-vs-aleatoric, Bayesian surprise `KL[post‖prior]` — `scripts/mesh-novelty` (`--bayesian`)
- **Markov blanket / Pearl partition** — `scripts/mesh-perimeter`
- **good regulator / homeostatic setpoint** — `scripts/mesh-homeostasis`
- **Expected Free Energy — epistemic value**, both halves:
  - **SALIENCE** (info gain about STATES) — `scripts/mesh-interruptibility --probe` (`review-efe-epistemic-active-sensing-2026-07-04`)
  - **NOVELTY** (info gain about model PARAMETERS) — `scripts/mesh-precision` novelty axis (`efe-novelty-vs-salience-2026-07-27`)
- **pragmatic value / prior preferences / dark-room** — `scripts/mesh-needs`, `fep-dark-room-prior-preference-2026-07-27`
- **Bayesian model reduction (Occam)**, **circular inference / overcounting**, **local-global two-timescale** — the `predictive-processing-*` set.

Every landing above concerns the **value of an action** (how much a policy is expected to reduce which
uncertainty). **None concerns the CONFIDENCE with which a policy is selected** — the precision γ that
active inference places *on the policy posterior itself*. That is the gap.

## The mechanism not yet embodied — γ, EXPECTED PRECISION OVER POLICIES

In the standard active-inference scheme, a policy is chosen by a softmax over its (negative) expected
free energy: `Q(π) = σ(−γ · G(π))`. The **inverse temperature γ is not a fixed constant — it is
inferred**, and it *is* the agent's **confidence in its own plan**:

- when one policy's expected free energy clearly dominates, γ is high — the choice is **decisive**;
- when the `G(π)` landscape is **flat** (many policies roughly equal), γ collapses — the argmax is a
  near-coin-flip and the agent should *not* commit as if it were sure.

γ is a first-class, measurable quantity in the framework (it is the term identified with **phasic
dopamine / confidence** in the neural process theory). Its **peakedness of the policy posterior** is the
metric the field reads off to say "how sure is the agent that this is the right move."

The affective reading closes the loop: **Hesp, Smith, Parr, Allen, Friston & Ramstead, "Deeply Felt
Affect: The Emergence of Valence in Deep Active Inference," Neural Computation 33(2):398 (2021)** derive
**valence** as tracking exactly this expected precision — positive valence = *rising confidence that my
chosen policies are good*. So γ is simultaneously (a) a decision-confidence and (b) the seed of an
affective (valence) axis the mesh does not yet have.

### The live source (searched current, not a fixed list)

- **Friston, Rigoli, Ognibene, Mathys, FitzGerald & Pezzulo, "Active inference and epistemic value,"
  Cognitive Neuroscience 6(4):187 (2015)** — the origin of the inferred precision **γ** on the policy
  prior (confidence in policy selection; the dopaminergic term).
- **Hesp et al., "Deeply Felt Affect," Neural Computation 33(2):398 (2021)** —
  <https://direct.mit.edu/neco/article/33/2/398/95642> — valence = the (rate of change of) expected
  precision; "affective charge is positive when expected model evidence is higher under the *posterior*
  over policies than under the *prior*" (increased confidence in plans).
- **LIVE 2025 continuations (surveyed this sweep):** the eLife reviewed-preprint **92892**
  (<https://elifesciences.org/reviewed-preprints/92892>) circulates in a **risk-and-ambiguity** framing
  (v2) as well as the novelty-and-variability framing (v3) already cited in the sibling doc — the paper
  itself is *moving*, which is the point of a live review. **"Decision, Inference, and Information:
  Formal Equivalences Under Active Inference," Entropy 28(1):1 (2025-12)**
  (<https://doi.org/10.3390/e28010001>) and **"Reframing the Expected Free Energy: Four Formulations and
  a Unification" (arXiv:2402.14460)** treat the EFE decompositions (risk+ambiguity / epistemic+pragmatic)
  where γ weights the whole selection — confirming γ-on-the-policy is current, not archival.

## The gap in the mesh, measured against the tool itself

`mesh-interruptibility --probe` builds the SALIENCE ranking correctly: on a diffuse (UNKNOWN/degraded)
band it nominates the single cheapest sense whose refresh best disambiguates the band. But `_probe` is a
pure **argmax over a FIXED priority list** — it returns the first degraded axis and prints one line:

```
[interruptibility:probe] kbd — run `mesh-kbd-activity` | refresh distinguishes DND vs AVAILABLE
```

with **identical authority** whether:

- **one** load-bearing axis is diffuse (resolving it *collapses* the band — a decisive probe), or
- **several** load-bearing axes are simultaneously diffuse (the posterior is diffuse along *many*
  dimensions — resolving one is a **partial** move that leaves the band UNKNOWN), or
- only a **weak-lever** axis is diffuse (tempo/ambient/light "rarely flip a band alone" — a low-yield
  refresh).

A consumer reading "probe kbd" as *"refresh kbd and you'll know the band"* is wrong in cases 2 and 3.
This is the **max-fold-effaces-the-disjunction** failure (that memory) at the policy layer: the argmax
reports the winner but not **how alone it stands** — i.e. it drops γ.

## The fix — one file: `scripts/mesh-interruptibility` (in tree, uncommitted)

`--probe` gains a **γ / expected-precision** token: `confidence=HIGH|LOW`, computed inside the pure,
offline-testable `_probe` from the count of simultaneously-diffuse **load-bearing** axes
(`lb_deg = kbd+room+awake+screen`; tempo/ambient/light are weak levers by the tool's own comment):

```
confidence=HIGH γ — decisive: the ONLY load-bearing axis diffuse; resolving it collapses the band
confidence=LOW  γ — N load-bearing axes diffuse; one refresh is a PARTIAL move (batch-probe or wait)
confidence=LOW  γ — only weak-lever axes diffuse; a refresh rarely flips the band alone
```

Live now (two load-bearing axes diffuse — kbd+room):

```
[interruptibility:probe] kbd — run `mesh-kbd-activity` | … · confidence=LOW γ (2 load-bearing axes
   diffuse — one refresh is a PARTIAL move (band won't fully collapse; batch-probe or wait, don't
   treat as a fix))
```

**Report-only / advisory** — γ never changes *which* sense is nominated or auto-dispatches anything; it
annotates the recommendation with how decisive it is, so a consumer can prefer to wait / batch when the
band is diffuse for many reasons rather than spend an active-sensing action on a coin-flip. It is the
**precision-over-the-policy complement** to the existing salience ranking: `--probe` already says *which*
refresh has the highest expected info-gain; γ says *how confident that choice is*.

## Gate (RED-first verified)

`--test` gains three real-path assertions on `_probe`'s new global `probe_gamma`: single load-bearing
axis diffuse → `HIGH`; two load-bearing (kbd+room) → `LOW`; only a weak-lever axis (light) → `LOW`.
Falsified by disabling the HIGH branch (`lb_deg -eq 1` → `-eq 99`): the single-load-bearing assertion
goes **red** (`γ should be HIGH (got LOW)`); restoring goes green. Verified on the edited genome with
`bash ./mesh-interruptibility --test` (`$0`-via-PATH otherwise runs the deployed copy — the drift note).

## Why not discarded

Discardable only if the mesh already carried a **confidence on its policy selection** — it does not.
Every prior FEP landing scores the *value* of an action; γ scores the *decisiveness of the choice
between actions*, a distinct, foundational (Friston 2015) and live (Hesp 2021; Entropy 2025) AIF
quantity. The fix is cheap, pure, report-only, and fits the exact file that already computes the policy
ranking. **A natural next landing** (not taken here — a fresh task): the *valence* reading of γ, i.e.
tracking `Δγ` over time as a positive/negative affect axis (Hesp et al. 2021) — the mesh has arousal-like
signals (`mesh-stress`, load, spend) but no valence.

## Sources

- Friston, Rigoli, Ognibene, Mathys, FitzGerald, Pezzulo — "Active inference and epistemic value,"
  Cognitive Neuroscience 6(4):187 (2015).
- Hesp, Smith, Parr, Allen, Friston, Ramstead — "Deeply Felt Affect: The Emergence of Valence in Deep
  Active Inference," Neural Computation 33(2):398 (2021) — <https://direct.mit.edu/neco/article/33/2/398/95642>.
- eLife reviewed-preprint 92892 — <https://elifesciences.org/reviewed-preprints/92892> (risk/ambiguity v2 · novelty/variability v3).
- "Decision, Inference, and Information: Formal Equivalences Under Active Inference," Entropy 28(1):1 (2025) — <https://doi.org/10.3390/e28010001>.
- "Reframing the Expected Free Energy: Four Formulations and a Unification" — arXiv:2402.14460 (2024).
