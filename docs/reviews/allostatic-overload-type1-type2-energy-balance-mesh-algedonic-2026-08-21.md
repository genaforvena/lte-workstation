# Allostatic overload is TWO things, and every escape actuator in this mesh answers only ONE

**Area:** homeostasis · allostasis · ultrastability (Ashby, Sterling) — from the angle asked for:
**a foundational idea we applied too loosely.**
**Date:** 2026-08-21 · genome mind, mesh-home · **live** review (web search + read, not a fixed list)
**Landed in:** `scripts/mesh-algedonic` — `--overload-type` (read-only, on-demand, 0 behaviour change).

---

## The source

> **McEwen BS & Wingfield JC, "The concept of allostasis in biology and biomedicine",**
> *Hormones and Behavior* **43(1):2–15 (2003)**, doi:10.1016/S0018-506X(02)00024-7.
> Retrieved live 2026-08-21 (web search → the paper's own statement of the two overload types,
> corroborated across the Zenodo record 13504700 of the same paper, the *Journal of Mammalogy* 86(2):248
> restatement "Concept of allostasis: coping with a capricious environment", and the 2022 Frontiers
> Ecol&Evol re-examination `10.3389/fevo.2022.954708`).

McEwen & Wingfield split **allostatic overload** in two, by **energy balance** (E_g required vs E_o
obtainable), and the two halves have *opposite* prognoses:

| | condition | what follows |
|---|---|---|
| **Type 1** | E_g **>** E_o — negative energy balance | **triggers the emergency life-history stage.** The animal abandons its normal programme; that *lowers* allostatic load and restores positive balance. **Self-limiting**; the normal cycle resumes when the perturbation passes. |
| **Type 2** | load chronically high while energy is **sufficient or in excess** (social conflict, captivity) | **no negative balance → the escape response is never triggered.** Mediators stay elevated indefinitely. It "can only be counteracted through learning and changes in the social structure." Called *virtually unique to human society and captive animals*. |

## The misread, and it is ours

`scripts/mesh-algedonic` integrates the mediator side properly — `allostatic_load()` gives
`LOAD_NOMINAL/LOAD_WATCH/LOAD_OVERLOAD` from the rolling mean of the noisy-OR pain. What it cannot say
is **which overload**. And that is not a cosmetic gap, because **every escape actuator this mesh owns is
keyed to scarcity**: `mesh-resource-guard` (RSS/PSI/swap), `mesh-mem-guard` (MemAvailable),
`mesh-load-gate`, the `mesh-spend` hold, `mesh-pace`. That is the **Type 1 ladder, complete and healthy**.

Nothing anywhere reads the **other cell** — chronic pain *while* CPU, memory, load and the resource guard
all have headroom. In that cell **no gate has a trigger**, so the load has no path out *and no alarm*.
And this node is precisely the captive case McEwen & Wingfield name: its load is **self-imposed by its own
dispatch**, not imposed by scarcity. A bare `LOAD_OVERLOAD` sends the operator to the shed ladder — an
actuator with nothing to grip — which is the "an error message names a cause, not *the* cause" shape
applied to a whole family of remedies.

**Not already embodied** — checked before building:

| near neighbour | why it is not this |
|---|---|
| `allostasis-joint-dysregulation-mahalanobis…` (07-30) | multivariate *shape* of the mediator vector; still mediator-only, no supply axis |
| `homeostasis-gated-regulation-cryptic-storage-recovery-cost…` (08-19) | what a *recovery* leaves behind; says nothing about whether an escape can fire |
| `reactive-scope-wear-moves-the-threshold` → `scripts/mesh-stress` | the RSM ceiling **R/M** (Wright et al. 2023) — already fully landed, incl. r₁/r₂/r₃. It moves the *boundary*; it never asks whether the mediator's elevation has an exit |
| `homeostatic-coupling-vs-partner-access…` → `mesh-load-gate` | homeostatic *sharing* between agents |
| `rheostasis-defended-setpoint…` (07-27) | a scheduled set-point move |

`grep -rn 'Wingfield\|type 2 allostatic\|overload type' docs/ scripts/` → **zero** hits before this.

## What landed

`mesh-algedonic --overload-type` — reads the **supply side** beside the mediator side, each state file
against its **producer's own documented vocabulary** (verified against the source tools, not guessed):

