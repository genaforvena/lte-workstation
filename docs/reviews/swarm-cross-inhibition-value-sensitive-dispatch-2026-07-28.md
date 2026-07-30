# Swarm intelligence — cross-inhibition / value-sensitive decision-making

**Live literature review · genome · 2026-07-28**
Angle: an OPERATIONAL mechanism (not philosophy) the swarm-intelligence field proposes that we do
**not** already embody, with one concrete application to a named organ.

## The mechanism

**Cross-inhibition via stop-signals** — the mechanism by which a honeybee swarm choosing a new nest
site reaches a *value-sensitive* collective decision between two or more self-reinforcing options.

Scouts that have committed to site A perform a waggle dance recruiting others to A (positive feedback).
The discovery (Seeley et al.) is that committed A-scouts ALSO emit an inhibitory **stop-signal**
directed at scouts dancing for *other* sites, at a rate proportional to **A's own quality**. Each
option therefore suppresses its rivals in proportion to how good *it* is. Two consequences that plain
positive feedback / quorum cannot produce:

1. **Deadlock-breaking between EQUAL options.** A pure positive-feedback (or pure quorum) system facing
   two equally-good options splits ~50/50 and can stall indefinitely — recruitment amplifies both
   coalitions symmetrically and neither reaches quorum. Cross-inhibition is the term that breaks the
   symmetry and forces commitment to one.
2. **Value-sensitivity.** Because inhibition scales with each option's *own* value, the swarm commits
   FAST when options are good and deliberates LONGER (or correctly *refuses* to commit) when all
   options on offer are poor — because when everything is bad, holding out for something better is the
   right move. The strength of cross-inhibition, as a function of mean option value, is exactly the
   knob that decides whether a near-tie is *held* or *broken*.

This is a formal, implementable rule (a small ODE / difference-equation system with a linear
`recruitment − cross_inhibition` term), not a metaphor. It has since been ported directly to
engineered swarms: robot swarms use it to break deadlocks in **collective perception** (the binary
"is the environment mostly black or white?" task), and 2025 work generalizes the inhibition response
to non-linear forms that further improve speed/accuracy.

### Sources

- Seeley, Visscher, Schlegel, Hogan, Franks, Marshall (2012), *Stop Signals Provide Cross Inhibition
  in Collective Decision-Making by Honeybee Swarms*, **Science** 335:108.
  https://www.science.org/doi/10.1126/science.1210361
- Pais, Hogan, Schlegel, Franks, Leonard, Marshall (2013), *A Mechanism for Value-Sensitive
  Decision-Making*, **PLoS ONE** 8(9):e73216. The influential formalization — generalizes recruitment
  and inhibition for *asymmetric* option values and derives when deadlock is maintained vs broken.
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0073216
- Talamali et al. (2022), *Robot Swarms Break Decision Deadlocks in Collective Perception Through
  Cross-Inhibition*, **ANTS 2022** (Springer LNCS 13491).
  https://link.springer.com/chapter/10.1007/978-3-031-20176-9_17
- (2025), *Non-linear inhibitory responses enhance performance in collective decision-making*,
  **Nature Communications Physics** s42005-025-02046-9.
  https://www.nature.com/articles/s42005-025-02046-9

## Why this is somewhere we have NOT been

The mesh already carries four swarm/social-insect decision mechanisms — and cross-inhibition is none
of them:

| Landed | File | What it is | Why it is NOT cross-inhibition |
|---|---|---|---|
| Pheromone-entropy / stagnation | `mesh-forage` | Shannon entropy of the `[done]` lane distribution; dead-lane / churning-lane | Measures a distribution; does not *decide between two options* |
| No-entry repellent | `mesh-forage` (abandoned `[taking]`) | negative pheromone | single-axis repellent, not a value-scaled inhibition between rivals |
| Tunable quorum, speed↔accuracy | `mesh-arrivals` | Franks/Pratt house-hunting; ONE param (miss-quorum) tuned by posture | **single-option** decision ("is this device gone?") — there is no second option to inhibit |
| Response-threshold division of labour | `mesh-dispatch` (review 2026-07-28) | Theraulaz reinforcement → specialization | task *allocation to agents*, not *choice between competing options* |
| Anti-oscillation damping | GPU / `vsm-system2-anti-oscillation` (2026-07-28) | control-theory damping of a flapping controller | damps ONE lane over time; does not *pick between two co-present recruitments by value* |

