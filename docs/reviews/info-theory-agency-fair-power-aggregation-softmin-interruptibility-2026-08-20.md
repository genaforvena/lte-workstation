# Live-literature review — information theory of agency: THE AGGREGATOR IS THE OBJECTIVE — a bystander folded in by SUM is a utility monster; fold by inequality-averse soft-min

**Date:** 2026-08-20 · **Window:** genome (idea-queue LITERATURE task) · **Seam:** information theory of
agency / empowerment / predictive information, from a live CRITIQUE
**Status:** BUILT in tree + deployed, **uncommitted** (steward lands) — `scripts/mesh-interruptibility`

## The paper

**Jobst Heitzig (Potsdam Institute for Climate Impact Research) & Ram Potham — "A Fair Objective for
Human-Empowerment-Preserving AI: Desiderata, Design, and Likely Behavioral Consequences",
[arXiv:2608.08240](https://arxiv.org/html/2608.08240) (v1, 8 Aug 2026).**

Found by web-searching the live 2026 empowerment literature for the *critique* end of the seam. Rejected
along the way as already-embodied or off-seam:

- [arXiv:2511.04177](https://arxiv.org/abs/2511.04177) Yang, Zhang, Cakmak & Kleiman-Weiner, "When
  Assisting One Disempowers Another" — **already embodied** (`mesh-interruptibility:319`, the very caveat
  this review replaces). Its v2 (Jul 2026) numbers are cited below because they are the empirical case
  *for* the fix.
- [arXiv:2509.22504](https://arxiv.org/abs/2509.22504) Song, Gore & Kleiman-Weiner, EELMA (ICML 2026) —
  already reviewed 2026-08-04 (`…discounted-empowerment-eelma-board-mesh-promises…`).
- [arXiv:2604.21155](https://arxiv.org/abs/2604.21155) multi-agent empowerment / interference channel —
  landed 2026-08-03 in `mesh-algedonic --agency-actors`.
- [arXiv:2502.02962](https://arxiv.org/html/2502.02962v3) Kiefer, "Intrinsic motivation as constrained
  entropy maximization" — a *unification* (empowerment ⊂ active inference ⊂ constrained maxent), and its
  one sharp failure mode ("without an a-priori agent/environment distinction, dying is the highest-entropy
  state") is the mesh's already-embodied semantic-information / viability seam (2026-07-29).
- [arXiv:2510.05996](https://arxiv.org/pdf/2510.05996) empowerment pre-training (env-dependent optimal
  n-step horizon) — the horizon axis is covered by the discounted-empowerment fix.

## The concept we did not embody: **the aggregation RULE across parties**

The mesh already knows *that* assisting one party can disempower another — Yang et al. is quoted in the
source. What it did not have is the next question, which is where all the content lives: **when several
humans' powers must become ONE number, which function do you use?**

Heitzig & Potham derive it from axioms rather than picking it. The individual layer is
goal-attainment capability `C_h^{g_h}(s)` → individual power `I_h(s) = log₂ Σ_g 2^{ζ C_h^g(s)}`; the
aggregate over humans ℋ is

```
P(s) = −log₂ Σ_{h∈ℋ} 2^{−ξ · I_h(s)}          ξ > 0 = inequality aversion
```

and they explicitly **reject the alternatives**: the utilitarian **sum** permits unlimited compensation
(the utility-monster problem — one party's collapse bought by another's gain), the **Nash product** loses
Pigou–Dalton, **egalitarian/leximin** is "overly extreme". Two of their axioms are the load-bearing ones:

- **Disempowerment Focus** — *adding an all-powerful human does not change P(s)*. Only the badly-off move
  the verdict. (In the formula: `I_h → ∞` contributes `2^{−ξ·∞} = 0`.)
- **Inequality Aversion (Pigou–Dalton)** — transferring power from a more- to a less-powerful human
  *raises* the aggregate. Their Cor. 4.1 puts a hard floor under it: if `k ≤ 2^ξ − 1`, reducing one
  human's power from 1 bit to 0 **cannot** be made up by raising k others.

Their own empirical motivation is the same Disempower-Grid result: **106 of 110 layouts (96%)** show an
assistant that empowers the user disempowering a bystander, and the obvious patch — add the bystander's
empowerment to the objective — prevents it in only **52%** while significantly degrading the user's reward
(p<0.001) in all 106. So the aggregator is not a detail bolted onto the objective. It *is* the objective.

## Why it applies here (measured, not asserted)

`mesh-interruptibility --foreclosure` is the mesh's embodiment of assistive empowerment: it scores how much
each FORM of a proactive act forecloses the operator's option space (reversibility + exclusivity +
attention-capture), so a consumer can pick the min-foreclosure form of its intent. A co-present third party
was passed as `+party` — and the entire effect of that flag was:

```bash
case "$party" in +party|party|multi)
  fc_caveat="multi-party-disempowerment: operator-empowerment is not the whole objective here — …" ;;
esac
```

**A string.** It never touched `fc_score` or `fc_band`. Two consequences, both real:

1. **A safety knob named in prose.** Live, before the fix, an act that costs the operator *nothing* and is
   *irreversible* for a bystander scored `foreclosure=0/8 band=LOW` with a footnote. Every consumer that
   compares forms by band — which is the whole point of the verb — would pick it.
2. **The comment asserted the wrong aggregator.** It said the score "is net-across-parties" — a **sum**,
   which it neither computed nor should. Under a sum (or mean), that same act reads `4.5/9 = MED`: the
   operator's gain literally pays for the bystander's loss. That is the utility monster, in our source, in
   the one tool whose job is to *not* be one.

This is not hypothetical on this node. `mesh-home` sits in the **bedroom** where rozalia and bruno sleep,
while the operator is usually elsewhere in the flat (memory `mesh-home-sits-in-the-bedroom-not-where-the-
operator-is`). Every `speaker-say` / `ambient-mix` / `speaker-autoplay` the mesh can emit lands on
bystanders who get none of the intent and cannot dismiss it. The bystander seat is the *typical* seat here,
not the exotic one.

## What was built — `scripts/mesh-interruptibility`

The bystander becomes a **party with its own three dims**, and the two are folded by the paper's rule:

```
I_h    = MAXF − f_h                                     residual option-bits left to party h
fc_agg = MAXF − ( −log₂ Σ_h 2^{−ξ·I_h} ) / ξ            (normalised by ξ, so ξ→∞ is the exact min)
```

`MESH_FC_XI` (default 1) is the inequality-aversion knob. Parties with `f_h = 0` are untouched by the act,
hence all-powerful with respect to it, hence **excluded from the sum** — that is Disempowerment Focus made
executable, and it is also why the single-party path **reduces exactly to the old number** (no regression:
with one party, `−log₂ 2^{−ξI}/ξ = I`). Each form now carries a bystander triple read from the third
party's seat — worse reversibility (they cannot dismiss a line addressed to someone else), the same
exclusivity (they lose the same shared speaker/TV), none of the intent.

Report-only, like the rest of the verb: it nominates the min-foreclosure form, it never actuates.

### The measured difference

```
$ mesh-interruptibility --foreclosure raw 0 0 0 +party 3 3 3
before: foreclosure=0/8 band=LOW  … caveat=multi-party-disempowerment: … may be disempowered
after:  foreclosure=0/9 band=HIGH bystander=9/9 aggregate=9.0/9 … NOT a sum

$ mesh-interruptibility --foreclosure ambient-mix +party
  foreclosure=4/9 band=HIGH bystander=5/9 aggregate=5.6/9     (alone: 4/9 MED)

Pigou–Dalton, same TOTAL foreclosure 6:   (0,6) → 6.0 HIGH    (3,3) → 4.0 MED
ξ sweep on (3,3):  ξ=0.5 → 5.0   ξ=1 → 4.0   ξ=2 → 3.5   ξ=16 → 3.1 → min = 3.0
```

The ξ sweep is the axiom visible as a number: weak aversion drifts toward summing the harm, strong aversion
converges on the worst-off party.

### Gates (`--test` block 10b) — **every one seen RED**, mutants run from a scratch copy

| mutant | gate that caught it |
|---|---|
| `agg="$fc_score"` (revert to operator-only) | `limited-trade-off: … banded LOW (agg=0)` |
| soft-min → arithmetic mean | `limited-trade-off: … banded MED (agg=4.5)` |
| drop the `f<=0 → skip` line | `disempowerment-focus: an UNAFFECTED bystander moved the aggregate (0 → 1.0)` |
| hardcode `xi=1`, ignore the env | `xi: at xi=16 the aggregate must converge on the worst-off party (3.0), got 4.0` |
| caveat back to prose (no number) | `the multi-party caveat must quote the bystander's SCORE, not just prose` |

Plus the reduction property (no-party aggregate ≡ operator score) and bystander dim-range refusal, so an
out-of-range bystander cannot be silently scored 0 — the same silent-all-clear trap the unknown-form
refusal already closes. Full suite green: `smoke-test: ok (18 fusion + … + 10b fair-multi-party
(disempowerment-focus/limited-trade-off/sum-rejection/pigou-dalton/xi) + 11 vocab-coverage)`.

## The transferable rule

**Whenever a per-party (or per-lane, per-sense, per-actor) quantity is collapsed to one number, the
aggregator carries the ethics and it is almost never the sum.** A sum or mean cannot distinguish "both
parties fine" from "one fine, one destroyed" — and the second is exactly the state the measurement exists
to catch. Sibling of the fusion doctrine already in `CLAUDE.md` ("an unreachable input renders UNKNOWN,
never a faked all-clear"): that rule protects against a *missing* input, this one against a *collapsed*
one. And its precondition is sharper still — **a party that enters the objective as a comment string is
not in the objective at all.** `grep -n 'caveat=' scripts/` is a cheap way to find the next one.

Not swept beyond this tool. Candidates with the same shape, unaudited: `mesh-fitness` / `mesh-vitality`
lane means, `mesh-sensorium` cross-sense fusion, `mesh-algedonic --agency-actors` (per-actor MI is already
decomposed — the question is how the pane collapses it).
