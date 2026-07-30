# Bayesian surprise ≠ Shannon surprise — attention follows the belief-UPDATE (predictive processing / Bayesian brain)

*Live literature review, 2026-07-28. Cross-domain transfer to a distributed sensor mesh.*
*Landed: `scripts/mesh-novelty --bayesian` (report-only, additive, uncommitted for steward).*

## The concept (operational, not philosophy)

Predictive processing keeps confusing two quantities that share the word "surprise":

- **Shannon surprise** (self-information): `−log P(x)` — how *improbable* the datum is under the model.
- **Bayesian surprise** (Itti & Baldi): `KL[posterior ‖ prior]` — how much the datum *moves the model*.

Itti & Baldi's foundational empirical result is that **raw improbability is the wrong attention signal**:
what attracts human gaze is Bayesian surprise, not Shannon surprise. The two *dissociate* — a wildly
improbable event can move no belief (you already knew rare things happen), and a probable event can shift
beliefs a lot (a common type whose *rate* just changed). "Surprise ... arises from violation of a strong
expectation and is quantified by the KL divergence between posterior and prior" — belief-update, not
rarity.

**Sources** (surveyed live, current):
- Itti & Baldi, *Bayesian surprise attracts human attention*, [NIPS 2005](http://papers.neurips.cc/paper/2822-bayesian-surprise-attracts-human-attention.pdf) / Vision Research 49(10):1295-1306 (2009), [ilab PDF](http://ilab.usc.edu/publications/doc/Itti_Baldi09vr.pdf).
- Baldi & Itti, *Of bits and wows: A Bayesian theory of surprise with applications to attention*, Neural Networks 23(5) (2010), [ilab PDF](http://ilab.usc.edu/publications/doc/Baldi_Itti10nn.pdf).
- Still live: *Curiosity-Driven Exploration via Latent Bayesian Surprise*, AAAI 2021; active-inference /
  intrinsic-motivation use through 2024-25 (e.g. [arXiv:2502.02962](https://arxiv.org/pdf/2502.02962),
  *Intrinsic motivation as constrained entropy maximization*).

## Where we'd been — and the gap (the idea applied too loosely, a SECOND time)

`mesh-novelty` is the mesh's **most-saturated** predictive-processing organ. It already carries: marginal
surprisal, **contextual** prediction-error (`--conditional`, itself a 2026-06-20 "applied too loosely"
correction: rarity → residual), diversity, local-global two-timescale deviance (`--levels`),
deterritorialization (`--territory`), the eigenform-absorption blind spot, the Schmidhuber reducible-vs-
noise block, the HGF-volatility HELD note, and the dark-room prior-preference floor.

**Every one of those axes is a *Shannon* surprise** — `−log P(e)` or `−log P(e|prev)`. **None is Bayesian
surprise.** And the tool's #2 payoff is literally a **SPEND gate** — "wake expensive minds on HIGH
novelty" — keyed on exactly the improbability signal Itti & Baldi showed is the wrong one for attention.

## The transfer

`mesh-novelty --bayesian` (alias `--wow`; `--json`). The baseline `base` Counter **is already a Dirichlet**
belief over event types (α = count+1 — the same Laplace smoothing `p()` uses), so the belief-move of one
observation is closed-form. For a unit categorical update (posterior adds 1 to component *t*):

```
KL[Dir(α+eₜ) ‖ Dir(α)]  =  ln A − ln αₜ  +  ψ(αₜ+1) − ψ(A+1)      (nats)
      = the belief-UPDATE          └ αₜ = base[t]+1, A = Σα = the p() denominator N ┘
```

(ψ = digamma, reimplemented numpy-free via recurrence + Abramowitz-Stegun 6.3.18; anchored in `--test` at
ψ(1)=−γ, ψ(2)=1−γ.) Each recent type is scored as a **fraction of a brand-new type's** belief-move at the
current corpus size (`bs_new`) — corpus-calibrated, cannot saturate (the pooled-rank doctrine), never an
assumed 0..1 raw bar. Classes:

- **MODEL-MOVING** (frac ≥ 0.5) — the datum shifts the model of the event distribution → genuine attend.
- **HABITUATED** (high Shannon ≥ 4 b, but belief no longer moves) — a wake the raw-surprisal gate pays
  every recurrence, that Bayesian surprise says skip.
- **ROUTINE** (low on both).

Report-only and advisory, exactly like `--levels`/`--territory`/`--independence`: it does **not** replace
the Shannon SPEND gate nor the dark-room must-attend floor — a chronic critical condition stays attended
even once its belief-move habituates (the two are **complementary**, not substitutes). It names *which*
wakes raw surprisal over-pays; whether to skip one stays with the consumer.

## The live finding (mesh-home board, real window)

```
window Δbelief 0.011b
[climate]               HABITUATED  (Δbelief 0.071b vs surprise 8.25b — 12% of a new type)
[criticality-recovered] HABITUATED  (Δbelief 0.064b vs surprise 8.12b — 11%)
[dispatch]              HABITUATED  (Δbelief 0.011b vs surprise 5.51b —  2%)
[task]                  HABITUATED  (Δbelief 0.006b vs surprise 4.62b —  1%)
[done]                  ROUTINE     (Δbelief 0.001b vs surprise 2.66b —  0%)
```

**Every rare tag on the real board reads HABITUATED** — 8+ Shannon bits (the raw SPEND gate screams
"wake!") but 1–12% of a genuinely new type's belief-move. These are precisely the recurrences that re-wake
minds while telling the model nothing it did not already know: the mesh's board is dominated by known-rare
types that Shannon over-values. A truly first-seen tag would read MODEL-MOVING at ~100% — and *that* is the
wake worth paying for.

## Distinctness

Not a duplicate of any existing axis. `--conditional` is still Shannon (`−log P(e|prev)`), just against a
context prediction; `--levels` splits deviance across timescales; `--territory` tracks recapture of a
surge; the Schmidhuber block asks *which* surprise is reducible. **Bayesian surprise is orthogonal to all
of them**: not *how improbable*, not *at what timescale*, not *reducible-vs-noise* — but *does this datum
MOVE THE MODEL at all*. It is the one axis that habituates a known-rare type without a hand-set floor, and
it critiques the tool's own headline use (attention ← belief-update, not rarity).

## The gate (RED-first verified)

`mesh-novelty --test` drives a stream where `[incident]` is known-rare in the baseline (30 occurrences →
6.13 Shannon bits every recurrence, but the belief has absorbed "rare things happen" → ~0 belief-move →
HABITUATED) and `[surge]` is a brand-new tip type (first sighting → maximal belief-move → MODEL-MOVING).
Both are high-Shannon; only Bayesian surprise separates the wasted wake from the genuine one. **Falsified
two ways:** (1) replacing `bayes_bits()` with `surprisal()` (belief-move → improbability) makes `[incident]`
read MODEL-MOVING → RED; (2) dropping the digamma asymptotic makes ψ(1)=−0.492 (≠ −γ) → the anchor RED.
Restored → `smoke-test: ok`.
