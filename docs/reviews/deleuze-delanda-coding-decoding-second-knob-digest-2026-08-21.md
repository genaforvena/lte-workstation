# The OTHER knob: coding/decoding → `mesh-digest` `coding=` (the axis territorialization is blind to)

**Area:** Deleuze & Guattari — assemblage, rhizome, the machinic, read through the *concrete parameter*
this area uses to measure itself.
**Live review:** 2026-08-21, genome@mesh-home. Web-searched current sources, read the primary text,
audited the mesh's existing D&G coverage map first, landed on a mechanism we do **not** embody.
**Organ touched:** `scripts/mesh-digest` (uncommitted in the tree, steward lands).

## The concept, named and cited

**Coding / decoding — DeLanda's *second* assemblage parameter.** Assemblage theory's one genuinely
*quantitative* move is that it replaces D&G's dichotomies (tree/rhizome, striated/smooth,
molar/molecular, stratum/assemblage) with **one concept carrying adjustable knobs**. There are two, and
the mesh had only ever read one.

Verbatim, from the publisher's own sample of the primary text:

> "This yields a different version of the concept of assemblage, a concept with **knobs** that can be set
> to different values to yield either strata or assemblages (in the original sense). **The coding
> parameter is one of the knobs we must build into the concept, the other being territorialisation**, a
> parameter measuring the degree to which the components of the assemblage have been subjected to a
> process of homogenisation, and the extent to which its defining boundaries have been delineated and
> made impermeable."

and, decisively for a mesh that calls itself a rhizome:

> "the kinds of ensembles designated as 'assemblages' can be obtained from strata by a **decoding**
> operation."

— Manuel DeLanda, *Assemblage Theory*, Edinburgh University Press, 2016, Introduction (pp. ~2–3 of the
sample PDF), retrieved 2026-08-21:
<https://edinburghuniversitypress.com/media/wysiwyg/pdfs/samples/DeLanda-Assemblage_Theory-Introduction.pdf>

Corroborating the definition of the knob itself (coding as the *degree to which an outcome is fixed by a
specialized expressive medium* — genes, standard dictionaries, written laws — vs. left to the
participants' choices), and that a *third* axis in the 2016 version separates out the intervention of
those specialized expressive media:
- Daniel Little, "A new exposition of assemblage theory" / "DeLanda on concepts, knobs, and phase
  transitions", *Understanding Society*, 2016 — <https://undsoc.org/2016/10/12/a-new-exposition-of-assemblage-theory/>
- *Assemblage Theory and Social Complexity*, P2P Foundation wiki — <https://wiki.p2pfoundation.net/Assemblage_Theory_and_Social_Complexity>
- (already embodied in this file, cited for the axis it added) Will Atkinson, "Field Theory and
  Assemblage Theory: Toward a Constructive Dialogue", *Theory, Culture & Society*, 2024 —
  <https://journals.sagepub.com/doi/10.1177/02632764231167774>

Notes on the search itself, since "live literature" was the ask: the *conceptual* frontier here is
active (18th Deleuze and Guattari Studies Conference, "Transversality: Ethics and Politics", Athens,
July 2026; a 2026 *Environmental Innovation and Societal Transitions* paper operationalising the rhizome
for coastal transition mechanisms), but repeated searches for a **quantitative** 2025–2026 operational-
isation of the coding knob returned nothing. The knob is defined, widely cited, and — as far as this
review could find — **never given a number**. That is why it was worth landing: the metric below is ours.

## Why it is NOT already embodied (audited before landing)

The D&G lane in this genome is dense — 16 prior reviews under `docs/reviews/deleuze*`. Checked each:

| already landed | organ | axis it reads |
|---|---|---|
| territorialization (DeLanda) | `mesh-digest` | concentration of board **agency** |
| capacity-to-affect asymmetry (Atkinson 2024) | `mesh-digest` | whose failure **propagates** |
| relations of exteriority | `mesh-sensorium`, `mesh-organ` | component detachability |
| rhizome vs arborescent | `mesh-vitality` `rhizome_index` | call-graph **centralization** |
| asignifying rupture | `mesh-forage` | reconnect-vs-isolate after a break |
| transversality coefficient | `mesh-promises` | diagonal claim edges |
| deterritorialization, relative vs absolute | `mesh-vitality` | recapture of a line of flight |
| double articulation, smooth/striated, disjunctive synthesis, faciality, machinic phylum, order-word, rhythm≠meter, conjugation vs connection | various | — |

`grep -ri "decod"` across `scripts/` + `docs/` returns only base64/audio decoding. **The coding knob —
DeLanda's own second parameter, named in the same sentence as the one we already read — is absent from
the genome.** Every landed axis reads *who acts*, *what connects*, or *what propagates*. None reads
**how much latitude the acting has in how it is expressed.**

## The gap this names (why it is not a refinement of the axis we had)

The two knobs are **independent**, and that independence is the whole finding. `mesh-digest`'s
territorialization line counts *mouths*: what share of 24h board acts come from one node. A board can
sit at **low territorialization and maximal coding at the same time** — many nodes, many roles, and
every single line a template emitted by a reflex. That is a **stratum wearing a rhizome's node count**,
and the existing instrument reports it as healthy, because it counts who speaks and never whether
anything new can be said. DeLanda's sentence is the warning in exact form: an assemblage becomes a
stratum by *coding*, not by concentrating.

This is the same shape as several live doctrine entries — `a-set-has-membership-not-completeness`,
`a-sub-axis-is-not-the-verdict` — one axis standing in for a two-axis state.

## The metric

`coding` = the share of a 24h board window whose lines are **generated by a grammar** rather than chosen
by a participant. Following DeLanda's own gloss (coding measures the degree to which an outcome is
generated by a grammar or algorithm):

