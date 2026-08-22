# Autopoiesis & the biology of cognition — the TWO-RATE REGIME METRIC
## (Zepik/Luisi's homeostasis experiment; live continuation 2025–2026) → `scripts/mesh-records`

date: 2026-08-22 · window: genome@mesh-home · lane: LITERATURE (live review)
task: `literature-autopoiesis-metric-2026-08-22`

---

## 0. Where the previous twelve landings went, and why this is not one of them

`docs/reviews/autopoiesis-*` already holds twelve: closure-of-constraints, complexity-ratio
(Fernández), allopoiesis loop-closure, sympoiesis/holobiont, viability-space, causal
symmetrization, constraint-conservation timescale, semantic closure, measurement–control
complementarity, re-entry, bunch-lifeness, SO-model signed leverage. Every one of them is a
**theoretical/formal** landing — a definition or a formalism turned into a mesh axis.

None of them is the thing this task actually asked for: *a concrete METRIC or EXPERIMENT the area
uses to measure itself*. Autopoiesis has exactly one lineage of **wet-lab** self-measurement, and
the corpus has never been there (`grep -ril` over all 288 reviews: `Luisi` 0 · `vesicle` 0 ·
`Zepik` 0 · `synthesis and destruction` 0).

---

## 1. The concept: the regime is the SIGN OF A DIFFERENCE OF TWO SEPARATELY-MEASURED RATES

**Founding experiment.** Zepik, Blöchliger & Luisi, *A Chemical Model of Homeostasis*, **Angewandte
Chemie Int. Ed. 40(1):199–202 (2001)**. Oleic-acid/oleate vesicles hosting **two competing reactions
inside the same boundary**: one that *produces* boundary surfactant, one that *destroys* it. The
result is a three-way classification read off the sign of `v_gen − v_dec`:

| sign | regime |
|---|---|
| `v_gen > v_dec` | **growth** (→ division / self-reproduction) |
| `v_gen ≈ v_dec` | **homeostasis** — self-maintenance, constant size, *changing material* |
| `v_gen < v_dec` | **decay / death** |

**The methodological point, which is the whole find.** Before Zepik, the wet-lab autopoiesis
programme (Luisi's self-reproducing micelles, 1990; *Autopoietic Self-Reproduction of Fatty Acid
Vesicles*, JACS) measured **growth only** — and *growth is the one regime where the level alone is
informative*. The reason a **destruction reaction had to be deliberately added** is that
**homeostasis is invisible to a level measurement**: a vesicle population of constant concentration
is, on the size axis, *indistinguishable from an inert suspension that is doing nothing at all*.
Constant size is evidence of self-maintenance **only once you can show both reactions are running**.
That is the experimental design: you cannot certify autopoietic self-maintenance from a flat curve;
you certify it from **two nonzero opposing rates whose difference is ~0**.

**The stochastic corollary.** Mavelli & Stano, *Kinetic models for autopoietic chemical systems: the
role of fluctuations in a homeostatic regime*, **Physical Biology 7:016010 (2010)** — models (SRAM /
rSRAM) built explicitly on Zepik's vesicles, examining the homeostatic regime *stochastically*.
Deterministically the balanced regime persists indefinitely; the balance is exactly where the
**variance**, not the mean, carries the survival information. (Honest limit: iopscience.iop.org is
unreachable from this vantage — 403/blocked — so this is at the level the search summary and the
title support, not a read of the full text. Flagged, not claimed.)

**Live continuation (this is not a fixed 2001 list).** The same two-rate structure is being
published now:

- Taneja & Higgs, *Protocell Dynamics: Modelling Growth and Division of Lipid Vesicles Driven by an
  Autocatalytic Reaction*, **Life 15(5):724 (2025)** — homeostasis is again a *balance condition*,
  and it adds a **scale term**: *"The reaction cannot be maintained if the cell is too large because
  the food supply rate is proportional to the area and the food consumption rate is proportional to
  the volume."* The balance is not a constant — it breaks as the system grows.
- *Degradation, Osmosis and the Emergence of Basic Functionalities in Abiotic Synthetic Life-like
  Chemical Systems*, **Life 16(7):1204 (2026)** — degradation as a first-class term in life-like
  chemistry (title/venue from search; mdpi.com 403 from this vantage, abstract not read).
- ALIFE 2026 (Waterloo) is running a *Autopoiesis & Structural Coupling* tutorial covering (M,R),
  chemoton, RAF and COT — the formal lane we have already mined, which is why this review took the
  wet-lab lane instead.