| axis | file | producer | adequate | constrained |
|---|---|---|---|---|
| psi | `.psi.state` | `mesh-psi` | `CALM`, `BUSY` | `STALLED` |
| mem | `.mem-guard-state` | `mesh-mem-guard` | `QUIET` | `PRESSURE`, `HOG-TILT`, `CRITICAL` |
| load | `.loadavg-state` | `mesh-loadavg` | `LIGHT/STABLE/RISING/FALLING/SPIKE` | `OVERLOADED` |
| res | `.resource-guard-state` | `mesh-resource-guard` | `OK` | `WARN: …` |

`BUSY` is deliberately **adequate**: *working hard is not being starved*, and reading it as scarcity
would erase the Type 2 cell entirely (mutant M3 below).

Verdicts: `OVERLOAD_NONE` · `OVERLOAD_TYPE1` (names the constrained axis) · `OVERLOAD_TYPE2` ·
`OVERLOAD_UNKNOWN` (rc 2). **The evidence bar is asymmetric on purpose:** Type 1 is an *existential*
claim (one constrained axis witnesses it); Type 2 is a *universal* one (no supply axis constrained), so
only Type 2 carries a coverage floor (`OT_MIN_KNOWN=3` of 4). Missing / stale / unrecognised supply
state drops out of coverage and drags the verdict to UNKNOWN — **"adequate energy" inferred from unread
axes would mint the chronic-pathology verdict out of blindness.**

## Live reading on this node, 2026-08-21T01:1xZ

```
algedonic overload type: OVERLOAD_NONE
  mediator side: LOAD_WATCH (mean pain=0.385 over n=144, 4 sample(s) >= 0.60)   current pain=0.790 [STRESSED]
  supply side:   ENERGY_NEGATIVE  known=4/4  axes=psi:STALLED,mem:QUIET,load:FALLING,res:OK
```

**The branch is reachable, measured, not assumed.** Replaying the whole live tape (3209 pain samples,
rolling-144 mean): **897 of 3066 windows (29.3%) are `LOAD_OVERLOAD`**, 2169 `LOAD_WATCH`, none below
0.20; rolling mean min 0.299 / p50 0.358 / p90 0.589 / max 0.919. So this is not a threshold nothing
reaches.

**What cannot be claimed, and why:** *which type* those 897 past overload windows were is
**unrecoverable**. `algedonic.log` records the mediator side only, and `pressure.log` carries no
timestamp to join on. So there is no back-test here and none is implied — the axis types overloads
**from now on, when read**. The honest next step is a *swept* additive `energy=`/`ekn=` field on the
status line so a 03:00 Type 2 episode is legible after the fact; that touches every reader of the tape
and is deliberately **not** bundled into this landing.

## Gates — seen RED, then restored

`--test` grows 10 legs (NONE · TYPE1×4 · TYPE2 · UNKNOWN×4). Five mutants, each run from a scratch copy:

| mutant | leg that bit |
|---|---|
| M1 unknown psi token falls through to `adequate` | `psi:?` / coverage 3 → both RED (it minted `TYPE2` at 4/4) |
| M2 coverage floor `3 → 1` | thin-coverage and stale-supply legs → RED (`TYPE2` from 2 axes and from 1) |
| M3 `BUSY` read as scarcity | `chronic+adequate -> TYPE2` → RED (got `TYPE1`) |
| M4 mem-guard matched by substring `*PRESSURE*` | `HOG-TILT` and `CRITICAL` legs → RED (both fell to `TYPE2`) |
| M5 supply read with `cat` instead of `fresh` | stale-supply coverage 1 → RED (got 2) |

The section's own `ok:` line is gated on the section's fail count, so a red leg can no longer sit under a
green summary.

**Read-only, on-demand, never in the 10-min path, never escalates, never routes work. Uncommitted —
steward lands from the tree.**

## Sources

- [McEwen & Wingfield 2003, Horm Behav 43(1):2–15 (Zenodo record)](https://zenodo.org/records/13504700)
- [Concept of Allostasis: Coping With a Capricious Environment, J Mammalogy 86(2):248](https://academic.oup.com/jmammal/article/86/2/248/890668)
- [Allostasis revisited: a perception, variation, and risk framework, Front Ecol Evol 2022](https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2022.954708/full)
- [Wright et al. 2023, A mathematical representation of the reactive scope model (the neighbour already landed in `mesh-stress`)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468437/)
