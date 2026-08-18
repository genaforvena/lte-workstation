# Relevance realization — live review: THE PRIOR DILEMMA (first priors, and the rigidity horn)

**Date:** 2026-08-18 · **Lane:** relevance realization & the frame problem (Vervaeke) · **Window:** genome@mesh-home
**Angle:** a *recent* result (2025) that attacks the mesh's own prioritiser at its foundation.
**Landed (uncommitted, in tree):** `scripts/mesh-dispatch --first-priors` — report-only posture read, rc 0 always.

## Where we had already been (so this doesn't double-count)

Eleven `rr-*`/adjacent reviews sit in `docs/reviews/`: opponent processing as a demand-tracking edge,
cognitive scope (the normalizer), efficiency↔resiliency, insight/reframe-at-impasse, ecological-rationality
footholds, routines & orientation worlds, cognitive tempering, the diametric autism↔psychosis posture,
EFE novelty-vs-salience, and — yesterday — the frame problem's **ramification** horn (change-anchored
supersession, `mesh-doctor --supersede`). Every one of them is about *how* a weighting is set. **None asks
what terminates the setting of weights.** `grep -riE 'first.prior|prior dilemma|permanently.upweight'` over
`scripts/` and `docs/` returned **0** before this review.

## The live result (2025 stream, still open)

The current live exchange in this area is a three-paper argument, all inside 12 months:

