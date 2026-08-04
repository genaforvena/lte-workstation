# EVOLVABILITY — the offspring-distribution axis, applied too loosely

**Area:** artificial life & open-ended evolution
**Angle:** a foundational idea we may have MISread or applied too loosely
**Organ:** `scripts/mesh-ideate` — `evolvability_tally()` / `landing_organ()` (report-only)
**Date:** 2026-08-04

---

## The idea

**Evolvability** — "the capacity to generate adaptive variation" — is a property of a parent's
**offspring distribution**, not of the parent's own performance, novelty, or productivity.

- **Mengistu, Lehman & Clune**, *"Evolvability Search: Directly Selecting for Evolvability in order
  to Study and Produce It"*, GECCO 2016 — estimate an individual's future potential as **the
  behavioural diversity of its immediate offspring**, and select on that directly. The paper exists
  precisely because the indirect proxies (fitness, novelty, archive coverage) were *assumed* to
  imply evolvability and do not.
- **Katona, Franks & Walker**, *"Quality Evolvability ES: Evolving Individuals With a Distribution
  of Well Performing and Diverse Offspring"*, [arXiv:2103.10790](https://arxiv.org/abs/2103.10790)
  (2021) — draws the line this review turns on, verbatim from the abstract:

  > "While Quality Diversity aims to find an archive of diverse and well-performing, but potentially
  > genetically distant individuals, Quality Evolvability aims to find **a single individual with a
  > diverse and well-performing distribution of offspring**."

