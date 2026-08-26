# The census is a pure FILTER: a snapshot frozen at the moment of observation, never revised by what came next

**Lane:** LITERATURE (live review) · free energy principle & active inference (Friston), angle = **a recent result (2023–2026)**
**Date:** 2026-08-26 · **Window:** genome@mesh-home
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-census` — **assigned by coin at p=0.20**, drawn uniformly from the 564 never-reviewed tools in the lane's denominator. Not chosen by me, not retargeted.
**Status:** implemented + gated, uncommitted in the tree (steward lands)

---

## 1. The result

Active inference's belief-updating scheme has **two passes**, and the mesh has only ever run one.

**Friston, Da Costa, Tschantz, Kiefer, Salvatori, Neacsu, Koudahl, Heins, Sajid, Markovic, Parr,
Verbelen & Buckley, "Supervised structure learning", *Biological Psychology* 193 (2024)
[arXiv:2311.10300, v1 17 Nov 2023]** — read in full via `pdftotext`. Verbatim (§ on the inversion
scheme):

> "This calls for Bayesian **filtering** (i.e., forward message passing) during the active sampling
> of observations, followed by Bayesian **smoothing** (i.e., forward and backward message passing)
> **to revise posterior beliefs about past states** at the end of an epoch. Bayesian smoothing
> ensures that the beliefs about latent states at any moment in the past are **informed by all
> available observations** when updating model parameters."

and, on what the backward pass *is*:

> "In neurobiology, this combination of Bayesian filtering and smoothing would correspond to
> evidence accumulation during active engagement with the environment, followed by a 'replay'
> before the next epoch."

**Still live in 2026.** Van de Maele, Verbelen, George & Pezzulo, "Schema-based active inference
supports rapid generalization of experience and frontal cortical coding of abstract structure",
**arXiv:2601.18946v2 (14 Mar 2026)**, §2.4, verbatim:

> "In contrast to standard parameter learning in active inference, where the belief over the state
> is **filtered** as actions are executed and observations come in, clone-graphs **smooth** the
> belief over states, and **propagate disambiguating information back** into other 'cloned' states.
> This provides a better estimate of the individual states…"

They run the backward pass over **"a sliding window of 10 observations"** — fixed-lag smoothing, the
bounded-cost compromise between filtering (cheap, wrong about the past) and full retrospection
(right, unbounded). That 10 is where `SMOOTH_LAG` comes from.

The transferable claim is narrow and mechanical: **a later observation carries information about an
earlier state.** A record that is written once at the moment of observation and never revisited is a
filtered estimate wearing the clothes of a trajectory.

## 2. Where we'd been — and the gap

`memory/fep-active-inference-coverage.md` maps 12 landed FEP concepts (EFE epistemic value,
BMR/BME, CKM, H3-reachability, interoceptive precision allocation, entropy regularizer, …). **Every
one of them is a forward-pass concept.** Nothing in the map, and nothing in the 21 prior `fep-*`
reviews, is about *revising a belief about the past*. Every durable tape in this mesh —
`records.log`, `presence.log`, `link-heal.log`, `model-bench.log`, `PROGRESS.md` — is append-only
and pure-filter: written at observation time, never corrected by later evidence.

`scripts/mesh-census` is the sharpest case because it *states* the assumption in its own docstring:

> "so the trajectory is legible. **Progress = the delta between snapshots.**"

## 3. What it costs, measured on the live record

A node that is merely **unreachable** contributes `0` to every class (`census()` sums `surf` over
`res`, not over the reached set), so the surface figure drops. When the node answers again, it rises
by exactly the same amount. The delta series then reports **two events where the world had none**.

`~/lte-workstation/PROGRESS.md`, 26 census rows, read by the new `--smooth` pass:

```
rows read: 26  (revisable v2: 0, pre-format v1: 26)
DELTA SERIES ("progress = the delta between snapshots"):
  filtered: 16 non-zero deltas / 25
  coverage-confounded: 9 delta(s) co-occur with a reachability change
