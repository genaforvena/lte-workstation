# VSM / management-cybernetics live review — REQUISITE VARIETY MUST HOLD AT **PEAK**, NOT AVERAGE LOAD

**Date:** 2026-08-19 · **Lane:** LITERATURE (live review), idea-queue · **Landed in:** `scripts/mesh-tell`
(`--pressure`, report-only) · **Status:** uncommitted in the tree, steward lands.

## The search (what "live" meant here)

The genome is deep in this area already — 31 VSM/second-order reviews, `mesh-algedonic` carries Beer's
algedonic channel and Pérez Ríos' pathology list, `mesh-vitality` carries S1–S5 + residual variety,
`mesh-tell --pressure` carries variety overflow. So the sweep was explicitly for ground we have **not**
been on. Two directions came back dry and are recorded as such:

- **Team Syntegrity / syntegration** (zero mentions in the genome — genuinely unexplored) has **no live
  literature**: the sweep returned Beer's own *Beyond Dispute* (1994), Truss & Leonard, and Metaphorum's
  standing page. Nothing 2025–2026. Unexplored ≠ live.
- **VSM applied to WSN / edge / sensor networks** — searched directly, twice. There is no published
  VSM↔sensor-network work at all; the two literatures do not cite each other. The cross-domain transfer
  the task asks for has to be *made*, not *found*.

Where the area **is** live is VSM re-applied to **agent fleets**, and that is where this landed.

## The concept we did not embody

> **Telukunta, Lilis & Baron, "The CASE Framework: A Multi-Disciplinary Control Architecture for
> Governing Enterprise Agentic AI", arXiv:2608.10153 (submitted 10 Aug 2026)** — Layer 3, *supervisory
> cybernetics for human-agent teams*.

It restates Ashby/Beer as an **engineered channel with measured capacity**:

- ineq. (4) `H(O) ≥ H(A) − H(A|O)` — oversight entropy vs the agent behaviour not already visible to it;
- ineq. (5) `V_human × G ≥ V_agents`, where `G` is the engineered gain (triage, semantic summarization,
  tiered escalation, exception-only routing);
- and the constraint we did not have, **verbatim**: *"with the inequality required to hold at **peak
  variety, not average load**"*, because *"agent behavioral variety grows combinatorially with agent
  count, tool access, and autonomy level, while human cognitive variety is fixed"*;
- *"Oversight is an engineered channel with measured capacity … treats any gap as a hard deployment
  blocker, exactly as it would treat an unmet load requirement in physical infrastructure."*

We embody the algedonic channel (`mesh-algedonic`), recursion (`mesh-vitality`), oversight
meta-monitoring (`mesh-reflex-health`, `mesh-doctor`) and the overflow *idea* (`mesh-tell --pressure`).
We did **not** embody the peak-vs-average constraint anywhere.

## The gap it fills — measured, not inferred

