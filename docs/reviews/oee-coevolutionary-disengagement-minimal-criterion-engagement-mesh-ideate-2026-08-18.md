# OEE review: coevolutionary DISENGAGEMENT — the minimal criterion had stopped
# discriminating, and the line that reports it could not say so

node: mesh-home · date: 2026-08-18 · window: genome
area: artificial life & open-ended evolution · angle: a known CRITIQUE / failure mode of the area
landed in: `scripts/mesh-ideate`, `viability_tally()` — UNCOMMITTED in the tree

## The concept we did not embody

Coevolutionary algorithms fail in ways a single population cannot: **cycling**, **over-focusing**,
and **disengagement**. Disengagement is when one population outstrips the other so far that *every*
encounter has the same outcome — every parasite beaten, or every host beaten. The relative fitness
gradient vanishes, selection degenerates into drift, and the run keeps looking active while it has
stopped choosing anything.

The counter-intuitive remedy is **reduced virulence**: selecting for the maximum ability to defeat
the opponent is precisely what destroys the gradient the arms race depends on, so a *moderately*
virulent parasite outperforms a maximally virulent one.

## Sources, and what was actually read

- **Origin (cited by record only):** Cartlidge & Bullock, "Combating Coevolutionary Disengagement by
  Reducing Parasite Virulence", *Evolutionary Computation* 12(2):193–222 (2004), PMID 15157374.
  **The full text was not reachable from this node** — HTTP 403 at MIT Press, Southampton eprints and
  PubMed. Nothing here is quoted from it.
- **Read first-hand — the same principle in its live ML form:** Parker-Holder, Jiang, Dennis,
  Samvelyan, Foerster, Grefenstette & Rocktäschel, "Evolving Curricula with Regret-Based Environment
  Design" (ACCEL), ICML 2022, PMLR v162. Verbatim from the PDF: edits "may move those that are
  currently **too hard or too easy** towards the frontier of the agent's capabilities"; and "since
  ACCEL uses a minimax **regret** objective (**rather than minimax as in POET**), it naturally
  promotes levels at the frontier of agent's capabilities." Maximise *learnability*, not difficulty —
  reduced virulence, rediscovered.
- **Still live (abstract read first-hand):** Mead, Lacerda, Foerster & Hawes, "Improving Regret
  Approximation for Unsupervised Dynamic Environment Generation", arXiv:2601.14957, 21 Jan 2026.

Prior-art gate 2026-08-18: `mesh-prior-art "coevolutionary disengagement"` → **CLEAN**;
`mesh-prior-art "virulence"` → **CLEAN**. Zero hits in knowledge/, chat.log, scripts+docs.

## Where it lands, and the measurement

`mesh-ideate` runs a genuine two-population coevolution: review-AREAS (the "mazes") against the
mesh's EMBODIED-CAPABILITY set (the "agents"), under Brant & Stanley's Minimal Criterion Coevolution.
The file quotes the criterion correctly — a maze is viable iff **"SOME-but-not-ALL agents solve
it — neither trivial nor impossible"** — and then implements only the SOME half: `viability_tally()`
asks `n > 0` and nothing else. **A one-sided criterion cannot detect its own saturation.**

Measured on the live corpus with the tool's own `VIABILITY_MAP` and window:

    FERTILE = 18, DORMANT = 0, of 18 areas  ->  discrimination rate 0.000

Every area passes. Consequences, both real:

1. The `MCC-VIABILITY` line is a **constant** — it lists the whole population as FERTILE and
   "DORMANT: none" on every run, so it carries no information about the criterion's state.
2. The behaviour this file has HELD for a steward ("bias `illum_pick` toward VIABLE areas — Brant &
   Stanley's actual move") would be a **literal no-op**, because VIABLE *is* the entire population.

A cross-check with a looser area key (48 filename prefixes rather than the tool's 18 mapped areas)
gives 47 viable / 1 dormant — 0.979 — the same saturation seen through a different lens. The
tool's own map is the number that governs, and it is 0.000.

## What shipped

`viability_tally()` now publishes **ENGAGEMENT** beside the partition: the fraction of the area
population the criterion actually separates, plus a verdict that names the pole when it saturates.

    ... | ENGAGEMENT 0.000 (0/18 discriminated out): DISENGAGED(all-pass — every area clears the
    criterion, so FERTILE is the whole population and a selection keyed on it changes nothing)

`ENGAGED` when some pass and some do not; `DISENGAGED(all-pass)` and `DISENGAGED(all-dormant)` for
the two poles, named apart — they are opposite states and must never print the same sentence.
Report-only, exactly as the partition already was.

**HELD (behavioural, steward/operator-gated):** the reduced-virulence move itself — tighten the
criterion (shorten the window, or require more than one landing) until it discriminates again, which
is "aim at the frontier, not at maximum difficulty" transposed. Held for two reasons: changing the
criterion changes which areas get drawn, and that is a generation-BEHAVIOUR change, not a report; and
a saturated read has a benign reading too — a genuinely productive spell across every area — which
only a trend across several windows can separate from a criterion that has gone slack.

## Gates

Three states driven through the real `viability_tally()`, falsified both ways:

- mixed fixture (fresh + ancient landing, the REAL map) → `ENGAGED`, and must **not** read DISENGAGED
- 2-area substitute map, both fresh → `ENGAGEMENT 0.000 (0/2)` → `DISENGAGED(all-pass)`
- same map, both ancient → `ENGAGEMENT 1.000 (2/2)` → `DISENGAGED(all-dormant)`
- the two poles must name **different** strings

Mutation-checked from a scratch copy, 5 mutants, all RED: engagement clause dropped · all-pass reads
ENGAGED · both poles share one sentence · rate computed from the fertile count instead of the dormant
one · mixed also reads DISENGAGED.

## Note on this artifact

This file is itself an `oee-`prefixed landing, so writing it feeds the very corpus the criterion
reads — it makes the `artificial life & OEE` area score FERTILE for another 30 days. That is the
mechanism working as designed, and it is also exactly why the saturated reading needed publishing:
a criterion every member passes is satisfied by its own output.
