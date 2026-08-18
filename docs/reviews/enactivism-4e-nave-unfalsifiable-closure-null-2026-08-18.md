# Enactivism & 4E — live review: the closure numbers that CANNOT FAIL

**Area:** enactivism & 4E cognition, entered from the angle the task names — a CROSS-DOMAIN transfer
onto a distributed sensor mesh. **Date:** 2026-08-18. **Window:** genome (mesh-home).
**Status:** landed, uncommitted in the tree. **Tool:** `scripts/mesh-closure` — new `--null` axis
(report-only, on-demand).

---

## I. The literature landed on

**Kathryn Nave, "Beyond Control: Finding the Purpose of Enactive Cognitive Science",
*Adaptive Behavior*, published online 9 April 2026, doi:`10.1177/10597123261435796`** — open access,
found by WebSearch and read 2026-08-18 (Sage full text).

Nave's target is the **cybernetic / dynamical-systems branch** of enactive cognitive science — the
branch this mesh has been mining for two months. Her charge is not that its formalisms are wrong.
It is that they cannot lose:

> the purpose of a system is *what it does* — a criterion that "generalizes trivially to all
> physical systems". A pendulum returns to equilibrium after a disturbance; a rock settles into a
> stable configuration; both display exactly the goal-directedness cybernetics calls purposive.

and then the sentence that transfers:

> "the mathematical flexibility of DST compounds this: **any activity can be retroactively described
> as satisfying some underlying stability equation.** Therefore, the observation that we 'find'
> purposiveness in dynamical analyses reveals nothing about reality; **it reflects only the
> formalism's expressive capacity.**"

Her positive move is to demand a criterion an arrangement of the same parts could *fail*:
constraint closure among **thermodynamically unstable** constraints, whose maintenance depends on
the system's own activity — *"the purpose of a system is not what it does, but what it needs to do…
the robot need do nothing at all."*

Live, not a museum piece: April 2026 in the journal where this argument is running, alongside Ward's
"What Is Enactivism?" (*Adaptive Behavior* 2026, doi:`10.1177/10597123261450094`), following her
*A Drive to Survive* (MIT Press 2025).

## II. What was checked FIRST, and refused

This area is the single most-mined one in the genome and the honest audit came before the build.
**Precariousness itself is already twice-landed and was NOT re-landed:**

- `review-autopoiesis-precariousness-constitutive-membership-mesh-vitality-2026-06-22.md` —
  precariousness as the constitutive-membership criterion (`mesh-vitality`).
- `docs/reviews/enactivism-4e-habit-precariousness-enacted-closure-2026-08-15.md` — precariousness as
  the *habit* criterion (Ramírez-Vizcaya, *Synthese* 206:137, 2025), which built
  `mesh-closure --enacted`, three days ago.

Also refused as embodied: graded viability (`mesh-body-power`), operational closure
(`mesh-closure`), cognitive-domain partition (`mesh-chaos:45-72`), irruption/absorption
(`mesh-needs:113-130`), structure↔activity causal symmetrization with an exact circular-shift
permutation null (`mesh-closure --symmetry`).

What survived is **not another closure concept. It is Nave's demand applied to the closure concepts
we already have** — and it lands on the graph axis, which is the one part of `mesh-closure` that has
never had a null.

## III. The finding

`mesh-closure` reports four headline numbers over the wired reflex set: **CORE, SOURCE, PERIPHERAL,
LOOPS.** Read `analyze()`'s classifier (`scripts/mesh-closure`, the classify block):

```
PERIPHERAL  if nobody mentions it         (in-degree == 0)
CORE        else if it mentions somebody  (out-degree  > 0)
SOURCE      else                          (in > 0, out == 0)
```

**A class is a function of two bits of a node's own degree pair and of nothing else in the graph.**
So a degree-preserving rewiring — same tools, same number of mentions in and out for every tool,
every *who-mentions-whom* reshuffled at random — reproduces CORE / SOURCE / PERIPHERAL / UNKNOWN
**exactly, with variance zero**. Three of the four headline numbers are a restatement of the degree
sequence. They are Nave's pendulum: a number that finds interior structure in every arrangement of
the parts is reporting the formalism, not the mesh.

LOOPS (mutual `a<->b` pairs) is second-order and *can* move. So it is the only one worth a null —
and it earns one.

### Live, 2026-08-18 (genome + `~/.mesh/reflexes.cron`)

```
null = configuration model: same tools, same in/out mention-degree per tool, edges reshuffled
R=200 replicates  seed=20260818  swaps/replicate=10xE
declared edges=938  nodes=232   LOOPS observed=120   null mean=33.67 sd=4.97  z=17.38  p=0.005  ABOVE NULL
live     edges=226  nodes=150   LOOPS observed=10    null mean=1.08  sd=0.95  z=9.38   p=0.005  ABOVE NULL
CORE / SOURCE / PERIPHERAL / UNKNOWN: NULL-INVARIANT BY CONSTRUCTION, variance exactly 0.
  declared 205 4 39 2  and  live 125 13 110 2   (CORE SOURCE PERIPHERAL UNKNOWN)
```

Two readings, and the second is a correction to a number already in circulation:

1. **The mutual loops are real.** 10 enacted loops against a null of 1.08 ± 0.95 (z=9.4) is genuine
   reciprocal structure, not degree accounting. The 2026-08-15 finding that six-to-ten loops survive
   the exercise test survives its null too, which is the stronger claim.
