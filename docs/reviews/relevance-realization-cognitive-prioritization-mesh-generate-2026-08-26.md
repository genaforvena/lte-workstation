# Relevance realization: cognitive prioritization (β) as the mesh's missing *composition* knob

**Area:** relevance realization & the frame problem (Vervaeke)
**Target organ:** `scripts/mesh-generate` (assigned by coin, p=0.20, drawn uniformly from the 560
never-reviewed tools in the lane's own denominator — not chosen by me, not chosen by the lane)
**Arm:** treated (assigned)
**Date:** 2026-08-26 · **Window:** genome
**Outcome:** APPLIES — mechanism named, cited, and shipped to the assigned organ (uncommitted, in-tree)

---

## 1. The mechanism

**Cognitive prioritization (CP)** — the third of the three opponent-processing constraints in
Vervaeke, Lillicrap & Richards, *"Relevance Realization and the Emerging Framework in Cognitive
Science"*, **Journal of Logic and Computation 22(1):79–99, 2012**
([PDF](http://contrastiveconvergence.net/~timothylillicrap/files/articles/relevance%20realization%20as%20an%20emerging%20framework%20in%20cogsci.pdf)),
Table 1, third row:

| internal economic property | external interactional property |
|---|---|
| cognitive scope · compression ↔ particularization · `w_ij = −η ∂J/∂w − α·w_ij` | applicability: general ↔ special purpose |
| cognitive tempering · TD learning ↔ inhibition of return | projectability: **exploiting ↔ exploring** |
| **cognitive prioritization · cost function #1 ↔ cost function #2 · `J₁,₂(β,α) = β⁻¹·J₁(α,·) + J₂(α,·)`** | flexible gambling: **focusing ↔ diversifying** |

The operational claim, quoted from §4.3 (*"The problem of flexibly gambling"*):

> "Whereas the internal economic constraints we call CS and CT had to do with how cost functions might
> be heuristically optimized, cognitive prioritization (CP) has to do with **the structure and
> prioritization of cost functions**. In short, one of the things which allows agents to be truly
> successful in the world is adapt not only their behaviour to suite a given task, but also **to adapt
> the sorts of tasks they are interested in optimizing**."

and the dial itself:

> "Betting should be flexible because, for instance, **the scarcity of one's internal reserves ought to
> cause a trade between focusing and diversifying as betting strategies.** For example, if an agent is
> very thirsty it will tend to gamble all of its efforts on getting water, i.e. it will focus its wagers
> on this project. As soon as thirst is satiated though, the agent will begin to pursue a diversity of
> problems. … agents ought to 'care' differentially about the environment because **they run on
> batteries** [Montague]."

Vervaeke's own footnote 3 (Zachary Irving) makes the knob explicit: with ten cost functions rather than
two, **"when beta gets very low, a learning system looks very specifically at food seeking, at the cost
of all those other activities that are potentially relevant."** β is a *composition* parameter — it does
not change how much the agent does, it changes **what the agent's effort is composed of**.

The frame-problem tie is the whole point of the paper: relevance is *never explicitly computed*
("relevance is never explicitly calculated by the brain at all"), it **emerges** from balancing these
economic constraints — which is why CP is a mechanism we can implement rather than a definition we would
have to presuppose. Live-literature context: the framework is still under active argument, notably
Jaeger et al., *"Naturalizing relevance realization: why agency and cognition are fundamentally not
computational"*, **Frontiers in Psychology 15:1362658 (2024)**
([link](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full)), and
Andersen, Miller & Vervaeke, *"Predictive processing and relevance realization: exploring convergent
solutions to the frame problem"*, **Phenomenology and the Cognitive Sciences**
([link](https://link.springer.com/article/10.1007/s11097-022-09850-6)). The Frontiers paper's thesis —
that RR *cannot* be an algorithm — is precisely the claim this patch tests from the cheap end: CP's
β is the most nearly-mechanical of the three constraints, so if any of RR ports to a shell reflex, it
is this one.

## 2. What we did NOT already embody — and the proof it is a gap, not a duplicate

We already run opponent processing on **two** axes, so the honest finding has to be sharper than
"we lack opponent processing":

| axis | where it already lives | Vervaeke row |
|---|---|---|
| RATE | `mesh-pace` — antagonistic cold-shrink / hot-stretch branches, read by `--control-mode` | cognitive **tempering** |
| GENERATION novelty | `mesh-ideate` — a 30-day decaying repellent played against an attractant | cognitive **tempering** (an inhibition-of-return trace, exactly as §4.2 describes) |
| **SELECTION composition** | **nothing** | cognitive **prioritization** ← the gap |

The gap is load-bearing, and it was already measured from the other side. Memory
`every-shed-actuator-is-keyed-to-scarcity` (2026-08-21) records that **every** escape/shed actuator on
this node — `mesh-resource-guard`, `mesh-mem-guard`, `mesh-load-gate`, the `mesh-spend` hold,
`mesh-pace` — fires on resource scarcity and each one modulates **how much** work happens. Not one of
them modulates **which** work happens. That is a complete Type-1 allostatic ladder and a missing
composition knob, and the memory's own conclusion is that the remaining cell "discharges only through
learning and changes in the social structure: a dispatch/pace **POLICY** change, never an actuator."
CP *is* that policy change, arriving from the literature side.

`mesh-generate` is where the gap bites, because it is the mesh's relevance-realization organ in the
literal sense: it decides **which single open idea buys the next paid worker slot**. Before this patch
its selector was FIFO — plus one narrow re-rank that fires only when the FIFO head is itself a `STUDY`
idea (`yield_score = (done+1)/(queued+2)`). It read no reserve signal of any kind: `MESH_BACKLOG_MIN`
is a fixed 3, and `grep -n "spend\|pace\|budget\|scarc" scripts/mesh-generate` returned only the
constant. A mesh at 5% of its spend window and a mesh at 95% picked the same next idea.

The queue's own census shows what that costs — the lifetime composition of the lane, by declared kind:

```
1405 LITERATURE    80 DECAY    76 CONNECTION    54 REFLEX    24 STUDY    ... 2 VERIFY
```

95% divergent exploration (J₂), ~5% self-repair (J₁), *at every reserve level*. Under scarcity the mesh
thinned that mixture uniformly instead of narrowing the frame onto the work that keeps it viable.

## 3. What shipped — `scripts/mesh-generate`

A scarcity-dialed β on the pop, sitting above the existing STUDY re-rank.

**β is read, not invented.** No new threshold, no new constant, nothing calibrated by hand: the reserve
reading is the spend governor's own arithmetic. `mesh-pace --eff-gap <base>` returns `MIN_GAP` when the
paid window is cold, `base` when the burn is unknown or the reserve arm is off, and `base × burn_mult`
(the operator-tuned 1.5/2/3 staircase) only once the burn is hot. So β = base/eff_gap and the entire
predicate is one inequality:

```
scarce  ⟺  eff_gap > base  ⟺  the governor is actively stretching itself
```

Every degenerate path lands on NOT-scarce, i.e. on today's exact behaviour: `mesh-pace` absent,
unreadable, non-numeric output, reserve arm disabled, burn unknown, `MESH_PACE_GAP` unset or 0.
Fail-open by construction — this can be silent, it can never stall the lane.

**It reorders one slot and never filters.** When scarce, an already-open J₁ idea
(`DECAY`/`REFLEX`/`VERIFY`/`ESCALATE` — the mesh repairing itself) takes the slot from the FIFO head.
The passed-over idea is *not consumed*: it stays `[ ]` and gets the next abundant cycle. If no viability
idea is open, the head keeps its slot. Nothing is dropped, no class is starved, and FIFO order is intact
the moment reserves recover — same shape as the study-yield re-rank, which also only ever reorders.

**The allowlist fails in the safe direction, and it is widenable from evidence.** A viability class we
forgot to list fails toward *no promotion*, i.e. toward plain FIFO — where we already were — never toward
a dropped idea. Per the doctrine rule about exclusion allowlists failing toward silence: the failure
direction here is a no-op, not a silence. And a scarce cycle that finds nothing to promote logs the
head's own **declared** kind token (`kind=LITERATURE`), so the classes we are actually passing over are
readable in `~/.mesh/generate.log` and the set can be widened from measurement instead of guessing.
Every promotion is logged unthrottled.

## 4. Verification

`--test` gained four arms, and **all four were driven RED by mutation before being accepted green**:

| mutant | arm that caught it |
|---|---|
| `cp_scarce` always false (focus never fires) | `scarce reserves did not promote viability work over the FIFO exploration head` |
| `cp_scarce` always true (focus unconditional) | `abundant reserves must leave FIFO order untouched — the focus fired with no scarcity` |
| promotion returns the head instead of the viability line | same scarce arm |
| the loud log line deleted | `cp-focus fired silently — every application must be loud` |

The arms assert, in order: scarce → J₁ promoted **and** the passed-over J₂ idea still `[ ]` (proves
reorder, not filter) **and** the `[~]` flip lands on the promoted line, not the head's line number;
abundant → FIFO head keeps its slot; **no seam at all** in a hermetic `HOME` with no `MESH_PACE_GAP` →
the live probe fails open to abundant; scarce with no viability idea open → FIFO unchanged and the
passed-over kind logged.

```
$ bash scripts/mesh-generate --test
smoke-test: ok (generation dry-run + cap_rotation_saturated gate + study-yield ledger/priority verified:
ledger honest counts, yield beats FIFO among STUDY, non-STUDY head untouched; cp-focus fires only when
scarce, promotes viability without consuming the passed-over idea, and fails open on an unreadable reserve)
```

**Live reading on this node, measured in the same run as this claim** (2026-08-26):

```
MESH_PACE_GAP=1800   mesh-pace --eff-gap 1800 → 60      (cold floor)
predicate: eff(60) > base(1800)? NO → ABUNDANT → diversify → FIFO unchanged
```

So the shipped change is a **no-op on this node right now**, twice over: the paid window is cold, and
the idea queue currently holds 0 open ideas. It arms itself the first time the governor stretches.
That is the honest state — not "verified working under scarcity", which has not happened yet. The
signal that it ever fires is a `cp-focus:` line in `~/.mesh/generate.log`, and the first one should be
read as evidence about the mechanism, not as a success.

## 5. What this does not claim

- **Only one of Vervaeke's three rows is now embodied on the selection axis.** Cognitive scope
  (compression ↔ particularization) has no analogue in `mesh-generate` at all.
- **CP is not RR.** The paper's own position is that relevance emerges from *balancing* all three
  constraints; one constraint wired into one organ is a test of portability, not an implementation of
  the framework. The Frontiers 2024 counter-thesis stands untouched by this.
- **The J₁/J₂ partition is a judgement.** Calling `DECAY`/`REFLEX`/`VERIFY`/`ESCALATE` "viability" and
  everything else "exploration" is a reading of the queue's kind vocabulary, not a measurement. The
  `kind=` log line exists so that reading can be corrected from the lane's own evidence.
- **β here is binary, not continuous.** Vervaeke's β⁻¹ is a weight; this is a threshold on one
  inequality. A continuous version (weight the re-rank by base/eff_gap rather than gating on it) is the
  obvious next step and is deliberately NOT shipped — it would need calibration against a real hot
  window, and none has been observed since the patch.

## 6. Files

- `scripts/mesh-generate` — `GEN_VIABILITY_RE`, `cp_scarce()`, the CP branch in `pick_open_idea()`,
  four `--test` arms. Uncommitted, in-tree; steward lands.
- This review.
