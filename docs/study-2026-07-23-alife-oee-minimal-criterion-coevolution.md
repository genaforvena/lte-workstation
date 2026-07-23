# Study finding — Minimal Criterion Coevolution (artificial life / open-ended evolution)

**Source:** auto idea-queue task — LITERATURE (live review): ALife & open-ended evolution, cross-domain
transfer to a distributed sensor mesh (2026-07-23).
**Verdict:** Finding + concrete proposal for `scripts/mesh-chaos`. NOT built (touches a load-bearing,
consent-gated reflex — needs design review before landing).
**Date:** 2026-07-23 · owner: genome

## The concept we do NOT embody

**Minimal Criterion Coevolution (MCC)** — Brant & Stanley, GECCO 2017, *"Minimal Criterion Coevolution:
A New Approach to Open-Ended Search"*
(<http://www.cmap.polytechnique.fr/~nikolaus.hansen/proceedings/2017/GECCO/proceedings/proceedings_files/pap140s3-file1.pdf>);
open-ended extensions still live in the 2025 literature (Quality-Diversity via DNS, variable-dimension
skill vectors — GECCO/ACM 2020–2025, <https://dl.acm.org/doi/10.1145/3377930.3389809>).

**Operational mechanism (verified from the paper, not the abstract):** two coevolving populations, each
gated ONLY by a *minimal criterion* — a pass/fail competency threshold, **not** a fitness gradient and
**not** a behavior descriptor. In the canonical maze domain: a *solver* reproduces only if it satisfies a
minimal criterion (reaches the goal); a *maze generator* reproduces only if its maze is solvable by ≥1
current solver but non-trivial. Neither population "wins." As solvers improve, generators must escalate
difficulty to keep passing their criterion, and vice versa — producing **open-ended complexity escalation
without any explicit quality comparison or hand-designed behavior descriptor.** That is exactly the
bottleneck MCC removes vs Novelty Search and MAP-Elites/QD (both need a behavior characterization).

## Why it isn't already embodied here (checked, not assumed)

`mesh-novelty` gives us novelty search; `mesh-sound-reflex --coverage` gives us a QD-flavored recipe-cell
spread. Both need an explicit descriptor. **MCC's reciprocal minimal-criterion arms race is absent.**
`mesh-chaos` picks what to inject by a `RANDOM % 100` probability gate over an opt-in target set
(`scripts/mesh-chaos:393`), and measures breadth with static coverage axes (HOT / undrilled / correlated-
failure). It re-injects faults the reflexes have **already** learned to survive, and it has no mechanism
to escalate toward the current robustness frontier. Selection is random, not coevolutionary.

## Concrete proposal — `scripts/mesh-chaos`

Add an MCC-style scenario population to chaos selection (behind the existing consent/opt-in + probability
gates — it can only ever *narrow* what gets injected, never raise blast radius):

- Keep a small population of scenarios in `~/.mesh/chaos-population.jsonl` (fault type × target ×
  tightened-timeout/composed-fault mutations).
- **Minimal criterion, scenario side:** a scenario is *kept/reproduced* only if, on its last drill, at
  least one reflex **failed to recover within timeout** (it still bites). A scenario all reflexes now
  survive is RETIRED as "solved" — it stops consuming injection budget.
- **Minimal criterion, reflex side (already ours):** a reflex "reproduces" = stays wired iff it recovers
  from ≥1 live scenario (this is `mesh-chaos`'s existing recover-or-ALERT check).
- **Escalation:** mutate surviving scenarios (compose two faults, shorten the recovery window) to sit at
  the frontier. The injector then spends its rare 1-in-100 tick on the fault most likely to expose a real
  weakness *now*, instead of re-drilling a solved one.

This makes the drill difficulty track reflex robustness open-endedly — the ALife transfer, mapped to the
one mesh organ whose job already IS an adversary/solver loop.

## Disposition

Filed as a proposal, not landed. It restructures selection in a consent-gated, load-bearing reflex;
correct move is design review + a RED-first test (a scenario that all reflexes survive MUST retire; a
never-survived scenario MUST persist and mutate) before any code. Cited, concrete, and genuinely a place
the mesh has not been.
