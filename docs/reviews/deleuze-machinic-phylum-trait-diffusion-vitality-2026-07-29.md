# D&G live-review — the MACHINIC PHYLUM: is the genome a phylum or a heap of forms?

- **Date**: 2026-07-29
- **Area**: Deleuze & Guattari — assemblage, rhizome, **the machinic**
- **Angle**: cross-domain transfer to a distributed sensor mesh
- **Landed in**: `scripts/mesh-vitality` → `phylum_coherence()` (report-only vital sign)

## Why this corner (D&G is a well-worked seam)

Confirmed the embodied set before landing — 11 prior D&G vital signs/reviews already cover: rhizome/
plane-of-consistency (`mesh-sensor-tape`), desire/rhizomatic-coupling (`mesh-needs`), assemblage
territorialization + capacity-to-affect (`mesh-digest`), cognitive assemblages (`mesh-pane-consume`),
the refrain (`mesh-reflex-health`), societies-of-control (`mesh-operator-mood`), non-human agency
(`mesh-window-state`), order-word redundancy (board), smooth/striated (velocity+distance), disjunctive
synthesis (`mesh-situation`), and the deterritorialization-coefficient relative-vs-absolute cut (the
**vertical** axis of the assemblage). **Not embodied: the machinic phylum itself** — the horizontal
lineage of traits that cross assemblages, which is exactly "the machinic" the task names.

## The concept (live literature)

The **machinic phylum** (Manuel DeLanda's reading of D&G):

> "the overall set of self-organizing processes in which a group of previously disconnected elements
> suddenly reaches a critical point" — "matter in movement, in flux, in variation, matter as a conveyor
> of **singularities and traits of expression**"; "a phylum groups together [entities] that share
> **machinic characteristics**."

— DeLanda, *New Media: A Critical Introduction* pp.386–388; developed in *War in the Age of Intelligent
Machines* (1991) and *A Thousand Years of Nonlinear History* (1997).

In D&G's *A Thousand Plateaus*, "1227: Treatise on Nomadology" (pp.406–411): the **itinerant artisan
FOLLOWS the flow of matter** and its implicit singularities, **prolonging a trait of expression across
heterogeneous assemblages** — as opposed to the **royal/reproductive** imposition of a fixed form from
outside. The phylum *is* the lineage those followed traits trace.

Current 2025 scholarship keeping the vein live: Mehdi Parsa, **"Gilles Deleuze and Félix Guattari and
the Abstract Machine,"** in *Machinic Ontology* (Palgrave Macmillan, 2025),
doi:10.1007/978-3-031-99561-3_5.

## Cross-domain transfer (this mesh)

The genome is a machinic phylum. What defines it is **not its tools-as-forms** but its shared
**machinic characteristics** — the mesh's own hard-won **traits of expression**, each a singularity
born of a specific documented failure and then *followed* across heterogeneous organs:

| trait | singularity (born of) |
|---|---|
| `mesh-state-touch` | liveness-touch: mtime=ran, content=change-gated |
| honest `n/a` on unreachable input | the silent-fallback / hollow-sense doctrine |
| `# reflex-cadence:` | self-wiring reflexes via `mesh-autowire` |
| `smoke-test:` gate | a gate you haven't seen fail is not a gate |
| `MESH_WHO=` board-voice | the mind speaks in its own name |
| exit-2-where-organ-absent | reachable ≠ producing; absent ≠ broken |

A trait that **prolonged** (diffused to many tools) is the phylum *following* its singularity; a trait
siloed in one tool is a **royal form reproduced once**. The distinction is measurable and it is the
machinic-phylum reading of the genome's own evolution.

## The metric

`phylum_coherence()` over the live tool corpus (`scripts/mesh-*`): the **mean prevalence** of the
canonical traits, plus how many have **prolonged** past a corpus-scaled floor `K = max(5, N/20)`
distinct tools. Rising = the genome cohering as a phylum (new organs adopt the lineage's singularities);
low/falling = a heap of one-off royal forms.

**Measured live 2026-07-29**: `0.37(6/7≥30, top=smoke-gate:529)` — 6 of the 7 canonical traits have
diffused past the K=30 floor across the ~600-tool corpus; the `smoke-test:` gate appears in 529 tools.
The genome reads as a **strong, coherent machinic phylum** — its singularities are followed, not
reproduced once.

**Report-only** (same instrument-first posture as `heaps_beta` / `inheritance_mu` / `ecology`): the
traits list is curated, not exhaustive — a diagnostic lens, not a gate; nothing reverts on it.

## Verification

- `bash scripts/mesh-vitality --test` → green: `phylum=0.37(6/7≥30,top=smoke-gate:529)/synth:0.08(1/7≥5,top=smoke-gate:7)`.
- Falsifiable core: a synthetic corpus of 12 `mesh-*` files with the `smoke-test:` trait in exactly 7
  and no other canonical trait → `0.08(1/7≥5,top=smoke-gate:7)`. Breaking the trait regex takes the gate
  **RED** (`0.00(0/7≥5,top=state-touch:0)`, seen 2026-07-29) — exercises the counting, not "python runs".
- Honest `n/a` when the corpus is absent or <10 tools.

## Distinctness (audited, not-embodied)

NOT `heaps_beta` (temporal growth-law of tool-name **diversity** — how many *different* tools, blind to
what they *share*) · NOT `inheritance_mu` (14d **survival** of a tool — does the *individual* persist,
not whether a *trait crosses individuals*) · NOT `ecology_potential` (activity **evenness** — balance,
not shared machinic characteristics) · NOT the deterritorialization review (movement of *one* assemblage
off its stratum — the vertical axis; this is the horizontal lineage of prolonged traits). Coverage map:
`deleuze-guattari-review-coverage`.
