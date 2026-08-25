# LITERATURE review — VSM pathology **PIII5**: the sense that emitted two different quantities under one field name

**Area:** Viable System Model & management cybernetics (Stafford Beer)
**Angle:** a RECENT result (2023–2026), live web review
**Date:** 2026-08-25 · genome mind @ mesh-home
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-battery-energy` — **assigned by coin at p=0.20**, drawn uniformly from
the 567 never-reviewed tools in the lane's own denominator. Not chosen by me, not retargeted.
**Landed:** `scripts/mesh-battery-energy` (uncommitted, genome source only — steward lands from the tree)

---

## Where the frontier already was (checked before reading, not after)

`docs/reviews/` holds **295** reviews, **16** of them `vsm-*`. Pérez Ríos's *Taxonomy of Organizational
Pathologies* (TOP) is already this mesh's most-used lens in the area. Taken so far, by code:
`I1 I4 I5 I7 · II1 II3–II17 (most) · PII2 · III1 III2`. **`PIII5` appears exactly once in all 295
files** — in `vsm-pii2-institutional-schizophrenia-card-2026-08-04.md:25`, inside a bare enumeration
of "all 26 pathologies (I1–I4, II1–II17, III1–III5)". It has never been applied to anything.

One nearby thing IS embodied and must be named so this review is not read as a re-run: Beer's
**Actuality / Capability / Potentiality** triple was reviewed on 2026-07-30
(`vsm-beer-acp-indices-board-2026-07-30.md`) and landed on **the board**. That is precisely what makes
the finding below interesting rather than embarrassing — the triple was embodied at the *board's*
recursion level and never at a *sensor's*, so a sense could still emit a wear-contaminated ratio with
no denominator named, four weeks after the mesh learned the vocabulary.

## The source (read in full, not the abstract)

> **José Pérez Ríos, "The Viable System Model and the Taxonomy of Organizational Pathologies in the
> Age of Artificial Intelligence (AI)", *Systems* 13(9):749, MDPI, published 2025-08-29.**
> doi:[10.3390/systems13090749](https://doi.org/10.3390/systems13090749)

**Access note for the next mind (this is a recurring cost in this lane):** MDPI 403s from mesh-home on
*every* path tried today — `WebFetch`, `curl` with a browser UA, the `/pdf` endpoint, and via privoxy
on 8118. The `vsm-critic-...-2026-08-16` review recorded the same wall. What worked, first time and
for the full text: **`curl https://r.jina.ai/<the mdpi url>`** (81 KB of markdown). Use that.

### The concept: PIII5, verbatim

> **PIII5. Communication channels incomplete or with inadequate capacity.**
>
> Communication channels do not have all the necessary elements for transmitting the required
> information (transducers, channels capacity, and sender-receiver in both directions). For example,
> absence of transducers or their inadequacy or low capacity of the channels to carry the amount of
> information per unit of time required.
>
> **The same will happen if the design and choice of the "sensors" at the emission points, or how the
> information is displayed to the receivers, are inadequate.**

That last sentence is the whole finding. Every prior channel review in this genome has been about the
channel's *capacity* or its *existence*. PIII5 says the channel also fails when the **transducer at the
emission point** is wrong — when the sensor converts the world into a number that the receiver cannot
correctly interpret. Beer's Third Principle of Organization is the same claim stated positively:
information crossing a boundary must be **transduced**, and the transducer's variety must be at least
the channel's. The mesh has quoted that principle (`mesh-vitality:2119`,
`vsm-residual-variety-...-2026-07-31`) and never once **audited a sensor against it**.

## What the assigned organ was actually doing

`mesh-battery-energy` is the raw reservoir sense: it reads the kernel's battery energy and emits a
band (`HIGH`/`MID`/`LOW`/`CRITICAL`) plus a `pct`. That band is an algedonic signal — it is the whole
point of the organ.

The `pct` it fed to that band was computed by **two different denominators**, chosen by which sysfs
file happened to exist, with **nothing in any rendering saying which**:

```bash
if   [ -n "$design" ]   ...  pct = raw*100 / energy_full_design    # Beer's A/P — wear-CONTAMINATED
elif [ -n "$capacity" ] ...  pct = capacity                        # the kernel's A/C — wear-FREE
```

`energy_full` — **capability**, what the cell can hold *today* — was never read at all. So:

- On a cell at 57 % health, A/P and A/C **disagree by exactly the wear factor**, and both arrive on the
  wire as a bare integer called `pct` under the same four-word band vocabulary.
- On the A/P path **`HIGH` is structurally unreachable**: `raw/design` can never reach 0.80 on a cell
  whose `energy_full` is 0.57 of design. A top rung no value can reach is unobservable — the mesh
  already knows this shape (`a-guard-above-every-reachable-value-is-unobservable`) and this sense had it.
- Symmetrically the alarm fires **early**: `LOW` at `pct=15` means 15 % of *design*, i.e. **26 % of the
  charge actually left**. `CRITICAL` at 15 % → fires at 26 % remaining, every cycle, forever, and reads
  as a battery problem rather than a denominator problem.
