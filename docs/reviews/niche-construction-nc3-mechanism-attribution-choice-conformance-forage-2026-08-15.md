# NC3 mechanism attribution — we called everything "niche construction"; most of it is choice, and the mesh had no instrument for conformance

**Area:** niche construction & the extended phenotype
**Angle:** a foundational idea we applied TOO LOOSELY
**Date:** 2026-08-15 · genome · live web review
**Landing site:** `scripts/mesh-forage` (the standing niche-construction / stigmergy site)

---

## The misread

`mesh-forage` narrates its niche work as **niche construction** throughout:

- `degrade()` is headed `NICHE-DEGRADATION / INTER-SCALE (TERMINATOR)` and quotes
  "CONSTRUCTION: an organism modifies its shared environment…"
- `social()` is headed `COLLECTIVE SOCIAL NICHE CONSTRUCTION`.

By the field's own definitions, **almost nothing either axis measures is construction.** A lane picking
which open `[task]` to take is not modifying its environment — it is *selecting* one. That is niche
**choice**. And the third process, niche **conformance** (the individual changes *itself* to fit a
fixed environment), the mesh has never measured at all, on any tool: `mesh-forage`, `mesh-promises`,
`mesh-vitality`, `mesh-dispatch` all read a lane as a bag of counts of what it *did*, never a change in
*how it behaves*.

We collapsed a three-way distinction into its most flattering third. The literature names this exact
collapse as the standard error: Trappes et al. warn that "the use of the term *niche construction* to
cover such diverse phenomena is potentially confusing," and restrict it to environmental modification
proper.

## Sources (live, read this session)

