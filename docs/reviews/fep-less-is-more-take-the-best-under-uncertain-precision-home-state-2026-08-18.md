# LIVE REVIEW — FEP / active inference: LESS-IS-MORE under uncertain precision

**Date:** 2026-08-18 · **Lane:** idea-queue LITERATURE baton (genome) · **Organ touched:** `scripts/mesh-home-state`

## The source (live, read today off the arXiv feed — not a fixed list)

Alex Bogdan, **"Free Energy Heuristics: Fast-And-Frugal Cognition as Active Inference Under Uncertain
Precision"**, arXiv:2606.15877v1, submitted **2026-06-14**, <https://arxiv.org/abs/2606.15877>.

Found by querying the live arXiv API for the newest `abs:"active inference"` submissions (60 most
recent, 2026-03 → 2026-08). Rejected on the same sweep as already-embodied or non-applicable:
2607.20306 (state-dependent observation noise ≈ our `fep-channel-knowledge-map-context-conditioned-
observation-noise-precision`), 2608.04232 (interoceptive attention ≈ our `fep-interoceptive-precision-
allocation`), 2608.09512 (renormalising generative models — architecture, no organ), 2606.23325
(Brody/Friston/Meister/Pothos, confirmation bias on square-root probabilities — beautiful, but the
mesh has no binary-hypothesis evidence-*selection* site to apply it to).

## The mechanism we did not embody

Two theorems:

- **Thm 2.6.1** — the policy minimising **expected free energy under uncertain precision** stops
  integrating cues after a **finite** number of high-validity ones, when the precision prior is
  **heavy-tailed** (i.e. when the agent does not know how reliable its own weights are).
