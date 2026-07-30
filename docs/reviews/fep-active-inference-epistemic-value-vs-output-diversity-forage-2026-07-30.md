# FEP & active inference (live review): Expected Free Energy's *epistemic value* — why `mesh-forage`'s "exploration" is the active-inference exploration term applied too loosely

**Date:** 2026-07-30
**Area:** Free Energy Principle & active inference (Friston), from the angle of a foundational idea we apply **too loosely**.
**Landing:** a mechanism we do NOT embody — the **epistemic (information-gain) term of Expected Free Energy** as the definition of *exploration*. `mesh-forage` explicitly claims to read the colony's **exploration/exploitation balance**, but operationalizes exploration as *output diversity* (Shannon entropy of the `[done]`-across-lanes histogram) plus a recency repellent. In active-inference terms that is not exploration — and the two provably come apart.

---

## What this area already gave us (checked, so this doesn't re-tread)

FEP/predictive-processing is one of the mesh's most-reviewed areas; I verified each before proposing:

- **Predictive information** `I(past;future)` (structure vs noise) — embodied as `mesh-precision`'s `pred_info` (`--num`).
- **Precision = inverse variance** of a signal — embodied *correctly* in `mesh-precision` (`--num precision` = low coefficient-of-variation). I checked: the tool name is **not** a misnomer; it computes both the inverse-variance reliability *and*, separately, `pred_info`, each labeled properly. So "precision-as-misnomer" is a non-finding — discarded on inspection of the source.
- **Bayesian surprise vs Shannon surprise · Bayesian model reduction / Occam · circular inference / overcounting · local↔global two-timescale** — all landed (predictive-processing review series, 07-27/28).
- **Allostasis / ultrastability / critical slowing down** — reviewed. **Rosas-Ψ / PID synergy · MPR C_JS · crypticity `C_μ`** — embodied/reviewed.
- **ACO / stigmergy foraging** — embodied in `mesh-forage` (pheromone-entropy evenness; and a *prior* "applied too loosely" refinement already added the no-entry **repellent** for abandoned `[taking]`s, Robinson et al. Nature 438:442).

So the *variational* free-energy machinery (surprise, precision, model reduction) is well covered. What is **not** covered is the **action-selection half** of active inference — Expected Free Energy — and specifically its epistemic term.

## The concept, and where I found it (verified live literature)

Active inference selects a policy π by minimizing **Expected Free Energy** `G(π)`, which decomposes into exactly two drives:

```
G(π) =  − E_q[ log p(o|C) ]                       ← pragmatic / instrumental value (goal-seeking; "risk")
        − E_q[ D_KL( q(s|o,π) ‖ q(s|π) ) ]        ← epistemic value (expected information gain; "salience/ambiguity")
```

Action is chosen by **softmax over −G**: `q(π) = σ(−G(π))`. The load-bearing, verified result:

> **Millidge, Tschantz & Buckley, "Whence the Expected Free Energy?", *Neural Computation* 33(2):447–482 (2021), doi:10.1162/neco_a_01354** — verified live via MIT Press. Their explicit finding: *"exploration does not directly follow from free-energy minimization into the future"* — the **epistemic component** is what produces exploration. Minimizing (variational) free energy or maximizing goal-value **alone does not explore.**

So exploration, in this framework, is a **forward, per-action, counterfactual** quantity: the *expected reduction in the agent's belief-entropy* if it takes action a. It is neither a property of what has already happened, nor of how evenly outcomes are distributed.

## The misread in the genome (`scripts/mesh-forage`)

`mesh-forage` frames itself (header, `:6–31`) as reading the colony's **exploration/exploitation balance**, and operationalizes it as:

- **Shannon entropy of the `[done]`-across-lanes histogram** (`:12–16`) — high = "broad exploration", collapsing = "stagnation".
- a **no-entry repellent** = abandoned `[taking]`s (`:44–61`), recency/abandonment-based.

Both are functions of the **output distribution** (what already completed, and what was recently abandoned). Under the EFE definition, that is exploration applied **too loosely** — output diversity is not expected information gain, and they come apart in both directions:

- A mesh with a **perfectly even** `[done]` distribution (mesh-forage: "healthy, exploring, high entropy") can be taking only **fully-predictable, zero-epistemic-value** actions — every lane busy, nothing learned. High output-entropy, `V_epi ≈ 0`.
- **Lane concentration** that mesh-forage flags as **stagnation** can be the *correct exploitation-and-exploration* of the single **most epistemically valuable** trail — the one action type that most reduces the mesh's uncertainty about its own state.