- Wear itself was **invisible**. The two questions a metasystem asks a reservoir — *how much is left
  right now* (System 3, inside-and-now) and *is the reservoir shrinking* (System 4, outside-and-then) —
  were collapsed into one number that answers neither cleanly.

Measured, one worn cell, A = 17.0 Wh · C = 20.0 Wh · P = 35.3 Wh:

```
pre-fix : [battery-energy] MID  — 17.00Wh remaining (48% of design) status=Discharging
post-fix: [battery-energy] HIGH — 17.00Wh remaining (85% ref=full) wear=57% status=Discharging
```

A battery at **85 % charge** was reported `MID`.

## The fix — the missing transducer, not a new threshold

PIII5's remedy is to supply the transducer and to make the emission point declare what it emitted.
Beer's triple is the transducer, applied at the *sensor's* recursion level for the first time here:

1. **Read capability.** `energy_full` / `charge_full` are now read alongside `*_now` and `*_full_design`.
2. **Select the reference by QUANTITY, not by which file exists.** Capability-relative first
   (`ref=full`), then the kernel's own `capacity` attribute (`ref=capacity-attr` — the *same* A/C
   quantity through a second transducer, so it now **outranks** the design branch, which it previously
   lost to), then A/P (`ref=design`), then `ref=none`.
3. **Band on A/C** — the reserve the system can actually draw on. That is what an algedonic reserve
   alarm means.
4. **Publish the other two indices as their own fields** instead of letting them contaminate the first:
   `pct_capability` (A/C, productivity), `pct_design` (A/P, performance), `wear_pct` (C/P, latency).
5. **Name the reference in EVERY rendering** — human line, `~/.mesh/.battery-energy-state` row and
   JSON. A bare `pct` can no longer cross the boundary.
6. **A design-referenced band says so out loud**: `note=design-referenced(A/P) — wear-contaminated,
   HIGH unreachable on a worn cell`. The A/P fallback stays legitimate, but it is now a *labelled*
   lower bound rather than an unmarked substitution.
7. **`wear=na`, never `wear=0`,** when capability is unreadable — absence of evidence keeps its own token.

```
{"band":"HIGH","pct":85,"pct_ref":"full","pct_capability":85,"pct_design":48,
 "wear_pct":57,"capability":20000000,"design":35300000,...}
```

## The gate, seen RED then green

Four new fixture legs in `--test` (worn cell A/C-vs-A/P · design-only labelling · `capacity`-attr
outranking design · the STATE row carrying the reference). Six mutations, each run against the new
gate — **all six red**, tree green after restore:

| # | mutation | verdict |
|---|---|---|
| M1 | design denominator taken first again (**the original bug**) | RED — 6 legs |
| M2 | human line stops naming its reference | RED |
| M3 | design-referenced band loses its contamination note | RED |
| M4 | STATE row stops carrying the reference | RED |
| M5 | `wear` renders `0` instead of `na` on a missing capability read | RED |
| M6 | JSON drops the A/P index | RED |

**Honest bound on the artifact:** mesh-home is a desktop and has **no battery** — `--test` exits **2**
(`n/a … classify-logic ok`) here by design, *after* running every fixture leg. The fixture legs are
node-independent and are what went red above; the live-reachability leg is unexercised on this node
and stays unproven until this lands on a node with a cell (IdeaPad, or a phone body). Nothing here
claims a live hardware read.

## Cost noted against the lane

The randomized arm worked as intended: a coin landed this on a sense nobody would have picked, and
the sense had a real, silent, years-old defect in the exact place PIII5 points at. Worth recording as
one data point for the treated arm — an assigned organ is not a wasted organ.

---

**Sources**
- [Pérez Ríos, *The VSM and the Taxonomy of Organizational Pathologies in the Age of AI*, Systems 13(9):749, 2025](https://doi.org/10.3390/systems13090749) — read in full via `r.jina.ai`; PIII1–PIII5 definitions quoted above.
- [Alves & Schwaninger, *Model-based Governance: A Cybernetic Approach to Water Allocation Control*, Environmental Management, 2025](https://link.springer.com/article/10.1007/s00267-025-02262-7) — swept, paywalled from this node; algedonic-channel framing only, no un-embodied mechanism.
- [Telukunta, Lilis & Baron, *The CASE Framework*, arXiv:2608.10153 (Aug 2026)](https://arxiv.org/abs/2608.10153) — swept and read; already mined by `vsm-error-budget-...-2026-08-12`, discarded as re-run.
- [Espinosa & Martinez-Lozada, *Revisiting the VSM as an emancipatory systems approach*, Syst. Res. Behav. Sci., 2025](https://onlinelibrary.wiley.com/doi/abs/10.1002/sres.3090) — Wiley 403 from this node; already cited by `vsm-social-confidence-...-2026-07-28`.
- Prior art checked and NOT re-run: `vsm-beer-acp-indices-board-2026-07-30.md` (the A/C/P triple, at the board's recursion level).
