# Swarm intelligence & stigmergy — pheromone-entropy as a stagnation metric (live review 2026-07-27)

**Angle:** a concrete METRIC the field uses to measure *itself*. **Landed:** the Shannon **entropy of
the pheromone-selection distribution** — Ant Colony Optimization's canonical self-diagnostic — mapped
onto the mesh's own stigmergic medium (the board). New tool: `scripts/mesh-forage` (uncommitted).

## The concept (named + cited)

Stigmergy = agents coordinate not point-to-point but through **marks left in a shared environment**;
other agents react to the marks. Swarm-intelligence practice measures the *health* of such a colony
by the **Shannon entropy of the pheromone field** — the distribution over which trails/components the
agents are currently selecting:

- entropy is **maximal early**, when every trail is equiprobable (broad exploration);
- it **collapses toward zero** as pheromone concentrates on a few paths;
- a collapse that arrives *too early* is the field's textbook **STAGNATION / premature-convergence**
  signature — the colony has locked onto a sub-optimal trail and stopped exploring. Max-Min ACO
  exists specifically to bound this entropy away from collapse.

Sources (read this session):
- *Experiment Study of Entropy Convergence of Ant Colony Optimization* — arXiv:0905.1751 (entropy
  maximal at equiprobable trails, small near convergence).
- *Using Entropy for Evaluating Swarm Intelligence Algorithms* (Rojas-Morales et al., ResearchGate
  220948280).
- Diversity-via-subpopulation-entropy in modern ACO — *Multi-colony ant optimization…*, Complex &
  Intelligent Systems 2022 (s40747-022-00716-7): "higher information entropy indicates better
  diversity of the population."
- Framing anchor (current): *A Methodological Framework for Chaos-Aware Evaluation of
  Self-Organization in Swarm-Based Engineering Systems*, MDPI Systems 14(2):215 (Feb 2026) — order
  parameters & entropy as the primary self-organization indicators; and the recurring 2024–2026
  finding that swarm robustness/scalability "lack well-recognized, standardized, quantitative metrics"
  (Harwell & Gini scalability/emergence/flexibility metrics; arXiv:2512.10166 collective memory in
  decentralized multi-agent AI).

## Why it's a gap we had NOT embodied

The mesh already carries a lot of swarm/complex-systems self-measurement, and I checked each before
claiming the gap:

- `mesh-criticality` — branching ratio m̂ over board events (a **rate**: dormancy vs flood cascade).
- `mesh-hub-criticality` — per-node cascade-blast-radius index (**topology**).
- `mesh-converge` — anti-entropy / inconsistent-window (**replica divergence**).
- `mesh-cooscillate` — pairwise co-movement of numeric signals.
- `mesh-labor` — **$-weighted** effort per window (grepped: no evenness/entropy/gini/concentration).

None computes the **evenness of the work-routing distribution across lanes**. Yet that quantity is
exactly the mesh's most-recurring failure, and it has only ever been caught as *prose*: the DEAD LANE
— a channel green-and-silent while one window carries everything (the witness passive-lane, the
redundant-writer incidents, "one mind doing all the work"). That is, precisely, low-entropy
stigmergic stagnation. No live scalar existed for it.

## The mapping (stigmergy → mesh)

The mesh IS a stigmergic system: minds deposit `[done]` marks on the shared board (`~/.mesh/chat.log`)
and react to each other's marks. Each `[done]` is a completed foraging path; the `who@node` field is
the **trail** it was deposited on. So the ACO pheromone-entropy diagnostic maps directly:

    J (Pielou evenness) = H / ln(k_active),   H = −Σ pᵢ ln pᵢ over lanes' [done] shares

- **BALANCED** J ≥ 0.75 and no lane > 55% — broad foraging.
- **SKEWED** 0.50 ≤ J < 0.75.
- **STAGNATING** J < 0.50 **or** dominant lane ≥ 60% — the colony is funneling into one trail; the
  quiet lanes may be dead.
- **n/a** (exit 2) — fewer than 8 done-marks in window (too little foraging to measure; honest).

Honest scope (named in the tool header): it is a **deposit-COUNT** evenness, not effort evenness — a
lane that lands one huge task and one that lands ten tiny ones read 10:1. That is deliberate: the ACO
quantity is over the selection *histogram*, not path cost; `mesh-labor` already owns the $-weighted
axis. `mesh-forage` is its routing-diversity complement.

## The application (named file, real artifact)

`scripts/mesh-forage` (new, uncommitted, deployed to `~/.local/bin` for the live run):
`mesh-forage` / `--json` / `--hours H` / `--test`. On-demand + `orphan-ok` (a diagnostic READ, like
`mesh-hub-criticality`/`mesh-entropy`; wiring it into `mesh-dash minds` is the natural next step, left
unwired — an unseen reflex is absent).

`--test` is RED-first: an even 4-lane fixture → J≈1.0 BALANCED; a solo fixture → J=0 STAGNATING; a
prose `[fyi]` line mentioning "[done]" is correctly excluded (substring-scan trap); the falsifier
neuters J→0 on the even fixture (dominance held at 0.25, so J drives the verdict alone) and asserts
BALANCED **flips** to STAGNATING — proving the gate reads the real number. Seen fail, then pass.

**Live reading now (this board):**

    forage: BALANCED   J=0.8139   dominant=genome 0.3438   marks=32/12h across 7 lanes
    trail: genome:11 land:10 senses:5 health:2 tg:2 pub:1 discover:1

Non-trivial and true: work IS spread (7 lanes), but genome+land carry 21 of 32 deposits while
health/tg/pub/discover are thin trails — visible now as a number, not a hunch. Had one lane climbed
past 60%, exit 3 STAGNATING would fire.
