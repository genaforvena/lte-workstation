# Live literature review — edge of chaos is not a scalar: temporal universality and peripheral origins

**Date:** 2026-09-10  
**Area:** complex adaptive systems / edge of chaos (Santa Fe lineage)  
**Angle:** a foundational idea we may be applying too loosely  
**Status:** literature artifact only; no tool behavior changed and no commit made.

## The one concept we do not yet embody

**Universality belongs to the ordered transition trajectory and its topology, not to one global
branching ratio or a static hub/periphery label.** Two live results sharpen this in complementary
ways:

1. **Temporal gap universality.** Fang et al. (published online 13 July 2026; version of record 19
   August 2026) analyze the *full ordered sequence* of incremental connectivity changes, not just
   the largest event or an inferred threshold. Their gap-size distribution has two independently
   measurable Fisher-type exponents, `tau_c` in the critical regime and `tau_s` in the supercritical
   regime; the pair classifies empirical networks, which systematically differ from idealized
   network models because of higher-order structure. The practical claim is important here: the
   trajectory can be classified from one system size without knowing the exact critical point.
   [Fang et al., “Temporal self-similarity reveals percolation universality classes in complex
   networks,” Nature Communications 17, 8605 (2026)](https://www.nature.com/articles/s41467-026-75436-4)

2. **Peripheral-origin mechanism.** van de Leemput et al. (2024) perturb every node in simulated
   two-way-pull networks and find that systemic transitions most readily start from nodes with
   *intermediate degree and low closeness centrality*—the fringe sweet spot. Highly connected core
   nodes are buffered by their neighbors; weakly connected nodes cannot create enough local critical
   mass. The mechanism is cooperative local spread across a bottleneck, not “the hub is the
   superspreader.” It persists across network architectures and both deterministic Allee-effect and
   stochastic Ising models.
   [van de Leemput et al., “Transformation starts at the periphery of networks where pushback is
   less,” Scientific Reports 14, 11344 (2024)](https://www.nature.com/articles/s41598-024-61057-8)

These are one operational gap, not two unrelated facts: a single `m-hat` can say that events
reproduce at a certain average rate while hiding *where* the cascade began and whether its ordered
growth has distinct critical/supercritical gap statistics. A static graph class called `PERIPHERAL`
also cannot say that a peripheral node was the seed of a later systemic transition.

## Repository check: why this is genuinely new here

The existing `scripts/mesh-criticality` already carries many checks on the event stream: MR
branching ratio, avalanche shape, dragon-kings, crackling relations, entropy-complexity, dynamic
range, susceptibility, coherent noise, aging, and allometry. It also contains the earlier correction
that “critical = healthy” is task-dependent. None of those records the seed node's degree/closeness
or reconstructs a whole connectivity-growth trajectory and its two regime-specific gap exponents.

The repository's `CORE`/`SOURCE`/`PERIPHERAL` labels in `scripts/mesh-closure` are dependency-mention
classes, not a cascade-topology measure. Treating that label as the literature's “periphery” would be
a category error. This is therefore not a rebranding of the existing edge-optimality, hub-driven
dragon-king, or static closure reviews.

## One concrete application

**Organ/reflex:** `scripts/mesh-criticality`.

Add a read-only `--origin` sidecar whose artifact is an origin-stratified cascade table, not a new
health verdict:

```text
origin=<window-or-node> degree=<observed> closeness=<observed> seed_class=<core|fringe|unknown>
descendants=<n> reached=<n> gap_c=<...> gap_s=<...> evidence=<n>
```

The sidecar should:

- reconstruct a bounded task/dispatch event graph from events that already carry their poster,
  owner, and parent/dispatch identity; refuse rows without those identities as `unknown`;
- compute degree and closeness on the observed graph for each cascade seed, then compare cascade
  reach across degree bins and centrality bins (the falsifiable prediction is a fringe/intermediate
  hotspot, not monotonic hub risk);
- retain the chronological incremental reach/gap sequence and estimate `tau_c` and `tau_s` only when
  both regimes have enough evidence, otherwise emit `INSUFFICIENT` rather than borrowing the global
  `m-hat`;
- remain read-only and advisory: the result is a topology/trajectory diagnosis that can falsify the
  “near `m=1` means healthy responsiveness” transfer; it must not retune dispatch or kill a node.

This is a proposal, not a claim that the implementation exists. The first acceptance artifact should
be a synthetic graph where a hub is buffered but an intermediate-degree fringe seed wins, plus a
single-system-size ordered trajectory whose two gap fits are intentionally different. A negative
result on real mesh data would be useful: it would discard the transfer because the mesh is not a
two-way-pull network or because its graph evidence is too incomplete, not because the old scalar was
quiet.

## Sources actually read (live, 2026-09-10)

- Fang et al., Nature Communications (2026), abstract, introduction, discussion, and methods-facing
  sections on the two gap exponents, single-size/no-threshold classification, empirical-network
  deviation, and ordered trajectory: <https://www.nature.com/articles/s41467-026-75436-4>.
- van de Leemput et al., Scientific Reports (2024), abstract, perturbation protocol, results, and
  mechanism section on degree/closeness, the fringe sweet spot, local critical mass, and robustness
  across architectures: <https://www.nature.com/articles/s41598-024-61057-8>.
- Taming the chaos gently (Nature Communications, 2025) was read as a counterpoint: it reports a
  task where initial edge-of-chaos dynamics help because structured diversity and dimensionality are
  balanced, reinforcing that “edge” is an empirical task relation, not a universal target:
  <https://www.nature.com/articles/s41467-025-61309-9>.

## Verification

```text
review-status: artifact written
tool-edits: none
git-commit: none (operator requested an uncommitted tree)
sources: 3 primary/peer-reviewed live pages opened and read
```