- **Thm 2.7.4** — under a *Descending Dominance* condition that stopping policy is **sample-wise
  identical to take-the-best** (Gigerenzer's one-cue fast-and-frugal rule). Fast-and-frugal heuristics
  and active inference are two descriptions of the same computation; **"less-is-more" is evidence
  about the meta-uncertainty regime, not evidence against Bayesian cognition.**

Empirical leg (pre-registered, gate fixed before data): FEH-79, seven models, five CoT lengths, 7,875
responses — on high-meta-uncertainty items longer chain-of-thought **costs 17.3 accuracy points**
(95% CI [7.7, 25.5]); matched items with definite answers show no cost.

**Why it is new here.** `grep -rniE 'take-the-best|meta-uncert|heavy.tail|frugal|less-is-more' scripts/
docs/reviews/` → zero hits on this concept before today (the `frugal`/`heavy-tail` hits in
`mesh-convexity`/`mesh-criticality` are Taleb's 2-shock test and SOC tails, unrelated). It is
**second-order** to everything the mesh has landed: precision-weighting prices a cue's reliability;
this prices **uncertainty about that reliability estimate**, and that flips the optimal rule from
*weight everything* to *stop after k*. A perfectly precision-weighted sum is still the dominated
policy when the weights are unsure.

## Where it lands: `scripts/mesh-home-state`

The mesh's purest instance of the high-meta-uncertainty regime. Every cue weight in that fold is a
**hand-set integer** (`+1` — the file's own comment reads *"Low weight (+1): this measures the
neighborhood, not the home occupant directly"* — `+2`, `+3`) with **no validity estimate behind it and
no corpus it was fitted to**: a heavy-tailed precision prior by construction. And the fold is pure
**additive integration** — ~25 sites push points into `score`, argmax wins. Regime condition holds;
the theorem's conclusion is that summing the long tail of `+1` cues is not adding signal and can
manufacture a confident verdict that the single most-valid cue contradicts.

Distinct from the four reviews already in that file — degeneracy-of-support (counts distinct modality
*families*; five degenerate `+1` cues are exactly the tail this theorem says to drop), O-information
(prices what a cue *adds*, not whether our estimate of what it adds is trustworthy enough to sum),
and the off-manifold shadow (prices the **margin** — but a verdict can win by a *wide* margin built
entirely of `+1` cues while the one `+3` cue points elsewhere; margin cannot see that).

**Sibling note.** `mesh-situation`'s fold is `max(rank INTERNAL, rank EXTERNAL)` — a selector, i.e.
literally take-the-best. Its causal-emergence review reads that max as a **defect**; under Thm 2.7.4
the same max is the **EFE-optimal** rule when validities are unsure. Not a contradiction — they price
different things (synthesis vs meta-uncertainty) — but neither organ *measured* which regime it was in.

## What was written (instrument-first, verdict untouched)

`scripts/mesh-home-state`, uncommitted in the tree:

1. `_VoteScore` — a `dict` subclass replacing `score = {}`, so all ~25 existing
   `score[X] = score.get(X,0)+N` sites need **no edit** and the cue ledger can never drift out of sync
   with the fold it describes. Vetoes go through `score.pop()` (not `__setitem__`) — correct by
   construction: a popped state is gone from the final dict and the shadow filters cues to survivors.
2. `frugality(votes, sc)` — returns the **take-the-best** pick (highest-validity single cue), whether
   it **agrees** with the additive argmax, **k\*** (fewest top-validity cues after which the running
   argmax never again leaves the full-integration winner; k\*=1 ⇒ take-the-best already suffices), and
   **tail_share** (winner's mass from minimum-weight cues). Returns `None` → renders `na`/`-`/`-1`,
   never a fabricated 0, including when a veto-then-revote makes the cues unable to reconstruct the
   argmax (metrics off cues that do not sum to the verdict would describe a different fold).
3. Emitted in `--json` under `off_manifold.frugal` and appended to the existing margin ledger
   (**9 → 13 tab fields**; the only reader is this file's own `--test`, swept in the same edit).
4. `--test-frugal` hidden hook + three `--test` legs: divergence, **matched control** (without it the
   divergence assertion cannot distinguish a real detector from one that always cries 0), honest-`na`.
   Plus a real-run wiring leg asserting the four columns come from the **live** recorder.

**Verdict logic is untouched** — same discipline as the off-manifold and causal-emergence blocks: an
operator-facing, cry-wolf-sensitive organ's fold is the steward's/operator's to change. The held fix
this calibrates: gate on `tbt_agree=0` **and** high `tail_share`, with thresholds ranked against this
ledger's live corpus, never an assumed 0..1. A real disagreement rate near zero would falsify the
concern for this organ — which is what the instrument is for.

## Artifacts

Gates seen **red then green** (mutants from a scratch copy):

| mutant | gate that fired |
|---|---|
| recorder `__setitem__` stops appending | `FAIL (frugality columns not produced by a real run — vote recorder dead)` |
| cue ordering sorted **ascending** by validity | `FAIL (take-the-best divergence not detected)` |
| one ledger column dropped | `FAIL (margin-ledger row malformed)` |

`bash scripts/mesh-home-state --test` → `smoke-test: ok (… hysteresis→…; off-manifold-shadow→ledger+json ok; semantic-scramble→… ok)`

**First live reading on this node — a divergence, immediately:**

```
state: ACTIVE   score: {'QUIET_NIGHT': 2, 'ACTIVE': 4, 'ACTIVE_SOCIAL': 3}
off_manifold.frugal: raw_state=ACTIVE  tbt_state=ACTIVE_SOCIAL  tbt_agree=0  k_star=5  n_cues=5  tail_share=0.5
ledger: …ACTIVE  ACTIVE  9  1  0.4444  0.9656  3  {...}  ACTIVE_SOCIAL  0  5  0.5000
```

The additive fold says ACTIVE; the single highest-validity cue (a `+3` into ACTIVE_SOCIAL) says
otherwise; **k\*=5 of 5** — every cue is load-bearing, the verdict rides the entire tail — and half the
winner's mass comes from minimum-weight cues. n=1, not a rate: the ledger accumulates the corpus.
