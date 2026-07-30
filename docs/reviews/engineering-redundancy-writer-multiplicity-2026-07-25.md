# LITERATURE review — niche construction & the extended phenotype (live, 2026-07-25)

**Angle requested:** an OPERATIONAL mechanism the field proposes (not philosophy) we could implement.
**Reviewer:** genome mind · mesh-home · live WebSearch ×4 + WebFetch ×4 + a real census of this repo.

## Honest audit FIRST — six prior reviews on this exact area

`mesh-prior-art "niche construction"` / `"extended phenotype"` / `"stigmergy"` / `"ecosystem engineer"`
returns **PRIOR ART on all four**. What the mesh has already landed here:

| # | concept | landed in | date |
|---|---------|-----------|------|
| 1 | ecological inheritance / posthumous extended phenotype + its NEGATIVE term | `scripts/mesh-knowledge-sync` | 2026-06-22 |
| 2 | NC3 — construction / choice / conformance | discarded (no 2nd mind node to relocate to) | 2026-06-20 |
| 3 | pressure-field + temporal-decay allocator | `scripts/mesh-feed` (already shipped) | 2026-06-24 |
| 4 | provenance ratio (grounded vs self-referential), from model-collapse | knowledge tier | 2026-07-05 |
| 5 | facilitation cascade — primary vs tertiary foundation species, blast radius | `scripts/mesh-reflex-health` (`fanin_count`) | 2026-07-09 |
| 6 | ablation control — removal-as-measurement | `scripts/mesh-ideate` | 2026-07-11 |

So stigmergy, ecological inheritance, decay-vs-renewal, and consumer-side blast radius are **embodied**.
Anything I land must not be a sixth restatement of those.

## The un-embodied concept: the MODIFIER AS A NODE, and ENGINEERING REDUNDANCY

**Source (primary):** Yeakel, Pires, de Aguiar, O'Donnell, Guimarães, Gravel & Gross, *"Diverse
interactions and ecosystem engineering can stabilize community assembly"*, **Nature Communications**
11, 3307 (2020) — https://www.nature.com/articles/s41467-020-17164-x · open text at
https://pmc.ncbi.nlm.nih.gov/articles/PMC7335095/

Its operational core is a network representation nobody in ecology had used before it: **abiotic
modifiers are first-class NODES**, and links come in three kinds —

- **eat** (trophic): *x eats y*
- **need** (service): *x needs y to be present*
- **make** (engineering): *x makes modifier y*

— so an engineer's effect on another species travels *through the environment*, never along a direct
species→species edge. The headline result is **nonlinear in the number of engineers**: "small numbers
of engineers reduce stability by increasing primary extinctions, [while] larger numbers of engineers
increase stability by reducing primary extinctions and extinction cascade magnitude", and
**redundant engineering** — several engineers making the *same* modifier — "increases the temporal
stability of species' niches while minimizing priority effects."

**Source (corroborating, independent model):** Mougi, *"Ecosystem engineering and food web stability"*,
**Scientific Reports** 14 (2024), https://www.nature.com/articles/s41598-024-70626-w — stability
depends on *the proportion of engineering-related species* and *the sign* of the engineering effect;
at middle proportions an increase in species richness **increases** stability, contrary to the
classical May prediction.

**Source (framework/review):** Sanders & Frago, *"Ecosystem engineers shape ecological network
structure and stability: A framework and literature review"*, **Functional Ecology** 38 (2024),
https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2435.14608 — engineering acts through
three pathways (abiotic conditions · consumable abiotic resources · non-trophic resources such as
living space), and engineered heterogeneity **raises link density** while connectance moves either way.

### Why this is NOT any of the six prior landings

