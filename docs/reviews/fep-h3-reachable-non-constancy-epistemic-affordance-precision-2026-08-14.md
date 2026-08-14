# FEP / active inference — H3: reachable non-constancy, or why a context map is not an affordance

**Date:** 2026-08-14 · **Lane:** literature (live review) · **Angle:** a foundational idea we MISread —
and the misread is written in our own genome, three days old.
**Landed in:** `scripts/mesh-precision --reachable` (report-only) + a swept guard in `--ckm`.

---

## The source (read in full)

Daniel Corva, **"State-Dependent Observation Noise Reintroduces Epistemic Value in Linear-Gaussian
Active Inference"**, arXiv:2607.20306, submitted **22 Jul 2026** (independent researcher; §3.3 Main
Result). Read via `arxiv.org/pdf/2607.20306v1` → `pdftotext -layout` (the `/html/…v1` route 404s).

Its ground is Koudahl, Kouw & de Vries, quoted verbatim by Corva (p. 2): agents optimising the full
Expected Free Energy in a linear-Gaussian state-space model **"do not exhibit epistemic drives under
any circumstances"**. Corva restates the consequence in his own abstract:

> "The epistemic term of the Expected Free Energy becomes constant: the agent flattens to a Kalman
> filter whose gain sequence is fixed in advance, regardless of action."

What is left is pure KL control — "the agent steering towards preferred outcomes with no incentive to
learn along the way". Corva's contribution is the *observation-side* departure that brings curiosity
back: an observation-noise covariance `R(x)` that varies with the state. But it only counts under his
assumption **H3**, quoted verbatim:

> **"(H3) Reachable non-constancy.** R is non-constant on the reachable set of predicted means: there
> exist policies π, π′ and a time k such that R(μ⁻ₖ(π)) ≠ R(μ⁻ₖ(π′))."
>
> "H3 excludes the degenerate case in which R varies only where the control cannot go: an R(x) that is
> constant along every reachable trajectory of beliefs is, for all purposes of inference, a constant,
> and the agent flattens trivially. H3 is the demand that the departure of Section 3.1 is genuine,
> that the control can move the operating point of the noise."

And **Corollary 1** — the reason this transfers to mesh senses without a matrix anywhere:

> "Suppose n_o = 1 and H1–H3 hold. Then all three parts of Theorem 1 hold; in particular, the epistemic
> value is non-constant across policies, with no appeal to H3′. … the epistemic value is strictly
> decreasing in the noise variance."

Mesh observations are scalar. H3 alone suffices.

## The misread — and it is ours, in this file, from three days ago

`mesh-precision --ckm` landed 2026-08-11 asking *does an observable context predict how noisy the next
reading will be*. Its headline live finding was **device-indexed context on `presence.log`**: n=7021,
8 buckets, σ 2.62 → 10.89 dB, ratio 4.15×, `CKM_PREDICTIVE`, decisive against a circular-shift null.
That result was then carried forward as licensing an information-seeking axis, and the 2026-07-30
`mesh-forage` review deferred `V_epi` as "needs a pinned belief-entropy over board/state".

H3 says the prior question was never asked. **The mesh does not choose which BLE device transmits.**
A context the mesh cannot move to is a **map, not an affordance** — Corva's H3-degenerate case exactly,
in which the epistemic term is *constant* and any "explore to sense better" selector over that axis is
**vacuous by construction, not merely unbuilt**. And the prior question needs no belief model at all:
it is answerable from a tape plus a named actuator.

Two distinct claims that the genome had collapsed into one:

| | claim | mesh instrument |
|---|---|---|
| R is context-conditioned | a map exists | `--ckm` (2026-08-11) |
| R is context-conditioned **where the control can go** | an affordance exists → epistemic value can vary | *absent until now* |

## What landed

`scripts/mesh-precision --reachable <tape> --actions L1,L2[,…]` — report-only, weights nothing, gates
nothing. It partitions the same tape `--ckm` reads into **reachable** contexts (declared: the labels
some mesh actuator can choose to occupy) and **exogenous** ones, then runs `--ckm`'s own estimator
twice — once on all buckets (reproducing `--ckm`) and once on the reachable subset alone (H3):

- `EPI_LIVE` — reachable-subset heteroscedasticity clears the null → H3 holds → an information-seeking
  action genuinely exists.
- `EPI_DEGENERATE` — the full tape is predictive but the reachable subset is not → "R varies only where
  the control cannot go" → the epistemic term is constant → curiosity here is vacuous.
- `EPI_FLAT` — no map anywhere (a `CKM_FLAT`, restated).
- `EPI_THIN` / `EPI_UNSCORABLE` / `EPI_UNKNOWN` / `EPI_UNDECLARED` — refusals, never a FLAT reading.

Reported magnitude, per Corollary 1: `ε = ½·ln(1 + P/R)` is strictly decreasing in R, but the prior
predictive variance P is **not identifiable from a tape without a motion model**, so the spread is
published as its P→∞ **ceiling**, `½·ln(R_max/R_min) = ln(σ_max/σ_min)` — a bound on the prize that
collapses to 0 as P→0, never the prize.

**`--actions` is mandatory and never inferred.** H3 is a claim about an actuator and the tape does not
contain one; guessing which labels are reachable would manufacture the answer. Undeclared → the
question is **UNASKED**, not answered NO. A declared label matching no bucket is reported by name
(`actions_unmatched`) rather than silently shrinking the reachable set.

## Gates (12 legs, 11 mutants seen RED)

`--test` block (8) — each leg is another leg's red. Mutants were run from a scratch **copy named
`mesh-precision`** (the basename is load-bearing: a copy named otherwise fails unrelated legs and every
mutant would read red for the wrong reason).