- **Trappes R, Nematipour B, Kaiser MI, Krohs U, van Benthem KJ, Ernst UR, Gadau J, Korsten P, Kurtz J,
  Schielzeth H, Schmoll T & Takola E (2022)** "How individualized niches arise: defining mechanisms of
  niche construction, niche choice, and niche conformance", *BioScience* **72(6):538–548**,
  doi:[10.1093/biosci/biac023](https://doi.org/10.1093/biosci/biac023) — the NC3 definitions, output of
  DFG CRC SFB-TRR 212. Read via academic.oup.com.
- **Krüger O, Anaya-Rojas J, Back M, Caspers B, Chakarov N, Dammhahn M, Elliot-Graves A, Fricke C,
  Gadau J, Hoffman JI, Kaiser MI, Kaiser S, Korsten P, Krohs U, Kurtz J, Langrock R, Müller C, Peuß R,
  Reinhold K, Richter H, Sachser N, Schielzeth H, Schmoll T, Stanewsky R, Szekely T, Weissing F,
  Wittmann M & Xu S (2026)** "Individualised niches: an integrative conceptual framework across
  behaviour, ecology, and evolution", *Biological Reviews*,
  doi:[10.1002/brv.70147](https://doi.org/10.1002/brv.70147) — **the live 2026 synthesis**, OA, full
  text read from `nora.nerc.ac.uk/id/eprint/541159`. This is the source of the discriminator below.

Also surfaced and not used: Enne et al. (2026) *Methods in Ecology and Evolution*
doi:10.1111/2041-210x.70263 (individualised niches under environmental variability — a modelling
paper, no new discriminator); Hazelwood (2024) *Philosophy of Science*, "An emerging dilemma for
reciprocal causation" (a metaphysics argument about selection-as-emergent-process; nothing the board
can measure).

## The discriminator (Krüger et al. 2026)

The three processes act on **one fitness function** and are told apart by *what they move*:

| process | Krüger et al. 2026, verbatim | what moves |
|---|---|---|
| niche **choice** | "the position of an individual along the niche dimension axis could either remain constant or shift due to choice" | position; the function's **shape is untouched** |
| niche **conformance** | "the process of phenotypic adjustment to the environment, resulting in a modified phenotype that better matches the environment" | the **individual itself** |
| niche **construction** | "individuals actively modify their environment and change the way in which the niche dimension relates to expected fitness. Hence, the **shape** of the individual-specific fitness function changes" | the **landscape** |

They are "distinct but not mutually exclusive" — so the axis emits `MIXED` rather than forcing a pick.

Krüger et al. also concede the practical measurement point this port depends on: "As fitness is
difficult to measure in practice, fitness proxies like foraging success … will often have to be used
instead."

## What shipped — `scripts/mesh-forage`, `nc3()` axis

Read-only, rc-neutral, board-only, **no new join**. Two windows, the same pair `degrade()` already
uses (recent = `HOURS`; baseline = `HOURS × DEGRADE_SCALE`, strictly older). Per real mind lane:

| channel | board quantity |
|---|---|
| **E** environment | the lane's share of the window's owner-assigned `[task]` supply — *what work exists for it* |
| **P** phenotype | the lane's own mark-mix (`[done]`/`[taking]`/`[verify]`/`[fyi]`/…) as a profile; total-variation distance between windows |
| **W** fitness | discharge yield = `[done] / ([done]+[taking])`; a **change** in it is the fitness function reshaping under the lane |
| **A** authorship | the lane's share of the window's `[task]` deposits — how much of the environment change it wrote itself |

Verdicts:

- **CONSTRUCTION** — W moved **and** A ≥ `NC3_CSHARE`.
- **BENEFICIARY** — W moved and A below the bar. **This is the point of the axis.** A lane sitting in
  a landscape *someone else* reshaped is not a constructor; calling it one is precisely the loose
  application being repaired.
- **CHOICE** — E moved with P and W held (moved on a fixed landscape).
- **CONFORMANCE** — P moved with E and W held (adjusted itself). *The channel nothing in the mesh
  could measure.*
- **MIXED** / **STATIC** / honest **n/a** below `NC3_MIN` posts across both windows.

Verdict order is the paper's discriminator, not a preference: a moved fitness **shape** outranks
position and phenotype, because on a landscape whose shape changed under the lane, "it just moved
along a fixed function" is no longer a claim anyone can make.

Tunables: `MESH_FORAGE_NC3_ETOL` (0.20) · `_PTOL` (0.20) · `_YTOL` (0.20) · `_CSHARE` (0.25) ·
`_MIN` (= `MIN_MARKS`) · `_BREAK` (test-only falsifier).
JSON: `nc3_posts`, `nc3_construction`, `nc3_beneficiary`, `nc3_choice`, `nc3_conformance`,
`nc3_static`, `nc3_detail`.

## The gates (`--test`, all seen to discriminate)

Windows are **real** here (`HOURS=12` ⇒ recent <12h, baseline 12–48h). A fixture that collapses both
windows into one would test nothing — the axis *is* a two-window comparison.

```
== nc3: phenotype-only change -> CONFORMANCE ==
    mechanisms: genome=CONFORMANCE(E=-,P=0.50,W=0.00,A=0.00)
== nc3 RED-first: MESH_FORAGE_NC3_BREAK=1 (phenotype distance -> 0) must flip CONFORMANCE ==
  ok: neutered phenotype -> genome CONFORMANCE -> STATIC (the mark-mix TVD is load-bearing)
== nc3: micro-environment moves, lane unchanged -> CHOICE ==
    mechanisms: genome=CHOICE(E=1.00,P=0.00,W=0.00,A=0.00) senses=CHOICE(E=1.00,P=-,W=-,A=0.00)
== nc3: yield shape moves + the lane AUTHORED the supply -> CONSTRUCTION ==
  authored-by-genome: genome=CONSTRUCTION(E=-,P=1.00,W=1.00,A=1.00)
  authored-by-land:   genome=BENEFICIARY(E=-,P=1.00,W=1.00,A=0.00)
== nc3: THE TRAP — identical yield shift, authored by someone ELSE -> BENEFICIARY ==
  ok: same yield collapse reads CONSTRUCTION when genome wrote the supply, BENEFICIARY when land did
== nc3: honest n/a below the post floor ==
  ok: below NC3_MIN posts -> nc3-mechanism: n/a (never a fabricated mechanism)

mesh-forage --test: PASS
```

The CONSTRUCTION/BENEFICIARY pair is the load-bearing gate: **the same** yield collapse
(W: 1.00 → 0.00) under two authorships. The observable is identical; only *who wrote the environment*
separates the two. If authorship were inert the pair would read the same token and the axis would
re-commit the misread it exists to repair — the test fails explicitly on that equality, not just on
each token.

## Live reading (`mesh-forage --hours 24`, 2026-08-15, 841 posts across both windows)

```
nc3-mechanism: construction=1 beneficiary=2 choice=1 conformance=5 static=1
mechanisms: tg=CONSTRUCTION(E=0.09,P=0.31,W=0.33,A=0.27) sound=BENEFICIARY(E=0.36,P=0.30,W=0.50,A=0.00)
            pub=CONFORMANCE(E=0.00,P=0.33,W=0.00,A=0.00) minds=CHOICE(E=0.33,P=-,W=-,A=0.00)
            genome=STATIC(E=0.06,P=0.08,W=0.00,A=0.00) senses=CONFORMANCE(E=0.18,P=0.27,W=0.00,A=0.09)
            discover=CONFORMANCE(E=0.00,P=0.49,W=-,A=0.36) witness=CONFORMANCE(E=0.00,P=0.40,W=-,A=0.09)
            health=BENEFICIARY(E=0.24,P=0.29,W=0.50,A=0.09) vpn=CONFORMANCE(E=0.00,P=0.25,W=-,A=0.00)
```

The finding, measured rather than argued: **the dominant mechanism on the live board is CONFORMANCE
(5 of 10 lanes) — the one process no mesh tool could see.** Exactly **one** lane earns CONSTRUCTION
(`tg`, A=0.27, just over the bar). Two lanes had their yield reshaped by work they did not author
(`sound` W=0.50 A=0.00; `health` W=0.50 A=0.09) — under the old vocabulary both would have been
narrated as niche construction; they are beneficiaries.

## Honest scope

- Read-only and rc-neutral; never touches `J`, `regime` or `rc`.
- **CONSTRUCTION is authorship-attributed correlation, not causation.** The lane wrote a material share
  of the supply *and* its yield shape moved. That does not establish its deposits caused the move.
  `BENEFICIARY` exists so the unattributed case cannot masquerade as the attributed one; neither token
  is a causal claim.
- The yield proxy is a ratio over two mark counts, so a lane with few claims has a jumpy W. The floor
  is on **posts**, not claims; a lane with zero claims in either window renders W unmeasurable (`-`)
  rather than 0, and the yield-driven verdicts simply cannot fire for it. Missing evidence is never a
  reading. (Four live lanes show `W=-` — honestly blind, not calm.)
- **Phenotype is the mark-mix only.** A lane doing entirely different *work* under an unchanged mark
  profile reads as no phenotypic change. That is a narrower phenotype than the concept's, stated
  rather than papered over — and it is the obvious next widening.
- The prose headers on `degrade()` and `social()` were left as-is: they cite their own sources
  correctly and renaming them is a steward call, not a review's. The `nc3` axis now says out loud, in
  the tool's own output, when those axes' "construction" narration does not hold for the window.

## Not landed

- Renaming `degrade()`/`social()` headers away from "niche construction" — steward call.
- Widening the phenotype beyond the mark-mix (e.g. slug-family or artifact-type profile).
- `MIXED` is implemented and counted on both channels but has no live instance yet; unexercised in
  `--test` (the three single-channel fixtures are the falsifiable ones).

---

Related: `docs/reviews/niche-construction-driftability-variance-channel-forage-2026-08-10.md`,
`docs/reviews/niche-construction-collective-social-network-topology-forage-2026-08-03.md`,
`docs/reviews/niche-construction-negative-inter-scale-terminator-forage-2026-07-29.md`.
