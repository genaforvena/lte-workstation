# Structural bias — the mesh measures WHO won and calls that even; the swarm literature measures WHICH SLOT won, and our picker fails that test

**Area:** swarm intelligence & stigmergy
**Angle:** a known CRITIQUE of the field — algorithms that look good because of a preference nothing in the problem justifies
**Date:** 2026-08-15 · genome · live web review
**Landing site:** `scripts/mesh-mind-control` (`_pick_agentic`, the mesh's actual selection operator) — new `--bias` probe

---

## The concept we did not embody: STRUCTURAL BIAS, and the uninformative-objective test that detects it

The swarm/evolutionary-computation field's standing self-critique is that a large fraction of published
metaheuristics are strong only where their own hidden preference happens to lie. The defect has a name:

> "Structural bias (SB) refers to systematic preferences of an optimisation algorithm for particular
> regions of the search space that arise independently of the objective function."
> — Kudela, van Stein, Bäck & Kononova, *Structural bias in multi-objective optimisation*,
> arXiv:2602.06742, submitted 2026-02-06.

The transferable part is not the diagnosis, it is the **detection method**, and it is the opposite of
what we do everywhere:

- You cannot read SB off the code (it lives in tie-breaks, iteration order, initialisation).
- You cannot read it off the outcome distribution either — that is the trap, see below.
- You **re-run the algorithm with deliberately uninformative objective values** ("synthetic test
  problems with … deliberately uninformative objective values"), so that anything it *still* prefers is
  produced "purely by algorithmic operators and design choices."

The sharpest, cheapest instance of the same test is the twin-optimum symmetry benchmark:

> Walden & Buzdalov, *A Simple Statistical Test Against Origin-Biased Metaheuristics*,
> EvoApplications 2024 (EvoStar), doi:10.1007/978-3-031-56852-7_21.
> Two identical, symmetrically-located global optima, one at the origin; a non-parametric test on the
> best solutions across independent runs flags any algorithm that does not split them evenly. In their
> case study of **15 published algorithms**, the test identifies most of the origin-biased ones — i.e.
> algorithms that had been reported as effective for years while their apparent skill was a preference
> for where the answers happened to be.

**We have eleven swarm/stigmergy reviews landed** (`swarm-ant-mill-*`, `swarm-density-adaptive-
evaporation`, `swarm-stigmergy-pheromone-entropy-*`, `swarm-cross-inhibition-*`, `swarm-tunable-quorum-*`,
…) and every one of them measures the **colony's outcome distribution**. None measures the **selection
operator against a null objective**. That is the gap.

## Why it lands on `_pick_agentic`, and why it compounds through the stigmergic loop

`mesh-mind-control`'s `_pick_agentic` **is** the mesh's selection operator: given the eligible windows it
returns the one that gets the work. Read its tie-breaks:

- `scripts/mesh-mind-control:579` — the idle-CLAUDE branch breaks ties by `pick_recency` (load-spread),
  with a deliberate strict `-lt` so equal/absent recency "degrades to the historical first-in-`$WORKERS`
  pick".
- Every other tier — idle-free (`opencode|codex`), queued-busy, blocked, unhealthy — is
  `[ -z "$x" ] && x="$win"`: **first-in-roster wins, unconditionally, and recency is never read at all.**

So when the objective (state, engine, health) rates two candidates identically, the winner is decided by
**position in `$WORKERS`** — a preference arising independently of the objective. That is SB, verbatim.

The mesh is stigmergic, so it does not stay local: the picked window works → posts `[done]` on the board
→ `mesh-forage` reads the **evenness of `[done]` across lanes** and renders `SELECTIVE` / a dead trail.
Nothing between those two ends separates *"the lanes really differ"* from *"the picker prefers whatever
sorts first"*. And the loop is self-confirming — a window never picked never posts, so it reads as an
evaporated trail, which is precisely the ACO stagnation signature `mesh-forage` was built to catch. The
pheromone map gets shaped by roster order and then read back as a fact about demand.

### The trap this makes explicit

Under permuted roster order, the outcome histogram **by identity** comes out flat (each name wins ~1/K)
for a picker that is **100% position-bound**. Evenness of *who won* is not absence of bias; only the
histogram **by slot** shows it. `mesh-forage` measures the identity axis. So does every board-side
evenness sense we own. A perfectly slot-bound dispatcher is invisible to all of them.

## What was built: `mesh-mind-control --bias` (read-only, rc-neutral)

Drives the **real** `_pick_agentic` through the stub seams `--test` already uses, with K candidates the
objective rates identically, roster order permuted (Fisher–Yates), R runs per row. Two objectives per
tier: `uninformative` (all recency 0 — the SB test proper) and `informative` (one candidate, placed
LAST in canonical order so a position-bound picker cannot be credited for finding it, given the oldest
`pick_recency` — a picker that reads its objective must follow it from every slot).

Measured on this node (`MESH_BIAS_RUNS=60`, K=4, seed 7):

```
  tier         objective        pos     id    fav  verdict
  idle-claude  uninformative   1.00   0.32   0.32  POSITION-BOUND
  idle-claude  informative     0.32   1.00   1.00  OBJECTIVE-LED
  idle-free    uninformative   1.00   0.32   0.32  POSITION-BOUND
  idle-free    informative     1.00   0.32   0.32  OBJECTIVE-BLIND
  queued       uninformative   1.00   0.32   0.32  POSITION-BOUND
  queued       informative     1.00   0.32   0.32  OBJECTIVE-BLIND
```

Read that as three findings, none of which was visible before:

1. **Every tier is POSITION-BOUND under an uninformative objective** (`pos = 1.00`) — while the identity
   share sits at ~1/K (`0.32`), i.e. the axis our senses measure reports "even" for a picker that is
   entirely decided by list order. The trap is not hypothetical here; it is the live reading.
2. **The one mitigation we have reaches exactly one tier.** `idle-claude` flips to OBJECTIVE-LED the
   moment the objective distinguishes candidates — the `pick_recency` load-spread works. `idle-free` and
   `queued` stay at `pos = 1.00` **even when the objective speaks**: OBJECTIVE-BLIND. Free-engine
   dispatch (opencode/codex — the tier we lean on precisely when claude is walled) has no load-spread at
   all, and no reading anywhere in the mesh said so.
3. The `live:` leg reports workers never once present in `.pick-recency` — a **lead, not a verdict** (a
   window may be never-picked because it was never idle). On this node every configured worker has been
   dispatched at least once.

**Falsifier built in.** `MESH_BIAS_BREAK=1` disables the permutation; the same picker then reads
`IDENTITY-BOUND` (`pos 1.00 / id 1.00`) — proof that the shuffle is what carries the finding, since an
unpermuted probe cannot tell a preferred slot from a preferred name.

**Gates (7, in `--test`, hermetic — stubbed sensors, no tmux, no board):** the six verdicts above plus
the trap assertion (`id < 0.5` on a POSITION-BOUND row), the BREAK falsifier flip, and `K=1 → rc 2`
(honest n/a, never a silent verdict).

**Seen RED, not assumed.** Mutant run from a scratch copy (`/tmp/.../mmc-mutant`) extending the
`pick_recency` tie-break to the `opencode|codex` branch: the probe flips `idle-free/informative` to
OBJECTIVE-LED and the suite fails with exactly one miss —
`bias FAIL: [idle-free/informative] → 'OBJECTIVE-LED' (want 'OBJECTIVE-BLIND')`. The gate is the record
of where the mitigation currently stops; whoever moves it must move the assertion deliberately.

## Honest limits

- **Fixture-driven.** The probe drives the real picker through stubbed sensors, so it measures the
  **operator**, not the live dispatch stream. It cannot tell you what share of *actual* dispatches was
  decided by roster order — only that, wherever the objective is silent, roster order decides.
- `pos = 1.00` is a property of a **deterministic** picker; the statistical machinery (R runs, shares)
  exists because the informative rows and any future randomised tie-break are not deterministic, and
  because the identity/slot contrast needs the permutation to be visible.
- **Nothing was changed in routing.** Whether to fix the bias — extend `pick_recency` to the free and
  queued tiers, or break exact ties by a name-hash rather than by list position — is a dispatcher
  behaviour change and belongs to a separate, operator-visible decision. This review ships the
  instrument and the measurement, not the edit.

## Sources (live web, read this session)

- Kudela, van Stein, Bäck & Kononova — *Structural bias in multi-objective optimisation*,
  arXiv:2602.06742 (2026-02-06). Definition of SB; the "deliberately uninformative objective values"
  method; the argument for behaviour-based benchmarking alongside performance-based evaluation.
- Walden & Buzdalov — *A Simple Statistical Test Against Origin-Biased Metaheuristics*, Applications of
  Evolutionary Computation (EvoApplications 2024), doi:10.1007/978-3-031-56852-7_21. The twin-identical-
  optima benchmark + non-parametric test; 15-algorithm case study.
- Supporting/adjacent, surfaced in the same sweep (not relied on for the mechanism): van Stein,
  Vermetten, Caraffini & Kononova, *Deep BIAS: Detecting Structural Bias using Explainable AI* (GECCO
  companion 2023, doi:10.1145/3583133.3590551); van Stein, Thomson & Kononova, *A Deep Dive into Effects
  of Structural Bias on CMA-ES Performance along Affine Trajectories* (arXiv:2404.17323, 2024);
  *An Investigation of Structural Bias in Particle Swarm Optimization* (EvoApplications 2025,
  doi:10.1007/978-3-031-90065-5_8).

## Files touched

- `scripts/mesh-mind-control` — `structural_bias()` + `--bias` CLI arm + 7 `--test` assertions +
  usage/header block. Read-only; no routing behaviour changed.
