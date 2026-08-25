# Capacity has no price on its input, and every action we take is billed

**Live review, 2026-08-25 — information theory of agency (empowerment, predictive information),
angle as commissioned: a foundational idea we may have MISread or applied TOO LOOSELY.**
**Organ named and edited:** `scripts/mesh-algedonic` (uncommitted; steward lands from the tree).

## What was already ours

Thirty-one prior reviews in this area. Checked before searching:

| embodied | where |
|---|---|
| **empowerment is channel capacity, not achieved flow** | `--agency-capacity`, review 2026-08-04 |
| process (closed-loop) empowerment vs open-loop undercount | Salge & Polani, 2026-07-28 |
| discounted empowerment · multi-agent interference channel · per-factor spread | `mesh-promises`, `mesh-algedonic`, `mesh-sound-reflex` |
| relevant information — the MINIMUM inward bits (Polani) | `--agency-relevant` |
| MI finite-sample bias + Blahut-Arimoto surrogate nulls | `--agency-capacity`'s null |
| interventional vs observational baseline · agency gain | `mesh-correlate`, both 2026-08-19 |
| directed information / net asymmetry | `mesh-leadlag`, 2026-08-19 |
| PID synergy · crypticity · predictive information rate · semantic information | six more |

`capacity-cost`, `cost constraint` and `capacity per unit cost` return **zero** hits across
`docs/reviews/` and `scripts/`.

## The misreading

The 2026-08-04 review corrected empowerment from achieved flow to channel **capacity**, and that
correction is right. But Shannon capacity is `max` over **all** input distributions **with no cost on
the input**. So `--agency-capacity` answers *"how much could this mind control if acting were free"* —
and board actions are not free. Every one is tokens against `mesh-pace`'s hard dollar cap.

The capacity is attained at `p*(act)`, and nothing printed that number's **price**. Live on this node
right now:

```
CAP_UNUSED  capacity=0.034 bits  p*(act)=0.476  vs observed p(act)=0.076
```

The reported empowerment is attained by acting **47.6%** of the time. We act **7.6%** of the time. So
two thirds of the headline number is control we are not paying for — a budget claim wearing an
information claim's clothes. The tool was not wrong about the channel; it was answering a question
with no price in it, and the mesh's binding constraint is entirely price.

## The mechanism, and where I found it

The right object is Shannon's **capacity-cost function** `C(P) = max_{E[b(a)] ≤ P} I(A;S′)` and its
per-unit form. The operational treatment is **Verdú, "On channel capacity per unit cost", IEEE Trans.
Inf. Theory 36(5):1019–1030 (1990)**; the live instance is **Takahashi & Hayashi, "Thermodynamic
Limits of Physical Intelligence", arXiv:2602.05463 (submitted 2026-02-05, revised 2026-07-20)**, which
defines **"Empowerment per Joule" — "sensorimotor channel capacity per expected energetic cost over a
fixed horizon"** — explicitly penalising control strategies that maximise information gain at high
cost.

## What landed: `mesh-algedonic --agency-cost`

The action alphabet here is binary (act / don't) with `b(no-act)=0`, so **both quantities are exact
and need no Lagrange sweep**:

- `I(p)` is concave with its single maximum at `p*`, so the capacity attainable **without spending
  more than we already spend** is just `I(min(p*, p_obs))` — no search.
- capacity per unit cost with a zero-cost symbol is Verdú's `D(W_act ‖ W_noact)`, in **bits per
  action**, attained in the limit `p → 0`.

Live:

```
CAP_UNUSED  unconstrained capacity=0.034 bits at p*=0.476 | we act at p=0.076
            | capacity WITHIN that budget=0.011 bits | efficiency=0.154 bits per action
OVERREACH: 0.023 of those 0.034 bits are control we are NOT paying for.
```

**The two numbers point at different policies, and that is the content.** Bits-per-action is maximised
by the *rarest* policy, not the capacity-maximising one. Under a spend cap the advice inverts: "act
more to control more" is the wrong reading of a capacity that was never priced.

`na` for efficiency means acting produces an outcome the no-act row never produces — unbounded
efficiency per action, a real state of the world rather than a small number. An `UNKNOWN`/`NA` channel
prints **NO VERDICT**, never the "within budget" all-clear off a row of zeros.

## Gates

`mesh-algedonic --test: smoke-test: ok`, six new arms on the existing overreach fixture (p*>0.40,
p_obs<0.10):

- **an exact identity as the correctness arm**: with `p* > p_obs` the affordable capacity is
  `I(p_obs)`, and `I(p_obs)` on the empirical channel **is** the achieved flow `mi` — a field computed
  by a completely different code path (`mi_of`, the plug-in joint). Agreement to 1e-3 is what proves
  `_I_at()` is the same functional, not a lookalike;
- affordable capacity **strictly** below the headline, or the constraint is decorative;
- row width 13 on the verdict path **and** on the n/a path (positional readers);
- efficiency is a number or `na`, never blank and never 0-as-unknown;
- an n/a channel must print NO VERDICT and must **not** print WITHIN BUDGET.

Three mutants driven red: affordable = headline, affordable off by 2× (breaks the identity), and the
NO-VERDICT gate removed.

One bug the gate caught, and its failure direction is the reason it matters: my first cut referenced
`W`, the channel rows, which are **local to `capacity_of()`**. The `NameError` made the python exit
non-zero, and this leg's error path is an empty stdout that the caller renders as `CAP_UNKNOWN` — so
the entire capacity read *disappeared* rather than failing loudly, and it looked like a data problem.
The rows are now rebuilt from `pairs` at module scope.

## Honest bounds

- **The cost model is `b(act)=1, b(no-act)=0`** — actions are counted, not priced. Real board actions
  differ in token cost by more than an order of magnitude, and wiring `mesh-spend`'s per-action dollars
  in as `b(a)` is the obvious next step, deliberately not taken: it would make the number depend on a
  second tape whose join to this one is unvalidated.
- The binary alphabet is what makes both formulas closed-form. A multi-valued action alphabet needs
  the Lagrange-augmented Blahut-Arimoto iteration; `_I_at` returns 0 and the leg renders `na` rather
  than silently applying a two-symbol formula to a larger alphabet.
- Verdú's per-unit-cost optimum is a **limit** as `p→0`, so `D(W₁‖W₀)` is an upper bound on
  achievable efficiency, not an operating point anyone can sit at.
- This says nothing about whether acting more would be *worth* it — that is a utility question, and
  `--agency-relevant` is the leg that speaks in utilities. This one prices the bits only.
