# Artificial life & open-ended evolution → MAP-Elites illumination on a distributed sensor mesh (2026-07-28)

**Angle:** cross-domain transfer of an OEE *operational mechanism* to the mesh. **Landed:** MAP-Elites /
Quality-Diversity **illumination** in `scripts/mesh-ideate`'s literature lane — the draw now targets the
darkest area×angle niche instead of sampling uniformly (uncommitted; steward lands).

## The concept (named + cited)

**MAP-Elites** (Mouret & Clune, *"Illuminating search spaces by mapping elites"*, arXiv:1504.04909,
2015; Quality-Diversity lineage — Pugh, Lehman & Stanley) is the canonical open-ended-evolution
*illumination* mechanism: instead of optimizing for one best solution, discretize a **behavioural-
descriptor space** into a grid of niches and drive generation toward the **empty / least-covered cells**
— illuminating the whole space rather than re-sampling a dense region. Empty cells are the highest-value
targets. Still the live frontier of ALife OEE: Faldor & Cully, *"Toward artificial open-ended evolution
within Lenia using quality-diversity"*, **ALIFE 2024** (arXiv:2406.04235); descriptor-learning variants
(Vector-Quantized Elites, arXiv:2504.08057, 2025).

## Why this is somewhere we have NOT been

The mesh embodies the **measurement** side of OEE almost exhaustively — MODES persistence filtering,
evolutionary-activity-vs-raw-activity, niche-construction μ, Hughes "novel-and-learnable", path
divergence (all in `scripts/mesh-vitality`) — and novelty-search **sparseness** (Lehman & Stanley, a
distance *reward*) plus the no-entry **repellent** in `scripts/mesh-ideate`. But the QD *mechanism*
itself — an archive that retains a champion **per behavioural cell** and steers generation to fill
**empty** cells — is the mesh's **standing OEE gap, named by the tree itself**: `mesh-generate:59`
documents MAP-Elites illumination as HELD, blocked on *"descriptor CHOICE is MAP-Elites' own documented
weakness"* — the hard behaviour-distance descriptor for the codebase lane. `mesh-ideate:248` likewise
files the MAP-Elites coverage gap as "needs the hard behaviour-distance DESCRIPTOR", distinct from
sparseness (no grid, no per-cell retention).

## The key observation this lands

**The literature sub-lane's descriptor is already free and discrete.** `gen_literature` picks a review
directive from an **AREAS × ANGLES** grid — 18 areas × 6 angles = **108 niches** — so QD illumination
applies here with *no descriptor to invent*, sidestepping the exact obstacle that HELD the general
version. The prior draw was `area="$(shuf -n1)"`, `angle="$(shuf -n1)"`, gated only by `recent_has`
(exact-key dedup of the last 14 emissions). Over 108 cells with a 14-deep memory that is **coupon-
collector** sampling: it re-hits recent-ish niches while whole area×angle combinations stay **dark** for
long stretches — the generator never systematically covers its own review space.

## The concrete application (named file)

`scripts/mesh-ideate` — `gen_literature`:

- `illum_pick()` enumerates the AREAS×ANGLES grid, counts each cell's coverage in a rolling archive
  (`~/.mesh/.ideate-illumination`, `ILLUM_MAX=500` ≈ 4.6 full grids), and returns a **global-minimum-
  coverage** cell (random among ties via shuf-then-stable-sort) — empty-cell targeting.
- The draw uses `illum_pick` instead of uniform `shuf`; `illum_add` records the emitted cell.
- **Preserved:** the `recent_has` dedup, the density-dependent relaxation phases (Talamali 2019), the
  sparseness instrument, the repellent. Empty-cell targeting and exact-key dedup *reinforce* — the
  darkest cell is by construction rarely-emitted, so it seldom collides with `recent_has`.
- **Distinct** (does not conflate): NOT the novelty-search sparseness reward (no grid, no per-cell
  retention — the exact thing MAP-Elites adds beyond novelty search); NOT the verdict-keyed repellent;
  the codebase-lane descriptor stays open (`mesh-generate`).

### Evidence + gate (seen RED then GREEN)

Live sandbox: **40 emissions → 40 distinct cells** (max coverage 1), where uniform `shuf` would collide
(~33 distinct by coupon-collector). `mesh-ideate --test` seeds the archive with every grid cell at count
1 except one target cell (the unique global minimum) and asserts a single emission lands on that exact
area **and** angle — driving the real `gen_literature`/`illum_pick`. Falsified by reverting to uniform
`shuf` → the emission is a random cell (drew Deleuze, not the target) → RED (verified). Full suite green.

## Tuning / next step

`MESH_IDEATE_ILLUM_MAX` tunes the rolling coverage window. Active by default (not a dead knob). Natural
next step, still open: apply the same empty-cell targeting to the **connection** lane once a behaviour
descriptor is chosen (the codebase-lane gap `mesh-generate` still names), and surface grid coverage % in
a dash so the mesh watches how illuminated its own review space is.