1. **Darling, Corcoran & Hohwy (2025), "Solving the relevance problem with predictive processing"**,
   *Philosophical Psychology*, doi [10.1080/09515089.2025.2460502](https://doi.org/10.1080/09515089.2025.2460502)
   (online 2 Feb 2025) — claims active inference (priors + prediction error + precision + action-as-inference)
   *comprehensively* solves relevance.
2. **Andersen, Miller & Vervaeke**, "Predictive processing and relevance realization: exploring convergent
   solutions to the frame problem", *Phenomenology and the Cognitive Sciences*, doi
   [10.1007/s11097-022-09850-6](https://doi.org/10.1007/s11097-022-09850-6) — the convergence claim
   (precision-weighting *is* opponent processing) this review's target argues against.
3. **← the one this review lands on.** **Parvizi-Wayne, D. (2025), "What active inference still can't do:
   The (frame) problem that just won't go away"**, *Philosophy and the Mind Sciences* **6**, doi
   [10.33735/phimisci.2025.12118](https://doi.org/10.33735/phimisci.2025.12118) (open access; read in full,
   ~18.7k words). Found by following the Darling et al. citation graph, not from a fixed reading list.

### The concept: THE PRIOR DILEMMA (§7, "First priors")

Parvizi-Wayne's move is not "precision-weighting is wrong" — it is *what sets the precision?* If the weight
on preference P1 is set by a higher-order policy P2, then P2's own preferences need a weight set by P3, and
so on: **"And onwards we go, into an infinite regress, in a brain which, of course, we do not expect to
regress infinitely."** The standard escape (Clark; Allen & Tsakiris; Kiverstein et al.; and Darling et al.
themselves) is to posit **first priors** — a special class of preferences held at *permanently* high
precision, which therefore need no higher-order policy to justify their weight. He names the cost:

> "if the weight of this preference is essentially fixed, no flexibility at all is afforded to the agent"
> … "reinstantiating prioritisation just reinstantiates the problem of relevance and the threat of infinite
> regress" … **"the two horns of what one might call 'the prior dilemma' arise: on one side, an infinite
> regress; on the other, rigidity."**

And the closing trap, which is the part that bites here: *any* context-sensitive adjustment of a first prior
re-opens the regress ("as soon as there is some 'context-sensitive adjustment of precision-weighting', the
frame problem seems to re-emerge"). So a first prior cannot be quietly made flexible — it can only be
**measured** for which horn it is sitting on.

## The mesh has exactly one first prior, and it was never audited

`priority:incident` (`scripts/mesh-dispatch`) is a textbook first prior:

- `priority_order()` puts the class at the head of the queue **unconditionally** — no context, no decay, no
  higher-order rule is consulted to justify the weight (that is the whole point: it caps the regress).
- `is_open()`'s never-taken branch makes the class **evaporation-exempt** — the weight is not just high, it
  is *permanent*. Header, verbatim: *"an incident is exempt from idle-exposure evaporation — the whole point
  is that it may sit unclaimed through busy stretches without aging out."*
- Inside the class there is **no discriminator whatsoever**: `priority_order()` preserves relative order, so
  two standing incidents resolve by FIFO — the context-blind constant the regress bottoms out in.

That is all three of Parvizi-Wayne's observations, in one 4-line awk. The design is *correct* — the class
exists precisely so an incident survives the stretches that age normal work out — but nothing in the mesh
could ever say **which horn the live board is on**, or what the fixed weight cost.

## What landed: `mesh-dispatch --first-priors` (report-only)

A posture read over the same pass state the picker uses (real OPEN mapfile, real `is_open()`, real exposure
ledger). It does not touch the picker. Three readings:

| verdict | meaning |
|---|---|
| `UNEXERCISED` | open work, no member of the class — the fixed weight decided nothing this pass |
| `INERT` | incidents standing with nothing to outrank — the weight won no contest, so it is **unfalsified** |
| `RIGID` | an incident is standing at/past the **eviction floor every token-less task faces** — it is held by PERMANENCE, not by urgency. The only reading that names a fault. |
| `+REGRESS-CAP` | ≥2 incidents at once · intra-class discriminator: none (FIFO) |
| `BALANCED` | contested, none past the floor |

The rigidity test is the part I think is actually new: the mesh already computes a *density-adaptive*
eviction threshold (`effective_stale_ticks`, from the 2026-07-28 swarm/evaporation review). An incident's
own idle-exposure tick count compared against that live threshold is an exact, non-arbitrary rendering of
"permanently upweighted" — **it is still standing at an exposure where every unweighted task would already
have evaporated.** No new constant was invented; the audit borrows the floor the picker already uses.

Displacement (`oldest token-less task Xm old waits behind an incident Ym old, queue-jump Zm`) is printed as a
**measurement, not a fault** — jumping the queue is what the axis is *for*; the review's own doctrine is that
naming a designed behaviour as a defect is how a report loses its reader.

### Live reading today

```
$ mesh-dispatch --first-priors
class: priority:incident — permanently upweighted, evaporation-exempt (the mesh's one first prior)
standing: 0 incident · 0 token-less · eviction floor 24 ticks (backlog 104)
verdict: NO-DATA — no open [task] on the board — nothing to prioritise
```

Measured over the retained board window (`~/.mesh/chat.log`, 2026-08-14T06:45Z → 2026-08-18T10:41Z, 3000
lines): **142 `[task]` lines, 0 carrying the trailing incident token.** 53 lines *mention*
`priority:incident` — every one of them is prose (reviews, `[done]` cites, digests), which is the
already-fixed prose-immunity hazard, not a member of the class. So the mesh's one first prior currently has
**no live member at all**: today's verdict is honest emptiness, and the RIGID horn is latent, not observed.
Stated plainly because the alternative is to let a fixture stand in for a finding.

## Gates (RED-first, 10/10 mutants)

Nine assertions, all black-box against sandbox boards (`HOME=<tmp> "$0" --first-priors`), fresh fixture per
direction. Every one was seen FAIL from a scratch copy before being trusted:

| mutant | assertion that went red |
|---|---|
| M1 `_fp_rest -eq 0` → `99` | lone incident must read INERT |
| M2 `_fp_tk -ge _fp_eff` → `-ge 999999` | 60 ticks past a 48-tick floor must read RIGID; row marked PAST-FLOOR |
| M3 `_fp_inc -ge 2` → `-ge 99` | two incidents must raise REGRESS-CAP |
| M4 `_fp_inc -eq 0` → `99` | no-incident board must read UNEXERCISED |
| M5 `queue-jump ${_fp_jump}m` → `0m` | ~120m jump must be measured |
| M6 drop the `--first-priors` READ_ONLY line | (whole mode goes dark — see limit below) |
| M7 `_fp_mark=within` → `PAST-FLOOR` | **control**: PAST-FLOOR must NOT fire when only a *token-less* task is past the floor |
| M8 drop the count from the regress-cap line | the flag must carry an evidence line |
| M9 inject `idle_exposure_tick` into the mode | the read must not tick the ledger |
| M10 append to `$CHAT` in the mode | the read must not post to the board |

**Coverage limit, stated rather than hidden:** the footprint gate (M9/M10) proves the *mode's own* writes are
caught. It does **not** exercise the `is_open()` exposure tick, because a sandbox HOME has no idle worker, so
`N_IDLE=0` makes that tick inert regardless of `READ_ONLY` — the same reason M6 shows up as "everything dark"
(the dispatch gate stops a non-READ_ONLY run on a card-less sandbox) rather than as a footprint failure. The
`READ_ONLY` wiring for this mode is therefore asserted one step weaker than the `--status` half beside it.

## Not applied (and why)

The obvious second target was `mesh-dash`'s alarm ordering (I demoted `phone-src-down` rows below real faults
this morning — a hand-set rank ladder, i.e. another first prior). Discarded for now: that ladder is a *display*
order with no eviction floor behind it, so the rigidity horn has nothing to measure against; inventing a
threshold for it would be the arbitrary constant this whole review argues against.

## Sources

- Parvizi-Wayne, D. (2025). *What active inference still can't do: The (frame) problem that just won't go away.* Philosophy and the Mind Sciences 6. https://doi.org/10.33735/phimisci.2025.12118
- Darling, T., Corcoran, A. W., & Hohwy, J. (2025). *Solving the relevance problem with predictive processing.* Philosophical Psychology. https://doi.org/10.1080/09515089.2025.2460502
- Andersen, B. P., Miller, M., & Vervaeke, J. *Predictive processing and relevance realization: exploring convergent solutions to the frame problem.* Phenomenology and the Cognitive Sciences. https://doi.org/10.1007/s11097-022-09850-6
- Jaeger, J., Riedl, A., Djedovic, A., Vervaeke, J., & Walsh, D. (2024). *Naturalizing relevance realization: why agency and cognition are fundamentally not computational.* Frontiers in Psychology. https://doi.org/10.3389/fpsyg.2024.1362658