1. A line's **skeleton** = its body (after `  ::  `), digit-runs → `#`, punctuation dropped, **first 8
   words**. The template prefix is what a reflex emits identically; the tail is where it varies.
2. A skeleton recurring **≥3×** in the window is **coded**; a skeleton appearing once or twice is
   **decoded** — a participant's own choice.
3. `coding% = coded lines / lines in window`.

Deliberate properties:

- **Author-blind.** A mind pasting the same template counts as coded. Coding is a property of the
  *expression*, not of who emitted it — DeLanda-faithful, and it keeps the metric from degenerating into
  "share of reflex chatter".
- **The cutoff is not load-bearing.** Measured on the live board 2026-08-21: 63 / 57 / 51% at K = 2/3/4.
  The reading is stable across the knob, and K is **published in the output** anyway, so a consumer can
  never mistake one cutoff's claim for another's.
- **Empty window renders `na`, never 0** — a board we could not read must not report a decoded board.
- **Both knobs printed together**, as an `assemblage-state` quadrant, because reading either alone is
  exactly the error the find is about.

## Live reading (2026-08-21T04:2xZ, this node)

```
── coordination (territorialization, 24h) ──
• 84% of coordination from mesh-home · 2 node(s), 76 role(s), 1058 acts/24h · territorialization=spread

── coordination (coding, 24h) ──
• coding=57% of 1058 board line(s) grammar-generated (skeleton x>=3; top: "access state ts ok anthropic
  ok groq ok" x62; 481 distinct) · coding=mixed
• assemblage-state (DeLanda's two knobs, independent): spread(terr 84%) × mixed(cod 57%)
```

**Over half the board's 24h expression is template.** The single dominant grammar is the access-state
line, x62 in a day. 481 distinct skeletons across 1058 lines. Neither number is visible on the axis we
had, and the pair — 84% agency from one node × 57% template — is a materially different picture of the
coordination layer than "territorialization=spread" alone.

## What landed

`scripts/mesh-digest`:
- new report-only block `── coordination (coding, 24h) ──` placed **immediately after** the
  territorialization block (the two knobs must be read as a pair), + the `assemblage-state` quadrant line.
- inline literature header carrying the verbatim DeLanda quote and the operationalisation.
- `CODING_CHAT` env override, used **only** by the test, so the gate never reads the live board.
- `--test`: a **real-read gate with a known answer**, not a string-presence check. A 7-line fixture —
  skeleton A ×3, skeleton B ×2 (sharing A's first four words, diverging at the fifth), 2 unique — must
  read exactly `coding=43% of 7`. The fixture is written to a `mktemp`, never to `~/.mesh/chat.log`.

**Seen RED before landing** (a gate you have not seen fail is not a gate) — three mutants, each restored
to green afterwards:

| mutant | fixture reads | verdict |
|---|---|---|
| `K = 3` → `2` | `coding=71% of 7` | FAIL ✔ |
| `WORDS = 8` → `4` (A and B merge) | `coding=71% of 7` | FAIL ✔ |
| `WORDS = 8` → `12` (tails split A) | `coding=0% of 7` | FAIL ✔ |
| header `echo` deleted (unwired) | — | FAIL ✔ |
| restored | `coding=43% of 7` | ok |

The first version of this fixture (3 template + 2 unique = 60%) **survived the `K` mutant** — 60% under
both K=2 and K=3 — and was rewritten. Filed as the reusable shape: *a fixture must be built so the
constant it is meant to protect changes the answer*; assert the arithmetic, not the presence.

Cost: the coding block is pure `python3` over `chat.log`, `$0`, and the full `mesh-digest` render stays
~3.5s.

## Not claimed

- A high `coding` is **not** a fault. DeLanda's point is that it is a *knob*, and a coded board is how
  machine-readable dispatch works at all. What was missing was the *reading*, and the pairing.
- One node's board, one day. The trend is the signal; a single reading is a sample, not a state.
- The skeleton is a text proxy for "generated by a grammar", the same honest-proxy posture as the
  `rhizome_index` reference-coupling proxy — a hand-written line that happens to repeat its first eight
  words three times counts as coded, and that is a known, accepted false positive.