```

**9 of 25 deltas (36%) in the mesh's own progress log co-occur with a change in reachability.** The
signature is unmistakable in the raw file — one node going dark and coming back:

```
## Census 2026-06-07T23:11:08Z   up 3->2   senses -21  actuators -18  connectivity -1
## Census 2026-06-08T07:41:38Z   up 2->3   senses +21  actuators +18  connectivity +1
```

Equal magnitude, opposite sign, eight hours apart. Nothing was lost and nothing was gained. And this
is not a historical curiosity: the census run made while writing this review reached **2 of 8** nodes.

## 4. What landed

`scripts/mesh-census` — two coupled changes, because the second is impossible without the first.

**(a) The record is made REVISABLE.** The old snapshot could not name what it failed to see, so no
future observation could ever correct it — a filtered row that discards the identity of the
unobserved is *unsmoothable in principle*. Every snapshot now carries `- Per-node:` (per-host class
counts for reached nodes) and `- Dark:` (host + why: `offline` / `unreachable` / `gateway`). The
human report gains a `coverage:` line that says outright the surface is a **LOWER BOUND** while any
node is dark. The `- Surface:` line is untouched, so existing readers keep working.

Live artifact (real census, `MESH_CENSUS_PROGRESS` pointed at a scratch file, 2026-08-26T11:18:11Z):

```
- Nodes up: 2/8
- Surface: minds=5 senses=10 actuators=10 connectivity=1 compute-nodes=2
- Per-node: mesh-home=3/7/6/0,phaedra=2/3/4/1
- Dark: GL-MT3000(offline),Redmi 10(offline),ilya(offline),imozerov-Default-string(offline),imozerov-IdeaPad-3-15IIL05(offline),rip(offline)
```

**(b) `mesh-census --smooth [--lag K]` — the backward pass.** For each dark host at row *t*, bracket
it with the nearest observation **before** and **after** *t* within K rows (default 10):

| bracket | verdict |
|---|---|
| both sides present and **equal** | `SMOOTHED` — the host held that set across the gap; the past surface was under-counted by exactly that much |
| both sides present and **differ** | `INDETERMINATE` — a bound `[min,max]` per class. **No point value is invented**, and the smoothed surface does not move |
| one side / neither | `UNREVISED` — no later observation yet. One-sided is still filtering |
| row predates the format | `unrevisable (pre-format)` — reported, never guessed around |

End-to-end, on a fixture reconstructing the 06-07/06-08 flap:

```
2026-06-07T23:11:08Z
  SMOOTHED     ilya (offline) held 1/21/18/1 across the gap (same set either side)
    filtered  actuators=10 compute-nodes=2 connectivity=1 minds=5 senses=10
    smoothed  actuators=28 compute-nodes=3 connectivity=2 minds=6 senses=31
DELTA SERIES: filtered 2 non-zero / 2 · smoothed 0 non-zero / 2 (2 were a node going dark, not the mesh changing)
```

**It never mutates a prior row.** The revision is *appended* as a `## Smoothing <ts>` block. The
filtered row stays exactly as written — it is the honest record of what was believed at the time,
and overwriting it would falsify the tape to flatter the smoother. Belief about the past is revised;
the tape is not.

## 5. Gates

`--test` grew from 3 legs to 9. The new ones are each the red of a specific way to get this wrong,
and **all seven mutants were driven red from a scratch copy** before the gate was believed:

| leg | asserts | mutant seen red |
|---|---|---|
| 4 | a pure flap is smoothed away; the smoothed surface equals the surface either side | revision does not move the surface → *"a dark-node flap was not smoothed away"* · `- Dark:` never parsed → same |
| 5 | a **disagreeing** bracket is bounded, not point-revised, and does not move the surface | `if back == fwd` → `if True` → *"disagreeing bracket was point-revised instead of bounded"* |
| 6 | a one-sided bracket is `UNREVISED` | `len(sides) < 2` → `< 1` → *"one-sided bracket was treated as a smoothing"* |
| 7 | the lag **binds**: `lag=10` reaches two rows forward, `lag=1` must not | window → whole file → *"lag=1 must NOT reach two rows forward"* |
| 8 | a pre-format row is `v1` and reported unrevisable | `fmt != "v2"` gate removed → *"pre-format row not reported unrevisable"* |
| 9 | a non-Census `##` section **closes** the row above it — the tool's own appended revision (or anything a human adds) must not be reparsed into the last census | header fall-through restored → *"a trailing section's fields were reparsed into the last census"* |

Leg 9 caught a real defect in my own first cut: it was written as "append the revision, check the
parse is unchanged" and it was **vacuous** — the revision block happens to contain no field-shaped
lines, so the mutant stayed green. It only became a gate once the fixture appended an adversarial
`## Notes` section carrying `- Surface:` / `- Per-node:` / `- Dark:` lines. A gate whose subject
never appears in its fixture asserts nothing.

## 6. Bounds — what this does NOT claim

- **The live 26 rows were NOT corrected.** All of them predate the `Per-node`/`Dark` fields, so the
  pass reads them `unrevisable (pre-format)` and appends nothing (`nothing appended (no row was
  revisable — a revision record with no revision in it would be a tape of only positives)`). The
  record only becomes smoothable **from the next census onward**. The 9/25 coverage-confounded
  figure is a *diagnosis* of the old rows, not a repair of them.
- **A smoothing is an assumption, and it is stated as one.** "Same set either side" does not prove
  the set never moved *during* the gap — it is the maximum-likelihood path given the bracket, which
  is exactly what a backward pass is. That is why disagreement yields a bound and never a number.
- **No adaptive probing.** The census still probes every node the same way every run; nothing here
  touches action selection.
- `--smooth` is read-only with respect to the mesh and append-only with respect to the file.

## 7. Sibling defect found, deliberately NOT fixed here

`probe()` collects `n["battery_verified"]` (the one real, no-side-effect **verification** the census
performs — an actual `termux-battery-status` read on an Android body), and the human report and
`PROGRESS.md` render it **nowhere**; it survives only inside `--json`. The docstring's claim that
the census "marks verified vs merely detected" is therefore false of the durable record: the
trajectory carries detections only. Left alone — it is a different finding and this arm assigned one
organ, not one refactor.

## 8. Searched the same window and set aside

- **Kouw, "Expected free energy as an information constraint on the Bethe Lagrangian", arXiv:2608.17167
  (17 Aug 2026)** — the KKT multiplier's inactive/interior/saturated regimes are a genuinely
  un-embodied idea (an epistemic drive that switches *off* when the constraint is slack), but it
  prices an *action* score and the census selects no actions. Same seam as the 2026-08-03
  entropy-regularizer deferral. Worth its own review on an organ that chooses.
- **Waade, Olesen, Laursen, Nehrer, Heins, Friston & Mathys, "As One and Many", *Entropy* 27(2):143
  (Feb 2025), doi:10.3390/e27020143** — the obvious census angle (the group's model is a
  coarse-graining, not the extensive **sum** of members' — and `census()` literally sums) collapses
  on inspection onto redundancy-vs-degeneracy, which **is** embodied: `mesh-sensorium --degeneracy`
  (`docs/reviews/antifragility-degeneracy-vs-redundancy-mesh-sensorium-2026-07-31.md`). Landing it
  would have been re-embodying an existing axis on a new organ.
- **Friston et al., "From pixels to planning: scale-free active inference", arXiv:2407.20292** —
  RGM needs a hierarchy the census does not have.

## 9. Earned rule

**A record written once at observation time is a FILTER, not a trajectory — and a filtered row that
cannot name what it failed to see can never be corrected by what comes later.** Write the identity
of the unobserved into the record, then run a bounded backward pass that revises the past by
appending, never by overwriting; where the bracket disagrees, publish a bound, not a number.
