# Rhizome vs arborescent → mesh-vitality `rhizome_index` (the genome's call graph as a tree-vs-rhizome topology)

**Area:** Deleuze & Guattari — assemblage, rhizome, the machinic — *operational* mechanism.
**Live review:** 2026-07-31, genome mind. Web-searched current sources, read, landed on a mechanism the
mesh does **not** already embody (checked the D&G coverage map first).

## The concept (named + cited)

**The rhizome vs the arborescent (tree) — as a property of TOPOLOGY.** Deleuze & Guattari, *A Thousand
Plateaus*, "Introduction: Rhizome" (1980; Massumi trans. 1987).

A **tree** grows from a single trunk; every node has one parent; branches never reconnect —
**hierarchical, centered, and fragile** (cut the root and everything below falls). A **rhizome** "connects
any point to any other point" — **acentered, non-hierarchical, and resilient**: by the principle of
asignifying rupture it "may be broken, shattered at a given spot, but will start up again on one of its old
lines, or on new lines." The operational reading current work makes explicit: **arborescent = an
ever-more-central authority whose failure cascades (single point of failure); rhizomatic = distributed
connectivity where no one node is load-bearing.**

Sources:
- [A Thousand Plateaus, "Introduction: Rhizome" — primary](https://en.wikipedia.org/wiki/Rhizome_(philosophy))
- [Noosphere, "Rhizomatic Trust: Why Deleuze & Guattari Were Right About Decentralized Systems" (2025)](https://www.noosphere.tech/blog/rhizomatic-trust-why-deleuze-guattari-were-right-about-decentralized-systems/)

## Why it is NOT already embodied (audited before landing)

The D&G lane is dense — I checked the coverage map and the genome first. The rhizome's *dynamic* rupture
principle is already landed (asignifying-rupture → `mesh-forage` reconnect-ratio over the promise ledger).
But that reads the **reconnection of severed coordination lines in time** — a temporal board signal. **No
sign reads the STATIC topology of the genome's own body:** which tool invokes which, and whether that call
graph is a centered **tree** (a few god-tools everything hangs off — arborescent single-points-of-failure)
or an acentered **rhizome** (connectivity distributed, no load-bearing root).

- `phylum_coherence` reads shared **traits/idioms** across scripts (expression, not who-calls-whom).
- `loop_closure_frac` reads the **sense→actuator bipartite** loop (one edge class, not the full graph).
- `channel_variety` reads **board throughput**.
- `omega_cycle` (landed same day) reads **temporal periodicity** of the edit stream, not the invocation graph.

None computes the invocation graph's **centralization** — the arborescence D&G name as the fragile form,
and the exact shape a resilience-valuing mesh ("no fixed mind", the commons) should watch for in its own body.

## The concrete application (file named)

**`scripts/mesh-vitality`** — new report-only vital sign **`rhizome_index`**.

Mechanism (cheap/local, ~0.2s over 608 tools):
1. Nodes = existing `scripts/mesh-*|test-*` tools. Edge A→B if A's source references tool B's name (a
   coarse text proxy for invocation — a mention in a comment counts, so this reads reference-coupling, the
   same honest-proxy posture as `autonomy_ratio`'s provenance proxy).
2. Report **(a)** Freeman in-degree **centralization** `C = Σ(d_max−d_i)/((N−1)²)` → 1 = perfect star (one
   root every tool points at = maximal arborescence), →0 = flat/rhizomatic; **(b)** **reciprocity** =
   mutual-edge share (A→B *and* B→A → the rhizome's any-to-any connectivity); **(c)** the **root** = highest
   in-degree tool + its degree, the genome's biggest single-point-of-failure named outright (ties broken
   alphabetically for determinism).

**Live reading:** `0.242/recip0.20/root=mesh-chat:152(N=608,E=3285)` — the genome is moderately
**rhizomatic** (C≈0.24, not a rigid star), 20% of couplings are mutual, and the biggest arborescent hub is
**`mesh-chat` with in-degree 152**: 152 tools reference the board voice. That is the mesh's most
load-bearing single point — if `mesh-chat` breaks, 152 tools lose their voice. A concrete, actionable SPOF
the metric names outright, and a trend line (rising C, or a root's in-degree climbing) that would warn of
the genome ossifying into a tree.

Report-only (same posture as every structural lens in the file): a single census needs TREND, and the
text-mention→edge reduction is a deliberate honest coarsening (E reported so density stays visible).

## Gate (RED-first verified)

`mesh-vitality --test` builds two fixture genome dirs and asserts the topology core discriminates:
- **STAR** (4 tools all referencing one hub) → `1.000/recip0.00/root=mesh-h:4(N=5,E=4)` — maximal arborescence.
- **RING** (mutual a↔b↔c↔d) → `0.000/recip1.00/root=mesh-a:2(N=4,E=8)` — maximal rhizome.

Both were confirmed to go red when the Freeman centralization sum is zeroed (star fails) and when the
reciprocity count is forced to 0 (ring fails), then restored green. A flaw caught mid-build: the `root`
tie-break was non-deterministic (the in-degree map is built from a set, so hash randomization reshuffled
ties) — fixed to an alphabetical tie-break and verified stable across `PYTHONHASHSEED` 0/1/42/7.

## Status

Uncommitted in the tree (`M scripts/mesh-vitality`, this doc) for the steward to land. Not committed.