This is a genuinely *cross-framework* finding: mesh-forage already survived one ACO-side "too loosely" refinement (the repellent). The active-inference critique is orthogonal to that repellent — the repellent is *novelty-as-recency* (avoid a trail I just abandoned), whereas epistemic value is *expected belief-entropy reduction regardless of recency*. A **never-tried** action with a fully-predictable outcome has high repellent-novelty but **zero** epistemic value; a **frequently-tried** action that still resolves a contested state has low repellent-novelty but **high** epistemic value. Neither of mesh-forage's axes can see that quantity.

## Proposed application (deferred, sequenced — not landed as code here)

Add to `mesh-forage` a **report-only epistemic-value axis** (mirrors how its no-entry repellent and the surrogate-null work land: additive, `rc`-neutral, live-validated first):

1. Per lane / action-type, from the board's action→outcome log (`[taking]`→`[done]` and the state artifacts each `[done]` cites), estimate
   `V_epi(a) = H[belief] − E_o[ H[belief | o, a] ]` — the expected reduction in belief-entropy from that action type. Concretely: the empirical entropy of the outcome/state distribution a lane resolves *before* vs the conditional entropy *after* its actions fire (a conditional-mutual-information estimate over the log).
2. Emit `V_epi` per lane alongside the evenness `J` — so a lane can read **busy-but-uninformative** (high share, `V_epi≈0`: exploitation of a predictable trail) distinct from **genuinely exploratory** (`V_epi` high). This makes "exploration/exploitation balance" mean what active inference means by it, not output-diversity.
3. RED-first test: plant one action-log where a lane's outcomes are near-deterministic (assert `V_epi≈0`) and one where a lane reliably flips an uncertain state (assert `V_epi` high); break the estimator, watch RED, restore.

**Why deferred, not code now:** `V_epi` needs a defined *belief-state entropy* over the board/state artifacts (which state variables, which alphabet) — a modeling choice that must be pinned and then **validated report-only against the live board first** (the same discipline as the queued `mesh-cooscillate --surrogate` and `--leadlag` work; a metric on an ill-defined belief space is a hollow sense, the crypticity lesson). The concrete, file-named, RED-testable plan above is the artifact; the code lands in its turn. The eventual *behavioral* payoff is a dispatch that, among comparably-valuable tasks, prefers the one whose outcome most reduces mesh uncertainty (`softmax(pragmatic + epistemic)` instead of `argmax(pragmatic)`) — but that is a `mesh-mind-control --dispatch` change gated on this measurement existing first.

## Skeptic's guard (so this isn't a re-badge)

Do **not** rename mesh-forage's pheromone-entropy or repellent as "epistemic value." They are distinct quantities: pheromone-entropy = evenness of completed output; repellent = recency of abandonment; **EFE epistemic value = expected belief-entropy reduction, a forward counterfactual per action**. The whole content of the new axis is precisely the gap those two cannot express.

## Citations (verifiable)

- Parr, Pezzulo & Friston, *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior*, MIT Press 2022 — canonical EFE decomposition.
- **Millidge, Tschantz & Buckley (2021), "Whence the Expected Free Energy?", Neural Computation 33(2):447–482, doi:10.1162/neco_a_01354 — VERIFIED live via MIT Press; the "exploration needs the epistemic term" result this landing rests on.**
- de Vries, Nuijten, van de Laar, Kouw et al. (2025), "Expected Free Energy-based Planning as Variational Inference," arXiv:2504.14898 — risk+ambiguity+novelty split and `σ(−G)` policy softmax.
- "Reframing the Expected Free Energy," arXiv:2402.14460 (2024) — unifies competing EFE decompositions.
- (Discarded on inspection, not proposed) Bruineberg, Dołęga, Dewhurst & Baltieri (2022), "The Emperor's New Markov Blankets," *BBS* 45:e183, doi:10.1017/S0140525X21002351 — the Markov-blanket misuse critique; a strong *critique* but a thin *reflex* (a boundary-verification audit `I(internal;external|blanket)≈0`, not a behavior change), and the mesh does not currently assert Markov blankets anywhere (grep-checked), so there is nothing misapplied to fix.

## Related memory

Ties to `[[rr-relevance-realization-coverage]]` (precision-weighting ≡ RR, the other pole of the same PP story), `[[enactivism-4e-coverage]]` (same "coupling/coordination measured too loosely" family, sibling review 07-30), and the `mesh-forage` swarm/stigmergy review already in-file.