- **Live end of the literature:** Barnett, Meister & Rainey, *"Experimental evolution of
  evolvability"*, **Science 387(6736):eadr2756, 21 Feb 2025**
  ([doi:10.1126/science.adr2756](https://doi.org/10.1126/science.adr2756)) — evolvability is itself
  a trait under selection that can evolve. So it is something to **measure**, not a side effect to
  assume.

## What the mesh read too loosely

The literature lane already carries the **two neighbours** of this axis, and neither is it:

| instrument | landed | what it reads | blind to |
|---|---|---|---|
| `illum_pick()` (MAP-Elites) | 2026-07-28 | grid-cell **coverage** — an archive property | no parent attribution at all |
| `viability_tally()` (MCC) | 2026-07-29 | the parent's own **productivity** — "did this area land a finding in the window" | a **count**, no variance term |
| **`evolvability_tally()`** | **this review** | **spread of a parent's offspring** across organs | — |

Katona et al.'s sentence above *is* the QD-vs-QE distinction the mesh collapsed. An area that lands
8 findings **all into the same organ** scores maximally FERTILE under the minimal criterion and is,
in the literature's own terms, a **low-evolvability parent** — one trick, repeated.

## Measured on the live corpus (137 `docs/reviews` landings, 60d window)

Count and spread are **decoupled here, live** — same N, opposite E:

```
self-organized criticality  N=8  K=3  E=0.29 → mesh-criticality   |  Deleuze & Guattari  N=8  K=7  E=0.86
swarm & stigmergy           N=10 K=4  E=0.33 → mesh-forage        |  enactivism & 4E     N=10 K=10 E=1.00
edge of chaos / CAS         N=3  K=1  E=0.00 → mesh-criticality   (MCC: FERTILE(3))
```

The sharpest form, same run: **MCC reads all 18 areas FERTILE, `DORMANT: none`** — on today's corpus
the minimal criterion discriminates *nothing* — while evolvability splits the same 18 into **5
ONE-TRICK / 13 DIVERSIFYING**.

*(These are the tool's answer on the day, not constants. The corpus grows; every figure moves.
Re-derive by running it — never quote them back.)*

## Why it is cheap here

The field's standing objection to evolvability search is **cost**. Doncieux, Paolo, Laflaquière &
Coninx, *"Novelty Search makes Evolvability Inevitable"*, GECCO 2020
([arXiv:2005.06224](https://arxiv.org/abs/2005.06224)), open by noting estimation "is generally too
expensive to be directly used as selective pressure", which is why they chase it as a *side effect*
of novelty instead. That cost is **sampling offspring you have not got**.

The mesh's offspring **already exist as artifacts on disk** — one `docs/reviews` file per landing —
and their behavioural descriptor (*which organ the landing modified*) is already written down.
Nothing is simulated; the whole instrument is a read. Same shape as the MAP-Elites landing, whose
key observation was that the AREAS×ANGLES descriptor was already free.

And Doncieux et al.'s "inevitable" does not cover this lane either way: the draw here is
coverage+recency, **not** novelty search, and the live E ranges 0.00–1.00 across areas — plainly not
uniform.

## What shipped

`evolvability_tally()` — report-only, one line to `$SPLOG` beside `MCC-VIABILITY`. Per AREA over
`EVOL_WINDOW_D` (60d — evolvability needs offspring *history*; at viability's 30d most areas fall to
N<2):

- **N** = resolved landings, **K** = distinct organs among them, **E = (K−1)/(N−1) ∈ [0,1]**
  — 0 = every offspring the same organ (one-trick parent), 1 = every offspring a different one.
- **N<2 → honest n/a**, never a guessed 0 (one landing has no offspring *distribution*).
- **ONE-TRICK** flag = N ≥ `EVOL_MIN_N` (3) and E ≤ `EVOL_ONE_TRICK_E` (0.34).
- Same AREA buckets as `viability_tally` (`VIABILITY_MAP`) **on purpose** — the two lines are meant
  to be read side by side, since the finding is that they disagree.

`landing_organ()` resolves the offspring phenotype from **two sources, not a strong path with a rare
fallback**: live split is `name=29 body=108`, so the body read is the **majority** resolver, and the
tally prints the split on every line so it can never read as a silent default.

- `name` — the organ token the modern landing convention puts last in the filename before the date
  stamp. Exact, but only post-2026-07-25 landings carry it.
- `body` — the modal `scripts/mesh-X` mention inside the artifact. Covers the whole corpus (137/137
  resolve under the pair) at the cost of being **modal**.

**Weakest joint, stated:** a review that merely *discusses* another organ more often than the one it
landed in is misattributed. This biases K **downward** toward whichever organ a family of reviews
keeps citing — so **ONE-TRICK is the direction the instrument can manufacture** and DIVERSIFYING is
the safe verdict. Read one-trick as a prompt to look, not a fact.

## HELD (steward's, not shipped)

Using E to bias `illum_pick`. A one-trick area is **not** necessarily to be retired — it may be
legitimately *deepening* one organ — and that judgement is a selection change, not a report. Same
boundary the MCC landing drew.

## Gates (RED-first, all seen fail)

Suite: `mesh-ideate --test`, 19 legs, ~5.7s, green.

One fixture, two areas with **identical landing counts** and opposite offspring spread:

| leg | assertion |
|---|---|
| (a) | 3 landings into ONE organ → `ONE-TRICK … (N=3,K=1,E=0.00→mesh-criticality)` |
| (b) | 3 landings into THREE organs → `DIVERSIFYING … (N=3,K=3,E=1.00)` |
| (d) | a single landing → `thin(N=1)`, and **never** ONE-TRICK |
| (e) | descriptor split reported honestly (`name=7 body=1 unresolved=0`) |
| **thesis** | `viability_tally` on the **same fixture** reads **both** areas `FERTILE(3)` — count is blind to spread |
| n/a | absent corpus → `EVOLVABILITY n/a`, never a faked all-diverse |

Four mutants, each run from a scratch copy, each `exit=1` **for the right reason**:

| mutant | red leg |
|---|---|
| M1 `K := N` (drop the distinct-organ term) | (a) — both areas read E=1.00 |
| M2 drop the `N<2` no-distribution guard | (d) — N=1 lands in DIVERSIFYING with `E=` empty |
| M3 count the body path as `name` (silent fallback) | (e) — split reads `name=8 body=0` |
| M4 widen the one-trick threshold to 1.0 | (b) — everything reads ONE-TRICK |

---

**Sources**

- [Quality Evolvability ES — arXiv:2103.10790](https://arxiv.org/abs/2103.10790)
- [Novelty Search makes Evolvability Inevitable — arXiv:2005.06224](https://arxiv.org/abs/2005.06224)
- [Experimental evolution of evolvability — Science 387(6736):eadr2756](https://doi.org/10.1126/science.adr2756)
- [Evolvability ES: Scalable and Direct Optimization of Evolvability — arXiv:1907.06077](https://arxiv.org/abs/1907.06077)
- Mengistu, Lehman & Clune, *Evolvability Search*, GECCO 2016 (ACM DL 10.1145/2908812.2908838)