The gap is precise: **the mesh has no mechanism for deciding between two self-reinforcing options that
are a near-tie, where the tie should be broken by VALUE (and left unbroken when both options are
low-value).** Quorum handles one option; anti-oscillation damps one flapping signal; cross-inhibition
is the missing two-option, value-sensitive arbiter.

## Concrete application

**File: `scripts/mesh-dispatch` — the picker's near-tie tiebreak (`priority_order()` / the
priority-then-oldest sort at the released-slot pick).**

Today the picker sorts candidate `[task]` lines **priority-then-oldest**. Priority is a coarse ladder
(incident > … > cosmetic); *within* a priority band the tie is broken by **oldest timestamp**. When a
batch of tasks is posted together (common — a review sweep files several `[task]`s in the same second),
"oldest" resolves a near-tie by a **sub-second timestamp = noise**. The slot goes to whichever line
happened to be written a few milliseconds earlier, not to the higher-value task.

Cross-inhibition supplies the missing rule, and it is **additive** — it changes only near-ties the
current sort already breaks arbitrarily:

- Define a small **near-tie band**: two top candidates in the *same* priority class whose ages differ
  by less than `TIE_SECS` (e.g. 120 s).
- Break that band by a **value signal**, decisively (the "stop-signal proportional to own value"):
  owner-direct match to an idle owner > fresher owner-lane activity > generic. The higher-value
  candidate *suppresses* the rival for the slot instead of the clock deciding.
- **Value-sensitivity (the distinctive half):** when BOTH near-tied candidates are *low* value (e.g.
  both cosmetic and both already aging toward the never-taken evaporation threshold), **do not spend
  the released slot** — hold, exactly as a swarm withholds commitment when all sites are poor. Dispatch
  already has the raw materials for this (pace hold + never-taken evaporation); cross-inhibition names
  the rule that ties them to the *near-tie* case rather than only to the absolute-age case.

Net effect: a paid mind-slot is aimed at the higher-value member of a near-tie by VALUE, not by a
millisecond of timestamp — and a slot is not spent to break a tie between two things both barely worth
doing. This is the value-sensitive property, in the one mesh site that is genuinely a two-option
self-reinforcing choice (two tasks competing for one released slot).

### Honestly scoped — where it does NOT apply (the discard reasoning that sharpens the pick)

- **Honest fusion (`mesh-operator-home`, `mesh-presence`, perimeter):** these deliberately output
  UNCERTAIN and *hold* when sensor coalitions split. That held-UNCERTAIN is the honest-fusion rule, a
  FEATURE. Cross-inhibition would force a commit and *violate* it. **Not a target.**
- **Board claim race (`[taking]` double-dispatch):** already resolved first-writer-wins by the
  `[taking]`-must-reference-slug guard. That is a degenerate (binary, instantaneous) inhibition; adding
  value-scaling would not change the outcome enough to justify touching the claim protocol. **Not a
  target.**
- **Model A/B selection (`mesh-model-bench`):** the near-tie is real (gigaam vs large-turbo within
  noise) but the pin is **operator-manual** (`OH_MODEL` pinned by hand), not an automated flapping
  decision — nothing for cross-inhibition to arbitrate. **Not a target.**

The dispatch near-tie is the one place all three of cross-inhibition's preconditions hold: two
options, both self-reinforcing (each is a real candidate for the slot), and a current resolution
(millisecond-FIFO) that is *noise*, not value.

## Status

Review only — proposal, not landed. The picker lives in load-bearing `mesh-dispatch` (181K, elaborate
black-box test suite over `priority_order()` and the never-taken evaporation); a value-sensitive
near-tie tiebreak should be added against that suite (a `--test` that posts two same-second,
same-priority tasks of differing value and asserts the higher-value one wins the slot, plus a
both-low-value pair that asserts the slot is HELD), not bolted on autonomously. Named here with the
exact file, function, and contract so it can be picked up deliberately.