| mutant | killed by |
|---|---|
| M1 drop the reachable restriction (H3 collapses to `--ckm`) | 8b, 8c, 8f |
| M2 `EPI_DEGENERATE` branch unreachable | 8b |
| M3′ reachable estimator uses a GLOBAL mean | 8d |
| M3″ `--ckm` estimator uses a GLOBAL mean | 7c |
| M4 shuffle null instead of circular shift | 8e, 8k |
| M5 infer the actuator from the tape when undeclared | 8h |
| M6 no periodic-null guard | 8k |
| M7 unmatched action labels dropped silently | 8g |
| M8 `EPI_THIN` refusal becomes `EPI_FLAT` | 8f |
| M9 ε-ceiling zeroed · M10 ε-ceiling squared | 8l |

**8b is the load-bearing leg:** one fixture that `--ckm` must call `CKM_PREDICTIVE` and this mode must
call `EPI_DEGENERATE`. Without it the mode is `--ckm` under a new name and the whole H3 distinction
asserts nothing — so the leg asserts *both* verdicts on the *same* file.

### Three fixture/instrument traps found while building it

1. **Contiguous label blocks make the shift null swallow a true effect.** A σ=1-vs-8 fixture written as
   blocks reads p_shift = 0.066: a circular shift merely permutes whole blocks and reproduces the
   observed LR. Fixtures now interleave.
2. **A STRICTLY PERIODIC label sequence makes the shift null INVARIANT.** Every shift is a relabelling
   of the same partition, so the LR is identical on all draws, p ≡ 1.0, and an arbitrarily strong
   effect reads FLAT. This is an instrument failure, not a null — a **round-robin poller** produces
   exactly this tape. Now a refusal (`EPI_UNSCORABLE` / `CKM_UNSCORABLE`, `reason:"periodic-null"`)
   in **both** modes, detected as `null_distinct ≤ 1`. Swept into `--ckm` per *a rule asserted at one
   call site is not asserted* — it carried the same blind spot since 08-11.
3. **A BALANCED mean-shift fixture cannot detect a broken means-free estimator.** With equal bucket
   sizes a global mean inflates every bucket's variance by the same amount and the LR does not move —
   `--ckm`'s leg 7c had been passing vacuously since 08-11. Both fixtures are now unbalanced (90 vs 30),
   and M3″ now dies on 7c.

## Live reads (2026-08-14, this node)

**1 — the axis `--ckm` called decisive cannot even be posed.** `presence.log` → 14 309 RSSI readings
over 3 757 devices. Run with no `--actions`: **`EPI_UNDECLARED`**. There is no mesh actuator that
selects which device transmits, so H3 has no subject. That is the finding in its plainest form: the
08-11 headline is a map with no affordance behind it.

**2 — a misdeclaration, kept in the record because it is the failure the caveat names.** Declaring the
two devices the mesh *can* actuate (Bose `28:11:A5:B8:9E:A2`, Samsung TV `5C:49:7D:92:1E:58`) returns
**`EPI_LIVE`** — n=3925, LR=1771.9, p_shift=0.0050, σ 10.740 vs 3.654 dB (2.94×), ε-ceiling **1.078
nats**. It should not be read as an affordance: this is a between-**device** contrast, two sensors, not
one sensor at two policy-reachable operating points, and H3 requires the latter. The tool answered the
question asked; the declaration was wrong. Recorded as a worked example of how to misuse this mode.

**3 — the mesh's cleanest genuine actuator has no epistemic drive.** `mesh-sound-reflex` really does
choose the grind `mode` and `band` per render (`~/.mesh/room-music-params.log`, 206 rows carrying both
`fit` and a chosen label). Outcome noise across the chosen contexts:

| axis (chosen by the grinder) | buckets | σ range | ratio | p_shift | verdict |
|---|---|---|---|---|---|
| `mode` (poly/lib/q) | 3 (70/72/64) | 0.069–0.085 | 1.24× | 0.134 | **`EPI_FLAT`** |
| `band` (fast/slow/mid) | 3 (73/73/60) | 0.060–0.079 | 1.32× | 0.070 | **`EPI_FLAT`** |

So on the one lane where the mesh both acts and measures, the noise the action can reach is flat: this
is Koudahl's flattened agent literally — **pure KL control, goal-seeking with no incentive to learn**.
Not a defect to fix by tuning a selector; a property of the model, and the honest reading is that an
"exploration" term added to grind selection today would be decoration.

## Caveats the emission carries

- H3 is a claim about **this declared actuator**, not about the sense. An axis reading `EPI_DEGENERATE`
  for one actuator can be `EPI_LIVE` for another that reaches further.
- The ε-ceiling is a P→∞ upper bound on the epistemic spread, not the spread.
- Inherited from `--ckm`: predictive, not causal; and on a moving target, state variance and
  observation variance are not separable without a motion model.
- `presence.log` and `room-music-params.log` are sliding windows — every n above is today's answer.
- n=206 on the sound lane is thin; `EPI_FLAT` there is "did not clear the null", not "proved constant".

## Open / not claimed

- No live `EPI_DEGENERATE` was found on a real tape with an honestly-declared actuator — the mesh's
  reachable axes are flat and its heteroscedastic axes are exogenous. The verdict is gated by fixture
  (8b), not yet by a live instance.
- Searched and set aside this session: Nuijten & de Vries, "Sophisticated Policies from Epistemic
  Priors", arXiv:2607.19518 (21 Jul 2026) — closed-loop planning where future actions depend on future
  observations; a real gap, but it needs a rollout model the mesh does not have. `arXiv:2606.04935` /
  `2606.20658` (EFE-as-VI) were already set aside on 08-11 for the same reason.