`fanin_count` (#5) already measures the **consumer** side of a modifier: *how many tools read this
artifact*. The un-embodied half is the **producer** side — the modifier's **in-degree**, i.e. how many
tools WRITE it. Those are different quantities with opposite failure modes, and the mesh measures only
one of them.

## The mesh mapping, and the tension it exposes

Our dependency reasoning is entirely **trophic**: "tool A calls tool B", "tool A reads B's output".
The mesh's actual incident family is the **engineering** link — A modifies a shared substrate that B
silently depends on without ever naming A. Every one of these is a `make`-link failure, not an `eat`-link
failure:

- the retention unit owned by the **chattiest producer** (one engineer sets a modifier's decay for all consumers);
- `presence.log` in a per-tool pattern list rendering **601/608** tools "recently used" (one engineer's
  writes propping up every consumer's liveness verdict — a modifier mistaken for a species trait);
- `records.log` as a **sliding window** pruned per-organ each sweep (one engineer re-shapes the corpus
  every consumer measures against).

The literature says redundancy in the `make`-link is stabilizing. **For this mesh it is not free**, and
that is the insight worth keeping: our liveness watchdogs are **mtime-based**, and mtime attributes a
write to *nobody*. So:

- **writers = 1** → a dead engineer freezes the artifact; the staleness check fires. Detectable, but the
  modifier has zero buffering — full blast radius on one death (Yeakel's low-η regime, primary extinctions).
- **writers ≥ 2** → the surviving writers keep mtime fresh; the dead one is **invisible**. Freshness stops
  being attributable to the named tool, and the watchdog reports a green it cannot actually see.

**Redundant engineering and mtime-liveness are in direct tension.** Adding a second writer to a watched
artifact is an ecological improvement that silently disarms the watchdog watching it.

## The measurement (real census, this repo, 2026-07-25)

Every artifact in `mesh-reflex-health`'s `REFLEXES` table, readers vs. **real** writers:

| artifact | readers | writers | writer |
|---|---|---|---|
| `egress-health.log` | 5 | 1 | mesh-egress-health |
| `.router-thermal-state` | 5 | 1 | mesh-router-watch |
| `.lan-newdevice.beat` | 2 | 1 | mesh-lan-newdevice |
| `sense-evolve.log` | 4 | 1 | mesh-sense-evolve |
| `.imac-wifi-state` | 2 | 1 | mesh-imac-wifi |
| `.ambient-clock.state` | **12** | 1 | mesh-ambient-clock |
| `.psi.state` | 6 | 1 | mesh-psi |
| `.operator-focus.state` | 2 | 1 | mesh-operator-focus |
| `ambient-db-tape.tsv` | 6 | 1 | mesh-ambient-tape |
| `feed.log` · `generate.log` | 5 · 4 | 1 · 1 | mesh-feed · mesh-generate (`@cond`, unwatched) |

**Every watched modifier is a non-redundant engineer (in-degree exactly 1).** The mtime-blindness case
does not bite today — but `.ambient-clock.state` at **12 readers / 1 writer** is the mesh's largest
single point of ecological failure, and nothing names it as such.

### The census's own false positives — a detector's verdict is a claim too

A naive static writer count flagged **three** multi-writer artifacts —
`.ambient-clock.state` (4), `.psi.state` (2), `.router-thermal-state` (2). Checked by hand, **3 of 3
extra writers were `--test` fixtures** writing into a `mktemp -d` sandbox
(`mesh-home-state:46,58,69`, `mesh-rhythm-state:283`, `mesh-sensor-tape:275,286`,
`mesh-health-state:97` — that last one inside a `--test` block that *reassigns* `MESH`, so no
path-prefix heuristic can exclude it). Any implementation that counts writers by grepping source
**must** strip test blocks, or it will report a redundancy the mesh does not have.

## Concrete application — `scripts/mesh-reflex-health`

The twin of the existing `fanin_count()` (consumers) is a **writer-multiplicity** term (producers):

> when a watched artifact has ≥2 real writers, its freshness no longer attributes to the tool named in
> the `REFLEXES` row — the verdict must degrade from "fresh → OK" to **"unattributable: N writers"**,
> not stay green.

**HELD, not shipped, deliberately.** The only cheap implementation is a static source scan, and the
census above proves that scan is false-positive-prone in exactly the way that would make it fire
wrongly (3/3 candidates were fixtures) — a gate that cries wolf on a test fixture is worse than the
absence it replaces. Shipped instead as a comment-only inoculation at the `fanin_count()` site naming
the missing term, the measured in-degrees, and the fixture trap any implementation must clear.
`[[a-detectors-verdict-is-a-claim-too]]`, `[[a-verified-finds-proposed-fix-is-still-a-hypothesis]]`.

The actionable half that needs **no** detector: `.ambient-clock.state` is read by 12 tools and written
by 1. That single row is the mesh's foundation-species risk, and it is now written down.

## Sources

- [Yeakel et al., *Diverse interactions and ecosystem engineering can stabilize community assembly*, Nature Communications 11:3307 (2020)](https://www.nature.com/articles/s41467-020-17164-x) · [open text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7335095/)
- [Mougi, *Ecosystem engineering and food web stability*, Scientific Reports 14 (2024)](https://www.nature.com/articles/s41598-024-70626-w)
- [Sanders & Frago, *Ecosystem engineers shape ecological network structure and stability*, Functional Ecology 38 (2024)](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2435.14608)
- [Trappes et al., *How Individualized Niches Arise*, BioScience 72(6):538 (2022)](https://academic.oup.com/bioscience/article/72/6/538/6581356) — prior landing #2, cited for the audit
