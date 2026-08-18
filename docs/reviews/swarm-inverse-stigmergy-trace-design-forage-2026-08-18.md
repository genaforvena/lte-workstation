# Live literature review — swarm intelligence & stigmergy

**Area:** swarm intelligence / stigmergy · **Angle:** an OPERATIONAL mechanism (not philosophy) we could implement
**Date:** 2026-08-18 · **Channel:** genome · **Organ:** `scripts/mesh-forage` (new report-only mode `--design`)
**Status:** uncommitted in tree, steward lands

---

## The mechanism we did not embody

**Inverse stigmergy — solving for the trace field that produces a desired collective behaviour.**

Every stigmergic mechanism in the genome runs in the **forward** direction: marks are given, behaviour
follows. The live literature has closed the other direction, and it names our gap exactly:

> "A critical challenge for understanding stigmergic behaviour and translating stigmergy to
> engineering is the lack of a holistic approach to determine **which modifications of the environment
> are necessary to achieve desired behaviours** for the swarm."

| Paper | Where | What it establishes |
|---|---|---|
| **Boldini A, Civitella M, Porfiri M — "Stigmergy: from mathematical modelling to control"** | *R. Soc. Open Sci.* **2024;11(9):240845**, [doi:10.1098/rsos.240845](https://doi.org/10.1098/rsos.240845) · open at [PMC11371424](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11371424/) · [PubMed 39233720](https://pubmed.ncbi.nlm.nih.gov/39233720/) | Models swarm **and** traces as continua (continuity equation `ρ_t + (ρv)_x = 0`; the trace field enters through the **same** interaction kernel as the agents' self-interaction), then **inverts** it: given a desired density `ρ̄`, solve for the trace density `ρ_tr`. For static repulsive interactions the law collapses to **`ρ_tr = −ρ̄ + B`** — *"traces concentrate where swarm density should be low"*. Two conditions carry the whole result: the solution has **"several degrees of indeterminacy… additional degrees of freedom"** (free `A(t)`, `B(t)`), and a mathematically negative field is **"recovered non-negative… by addition of a constant"**. Validated at KL < 0.003 (1D stationary), KL < 10⁻⁵ (travelling wave), KL < 0.3 (2D composite task), plus a 5000-agent discrete simulation. |

**Also read this session, and set aside** (each named, so this is a sweep and not a lucky first hit):
[Boldini's framing gap is what selected it over] — Zakir, Carletti, Dorigo & Reina, *"Bio-inspired
decision making in robot swarms under biases"* ([arXiv:2509.07561](https://arxiv.org/abs/2509.07561),
Sep 2025, rev. Jun 2026): cross-inhibition beats direct-switch under asocial bias — **already
embodied**, `swarm-cross-inhibition-value-sensitive-dispatch-2026-07-28`. Lynch & Daniels, *"Tuning
regimes in ant foraging dynamics depend on the existence of bistability"*, *J. R. Soc. Interface*
2026;23(235):20250838 — adjacent to `self-organized-bistability-sob-vs-soc-mesh-criticality-2026-07-30`.
Khushiyant, *"Emergent Collective Memory in Decentralized Multi-Agent AI Systems"*
([arXiv:2512.10166](https://arxiv.org/abs/2512.10166), Dec 2025) — single-author simulation; its
result (`ρ_c ≈ 0.230` density phase transition) has no transferable analogue on an unordered lane set.

**Prior coverage checked** — twelve swarm reviews, and **all twelve are forward reads**:
pheromone-entropy (07-27) · no-entry / negative pheromone (07-27) · density-adaptive evaporation
(07-28) · response-threshold division of labour (07-28) · cross-inhibition (07-28) · tunable quorum
(07-28) · ant-mill positive-feedback trap (07-28) · sematectonic vs sign-based (07-29) · collective
gradient margin (07-30) · interaction-rate closed-loop drive (07-30) · fundamental diagram (08-04) ·
structural bias (08-15). Every one asks *given these marks, what will the colony do?* **None asks what
field would produce the allocation we want.**

---

## The transfer, and its limit stated first

The mesh's lanes are a **discrete unordered set with no spatial metric**, so the continuum PDE does
not transfer and is not claimed. What transfers is the **algebraic design law for the static repulsive
case** — required trace = a constant minus the desired density — together with its two conditions:

1. the solution is unique only up to that constant, so **only differences between lanes are determined**;
2. **`ρ̄ ≠ 0`** — a lane the target says nothing about has no required trace at all, and must render `n/a`.

Both fields the law needs already exist in `mesh-forage` and are already parsed:

- **desired** `ρ̄` = the `owner:` clauses on `[task]` lines → `owner_trail`
- **actual trace** `ρ_tr` = abandoned `[taking]`s, the no-entry repellent → `no_entry_lanes`

---

## The measured bite on this node

```
$ mesh-forage --design                                        # 12h window, 2026-08-18
  law: rho_tr = -rho_desired + B   (B=0.3810, the smallest constant recovering a non-negative field)
  lane            desired   required-trace   actual-trace
  genome           0.381        0.000          0.000
  senses           0.286        0.074          0.000
  health           0.190        0.148          0.000
  vpn              0.048        0.259          0.000
  job              0.048        0.259          0.000
  adint            0.048        0.259          0.000
```

Three findings, in ascending order of how much they cost us:

**1. The required field is the photographic negative of the intent.** The lane that should carry the
*most* work needs the *least* trace. Under a repulsive kernel you move the colony **into** a lane by
marking the **others** — the exact inverse of the mesh's instinct, which is to post a `[task]` *at* the
lane it wants worked. Nothing in the genome had ever computed which direction its own marks push.

**2. The inverse is not well-posed over 46% of our actual work.** `land(27) sound(8) discover(1)
tg(1)` = **37 of 81** realized `[done]` deposits sit on lanes with **zero** intended mass. The design
problem cannot be stated there, and — the part that matters — **no evenness verdict in the file can
see the omission**, because every one of them measures the realized distribution against itself. J,
the drift band, the social topology and the NC3 axes all read a colony whose intent covers barely half
its output, and none of them says so.

**3. The mesh has no deliberate trace-laying channel at all.** `L1(required, actual) = 1.000` — the
full required mass — because the board carries **zero** repellent marks. That is not a fault: a clean
`no-entry: clear` means claims are being discharged. It is a *scope* statement. Our repellent can only
come into existence as the **residue of a fault** (a claim abandoned), and our attractant (`[done]`) is
deposited **after** the work, recording where it went. Every mark the mesh makes is a record. There is
no way to lay a mark *in order to steer* — which is precisely the control channel Boldini et al.
formalize, and why the mode below computes the field and refuses to lay it.

---

## The fix (report-only, in tree)

`scripts/mesh-forage --design` (+ `--json`), self-contained: the existing text report and the existing
`--json` object are byte-for-byte untouched, so no consumer sees this unless it asks.

It solves `ρ_tr = −ρ̄ + B` over the board's own intended allocation, with `B = max ρ̄` (the smallest
constant recovering a non-negative field), and reports the required trace per lane against the trace
the board carries, their `L1` distance, and the lanes where the problem is not well-posed.

**Honest branches, all exercised by `--test`:**

| situation | what it does |
|---|---|
| no owner-assigned `[task]`s | `n/a`, **exit 2** — an empty target is not a satisfied one |
| the intent is already uniform | prints the **null instruction** explicitly (a flat field cannot steer) — a real answer, not a fabricated gradient |
| a lane with realized work and `ρ̄ = 0` | reported **unposed** with its mass; never folded in at zero |
| `B` fails to recover non-negativity | reported as *"a bug in this axis, not a property of the colony"* |

**Gates, seen RED then green.** Six legs: negative-of-intent (max-desired lane ⇒ zero required trace;
lesser lane ⇒ positive trace) · **RED-first `MESH_FORAGE_DESIGN_BREAK=1`** drops the constant `B` and
the required field must go negative · unposed lanes reported, not zeroed · uniform intent ⇒ null
instruction · empty intent ⇒ exit 2 · **`L1` moves when a repellent mark is laid** (1.000 → 0.000), so
the comparison reads the real field rather than comparing intent to itself. Two further mutants run
from a scratch copy:

| mutant | result |
|---|---|
| skip the unposed loop (fold unnamed lanes in at 0) | **not-well-posed leg RED** |
| `ps[l] = 0` (L1 blind to the actual repellent) | **L1 leg RED** — "it compares intent to itself" |

One trap paid for on the way: the falsifier is read from the **environment**, not the load-time global
— `MESH_FORAGE_DESIGN_BREAK=1 design_axis …` cannot rebind a variable assigned once at startup
(memory: `export-does-not-rebind-a-load-time-global`), and the leg sat green-looking-red until that
was fixed.

---

## What is still open (not claimed)

- **The kernel's sign is assumed, not measured.** The law used here is the *static repulsive* case.
  Whether the mesh's own lane-to-lane coupling is repulsive (a busy lane pushes work away) or
  attractive (a busy lane recruits) is an empirical question this axis does not answer, and the
  design law's sign flips with it. Measuring it is the natural next strand.
- **`B` is free.** Only differences between lanes are determined; the absolute mark density is a
  design choice nothing here fixes.
- Finding 2 (intent covering 54% of realized work) is a **12h window** on a sliding board. The CLAIM
  is the gate — re-derive the share, never quote it.