2. **A third of the *declared* loops are chance.** 120 observed against a null mean of **33.67**.
   Every report of "90 / 120 closed constraint loops — this is a real self-maintaining
   organization" has been quoting a figure whose baseline at that degree sequence is ~34. The excess
   is real; the headline was never the excess.
3. **CORE=205 / PERIPHERAL=39 (and their enacted 125 / 110) carry no evidence of organization at
   all.** A mesh whose every dependency was reshuffled at random prints the same four numbers. This
   does not make the PERIPHERAL *list* useless — it is still a correct list of tools nobody
   mentions, which is exactly what it is used for — but the *counts* have been read as a closure
   result, and as a closure result they are vacuous.

## IV. The trap found while building it (worth more than the axis)

The first implementation used a **fixed** number of accepted double-edge swaps per replicate, which
is the textbook default. On the 4-node fixture (`n1<->n2`, `n3<->n4`, every node in=out=1) it
reported:

```
LOOPS observed=2   null mean=2.00 sd=0.00  z=0.00  p=1.000  WITHIN NULL
```

Not noise — algebra. Where every node has in=out=1 the graph **is a permutation**, and one accepted
swap is exactly one transposition, so a fixed *even* swap count can only ever reach even
permutations. The three even derangements of four elements are all products of two 2-cycles, all
with mutual=2. The null was pinned on the observation, and reported it with `sd=0.00` and `p=1.000`
— a perfectly confident WITHIN NULL. **A null that agrees with you for an algebraic reason is worse
than no null**, because it reads as a measurement that was taken and passed. Fix: draw the accepted
count from the seeded rng (`target = nswap + rng.randrange(nswap)`) — still reproducible, no fixed
parity. Documented in the program, and `--test` mutant **m6** reverts it and goes red.

## V. Gate (RED-first; all mutants proven from a scratch copy)

The invariance claim is the load-bearing one, so it is **measured against the real classifier, never
asserted in prose**. Three fixtures:

| fixture | wiring | degree sequence | classes | LOOPS |
|---|---|---|---|---|
| N1 | `n1<->n2`, `n3<->n4` | every node in=1 out=1 | CORE=4 | 2 |
| N2 | `n1->n2->n3->n4->n1` | **same** | CORE=4 | 0 |
| N3 (control) | `n1->{n2,n3}`, `n2->n1`, n4 isolated | different | CORE=2 SOURCE=1 PERIPHERAL=1 | 0 |

N1 vs N2: one degree sequence, two wirings, **identical class counts and different LOOPS** — the
finding, driven end-to-end through `bash "$0"`. N3 is the control that stops the equality leg being
vacuous: **an equality assertion with no proven-unequal partner asserts nothing.**

| mutant | change | result |
|---|---|---|
| m1 | swap never accepted (no-op null) | RED — 2 legs |
| m2 | `random.Random()` — seed ignored | RED — reproducibility leg |
| m3 | invariance summary hard-codes the counts | RED — the N3 leg, uniquely |
| m4 | `mutual()` returns `len(s)` | RED — 2 legs |
| m5 | `E < 4` too-small guard removed | RED — the n/a leg |
| m6 | fixed swap count (parity trap restored) | RED — 2 legs |
| m7 | `analyze()` class rule made to read reciprocity | RED — the invariance leg |
| m0 | no-op control (a comment) | green |

**m7 is the one that matters**: it proves the invariance leg is a live measurement of `analyze()`'s
rule and not a tautology of the fixture — a classifier that read one bit beyond degree would break
it.

Every pre-existing axis is **byte-identical** to `git show HEAD:scripts/mesh-closure` — `--full`,
`--peripheral`, `--json`, `--enacted`, `--timescale`, `--cadences`, `--symmetry`, `--semantic`,
`--semantic-sites`, `--help`, all diffed and unchanged. `--test` 3.0s → 4.1s. Live `--null` 21s.

## VI. Honesty bounds (also in the tool header)

- The configuration model preserves degrees and destroys everything else. Beating it is evidence of
  **some** structure beyond degree, never evidence that the structure is the one we tell ourselves.
- It inherits every bound of the graph handed to it. On the `declared` population ~75% of edges are
  prose (`--enacted`), so declared significance is significance about how the mesh **writes**, not
  how it runs. **The `live` row is the one to read.**
- `p` is the add-one-corrected empirical tail: the floor is `1/(R+1)`, so at R=200 `p=0.005` means
  "no replicate reached it", never zero.
- Deterministic at a fixed seed. A number that moves between runs on an unchanged genome is a bug.

## VII. Not wired

On-demand, like every other `mesh-closure` axis (`orphan-ok`). It measures a static graph and acts on
nothing. The natural consumer is a steward pass and the `minds` dash.

**Still open in this area** (carried forward from 2026-08-15, unchanged): allostasis / anticipatory
regulation; CRQA structural coordination metrics; habit at the timescale of *activities* and
*regional identities* — whether a channel/role is a precarious self-sustaining network rather than a
roster entry. **New, from Nave:** her actual positive criterion is untouched here — a mesh constraint
(cron line, deployed binary, `--test` verdict) **persists passively**; nothing in the mesh degrades
faster because a reflex stopped running. Under her test the mesh is the pendulum, and the honest
version of that finding needs its own review, not a bolt-on.