**Sources (all reached by live WebSearch/WebFetch 2026-08-22):**
[Zepik et al. 2001, Angew. Chem.](https://onlinelibrary.wiley.com/doi/10.1002/1521-3773(20010105)40:1%3C199::AID-ANIE199%3E3.0.CO;2-H) ·
[Mavelli & Stano 2010, Phys. Biol. 7:016010](https://iopscience.iop.org/article/10.1088/1478-3975/7/1/016010) ·
[Taneja & Higgs 2025, Life 15(5):724 (PMC12113545)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12113545/) ·
[Life 16(7):1204 (2026)](https://doi.org/10.3390/life16071204) ·
[Autopoietic Vesicles in Different Dynamic Regimes: Growth, Homeostasis and Decay, OLEB 39:340 (2009)](https://ui.adsabs.harvard.edu/abs/2009OLEB...39..340M/abstract) ·
[ALIFE 2026 tutorial](https://autopoiesistutorial.netlify.app/)

---

## 2. Is it already embodied? — NO, and the near-miss is instructive

`scripts/mesh-vitality` **names this exact cancellation** in its own comments — *"tool_count Δ (NET
growth = births − deaths, which CANCELS: 5 tools added + 5 attic'd reads Δ0, identical to zero
activity)"* — and answers it with `inheritance_mu()`, the survival fraction of a fixed 14-day
cohort. That is a **survivorship** answer, not the Zepik answer:

- μ is a **fraction of a past cohort**, so a component born *and* destroyed inside the window is
  invisible to it — precisely the fastest turnover, which is where the regime question bites.
- μ carries **no rate and no time base**: it cannot yield the derived quantity the regime metric
  exists to give, **expected residence time τ = N / v_dec**.
- μ is a **genome** measure. The organ where the level is *saturated* and therefore structurally
  uninformative is not the genome — it is the record corpus.

`mesh-promises` (obligations opened vs discharged) and `mesh-vitality`'s `chan_variety`
(board inflow vs closure) are the only places the mesh reads a *pair* of opposing rates at all, and
both are board-scoped. **No sense, organ or reflex measures its own material turnover.**

---

## 3. The application: `scripts/mesh-records` — a corpus pinned at its cap publishes a LEVEL

`mesh-records` is the archivist: it archives every record-producing organ into a corpus capped by
`MESH_REC_MAX_MB` (2000) and `MESH_REC_KEEP_DAYS` (14), and prunes on every sweep. What it publishes
(`--stats`) is **the level and the order**: corpus file-count, corpus MB against the cap, per-organ
ledger `n` and span, score medians. Read live this minute:

```
corpus: 3071 file(s) / 2439M (cap 2000M / 14d) · ledger 1625 line(s)
per-organ files on disk:  ear 2054 · drop 923 · scape 59 · note3 35
```

**The corpus is a Zepik vesicle and it is running its size prune on every single sweep** (the file's
own comment says so: *"corpus pinned at the 2000 MB cap (so the size prune runs on EVERY sweep, not
occasionally)"*). At the cap, `2439M / 2000M` is a **saturated level**: it is the same number whether
the archivist is ingesting 8 records a sweep and evicting 8, or whether every source organ has gone
deaf and nothing is moving at all. `--stats` cannot tell homeostasis from inert — the exact
degeneracy Zepik added a destruction reaction to break.

**This is not a hypothetical blindness — it has already cost this file two hand-fixes,** both of them
rate problems diagnosed at the level:

1. `THE PER-ORGAN FLOOR` (2026-08-21): note3, this node's only physically independent microphone,
   was *"archived and evicted inside the same 2-minute sweep"* — 0 files on disk against 200 measured
   ledger rows. Residence time had collapsed to below one sweep.
2. `THE GRIND-REACH FLOOR` (2026-08-22): *"zero renders for 1h05m while the grinder ticked on time
   every 10 minutes"* — fresh ear records were the lowest-scoring files in a capped corpus and were
   deleted before the grinder's next tick. Fixed with `MESH_REC_GRIND_REACH=900`, a **constant
   guessed from the grinder's cadence**.

Both are the same measurement: **is a record's expected residence time longer than the reach of the
consumer that must see it?** Both were found by a human noticing a downstream silence, because
nothing in the tool measures τ. And the 900 s shield is a *fixed* number in a system whose demand
grows with organ count — the scale term Taneja & Higgs make explicit (`supply ∝ area, consumption ∝
volume`): a shield sized for today's ear rate is not a shield at tomorrow's.

### The concrete change (implemented, see §4)

`mesh-records` gains a **turnover accumulator + a regime verdict**:

- `prune_corpus` and the sweep loop **count what they actually did**, per organ: records archived,
  records evicted by age, records evicted for space.
- One line per sweep is appended to a durable monotone tape `~/.mesh/records-turnover.log`
  (accumulator, delta'd across the interval — never a rate computed from the *ledger*, which is a
  per-organ sliding window with a coverage reserve and therefore **structurally cannot** give the
  chattiest organ's archive rate: `ear n=600` spans 66.5 h *truncated*, so a ledger-derived ear rate
  is a statement about the retention cap, not about the ear).
- `mesh-records --regime [hours]` reads the tape and publishes, **overall and per organ**:
  `v_gen` (rec/h in), `v_dec` (rec/h out), the regime word, and `τ = N / v_dec` — the expected
  residence time — flagged **STARVED** when `τ < GRIND_REACH`, which is the invariant the 900 s
  constant is a guess at.
- **`INERT` is a distinct verdict from `HOMEOSTASIS`.** `v_gen ≈ v_dec ≈ 0` is *not* balance; that
  is the whole point of the 2001 experiment, and it is the one verdict a level-reading `--stats`
  can never produce.
- Every rate publishes its **coverage** (how much of the requested window the tape actually spans),
  per the CLAUDE.md rule; a window with no tape renders `na`, never `0`.

### Doctrine line this earns

> **A saturated level is not a state — publish the two opposing RATES that hold it there.** A corpus
> pinned at its cap, a queue at its bound, a pool at its quota: the level is the same number for
> healthy turnover and for a dead producer, so a verdict read off it is a constant. Measure ingress
> and egress separately over the same window, name `INERT` (both ≈ 0) as its own verdict distinct
> from `HOMEOSTASIS` (both large, difference ≈ 0), and derive residence time `τ = N / v_dec` so a
> consumer's reach can be checked against it instead of guessed at with a constant.

---

## 4. What was NOT done / open

- The **fluctuation** half (Mavelli & Stano) is *not* implemented: a variance term on `v_dec` and a
  distance-to-death in fluctuation units is the natural next axis, and the honest position is that I
  could not read that paper's full text from this vantage.
- `mesh-vitality`'s `tool_count Δ` has the same shape and is **left alone** — it already carries
  `inheritance_mu` as a partial cover, and that file is at 30+ axes. Named here so the next mind
  does not re-derive it.
- The 2026 *Life* 16(7):1204 degradation paper is cited by title/venue only (403 from this vantage).