`mesh-tell --pressure` (landed 2026-08-15 off Neese & Penabaz-Wiley's *variety overflow*) rendered a
band from the **median gap alone**:

```awk
printf ... (mg<ref ? "overflow-risk" : "paced")
```

The `burst<5m` column was computed, printed, and **never read by the verdict** — decorative. So a pane
poked eight times inside twenty minutes and then left alone for hours read **PACED**: the median
averages the burst away, which is exactly the "average load" sizing CASE says an oversight channel may
not be given. This is the same shape as the doctrine's own *sample-is-not-the-interval* rule, inverted:
there a narrow window missed the sustained state; here a wide statistic misses the sustained burst.

**Live at landing** (`~/.mesh/tell-wal.log`, 1174 arrivals / 4.8d — a sliding window, so a current
answer, not a reproducible population). Four of thirteen windows carried a calm verdict over a burst
below the cited 15-min reference:

| win | arr | med_gap_min | peak8_gap_min | burst<5m | verdict before | verdict now |
|---|---|---|---|---|---|---|
| genome | 338 | 13.8 | 0.5 | 32% | overflow-risk | overflow-risk(med+peak) |
| senses | 139 | 31.8 | 10.9 | 25% | **paced** | overflow-risk(peak) |
| sound | 115 | 30.0 | 12.9 | 10% | **paced** | overflow-risk(peak) |
| adint | 48 | 62.3 | **2.7** | 34% | **paced** | overflow-risk(peak) |
| wake | 34 | 45.2 | 4.3 | **39%** | **paced** | overflow-risk(peak) |

`adint` is the clean case: a median of 62.3 min reads as an hourly, humane pace, while its tightest
sustained run put eight prompts into the pane at 2.7 min apart. `wake` is the sharper one — a 39% burst
share was sitting **in the row** saying so, and the verdict could not see it.

## What was built (report-only, nothing gates a send)

`scripts/mesh-tell`, `wal_pressure()`:

- new `peak<MIN_N>_gap_min` column = the **tightest sustained run**: the shortest span holding `MIN_N`
  consecutive arrivals, rendered as its effective inter-arrival gap;
- **no new threshold** — this is the point. It asks the *same* cited 15-min question (Iqbal & Horvitz,
  as quoted by Neese & Penabaz-Wiley) over the *same* minimum sample the median leg already requires.
  A peak leg with its own tuned constant would just be a second knob;
- a single tight **pair** cannot move it (`MIN_N` arrivals must fit inside the run), so a retry storm
  is not a rate;
- the fold **names its winner**: `overflow-risk(med)` = a chronic pace, `overflow-risk(peak)` = a burst,
  `overflow-risk(med+peak)` = both. A bare max-fold would efface which claim was made
  ([[max-fold-effaces-the-disjunction]]).

## Gates (each seen RED first, from a scratch copy)

| leg | asserts | mutant that turns it RED | seen |
|---|---|---|---|
| 9 | a median-CALM window (med 180.0) with 8 arrivals 2 min apart reads `overflow-risk(peak)` | `hi=0` — the pre-CASE median-only verdict | RED |
| 9a | the fixture *is* median-calm (`burstwin 16 180.0`) — otherwise the leg proves nothing | (self-guard: a leg that cannot show what it excludes) | — |
| 10 | the fold names its winner: chronic → `(med…)`, median-calm burst → never `(med` | verdict collapsed to a bare `overflow-risk` | RED |
| 11 | ONE 90s pair among hourly arrivals stays `paced` | peak computed as the minimum single gap | RED |

Control: unmutated copy green (`smoke-test: ok`), rc=0.

## Honesty constraints carried forward

The three from 2026-08-15 still hold and the peak leg does not weaken them: `level=off` renders n/a and
never a calm zero; the reference is cited, not tuned; the claim is arrival pressure **at the pane**, not
goal interference. One added: below `MIN_N` the peak is `n-a` and the verdict says `paced(med; peak
blind)` rather than passing a blind leg off as a pass.

## Held (deliberately not built)

CASE's *"any gap is a hard deployment blocker"* — the gating half. The mesh has now measured the peak
for exactly one run; turning a report-only axis into something that refuses or delays a send is a
change to what gets delivered, and the doctrine's own order is measure first. `mesh-dispatch` already
holds on pace/idle/thermal; wiring a peak-pressure hold belongs to a later, separately-argued step.

## Sources

- Telukunta, Lilis & Baron, *The CASE Framework*, arXiv:2608.10153, 10 Aug 2026 — https://arxiv.org/abs/2608.10153 (full text read: https://arxiv.org/html/2608.10153v1)
- Neese & Penabaz-Wiley, *The Requisite Variety of Presence*, Enacting Cybernetics 3(1):2, doi:10.58695/ec.20 (the axis this corrects)
- Pérez Ríos, *Models of organizational cybernetics for diagnosis and design* / VSMod® — https://www.udc.es/export/sites/udc/goberno/_galeria_down/vepes/documentos/ORGANIZATIONAL_CYBERNETICS_PEREZ_RIOS.pdf_2063069239.pdf (channel/transducer pathology list; already partly embodied in `mesh-algedonic`)
- Beer, *Beyond Dispute: The Invention of Team Syntegrity* (1994) / Metaphorum — https://metaphorum.org/syntegration (the dry direction, recorded above)
