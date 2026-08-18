# Live-literature review — information theory of agency → a distributed sensor mesh: the RESTLESS ARM, and the pacing fault the mesh has no flag for

Date: 2026-08-17 · lane: genome (idea-queue LITERATURE task — information theory of agency, angle =
CROSS-DOMAIN transfer to a distributed sensor mesh) · status: fix in tree, uncommitted (steward lands)

## Where we had already been (checked in the tree BEFORE landing)

This is the mesh's most-worked seam — **20** `info-theory-agency-*` reviews plus 10
`predictive-processing-*`, and the 2026-08-16 landing opens by calling it "near-saturated". Confirmed
by grep, not memory:

- open-loop / process / assistive / **multi-agent interference-channel** empowerment, empowerment as
  **channel capacity** (Blahut–Arimoto), **discounted (EELMA)** empowerment, MI finite-sample bias null;
- **predictive information**, predictive information **rate**, crypticity, transfer entropy, PID
  synergy/redundancy, Maximum Occupancy Principle, plasticity `I(O→A)`, **relevant information** (the
  minimum-inward-bits landing);
- **semantic information** (scramble→viability) and **Schneider R_seq/R_freq** — both landed;
- **Csaky, "Prediction and Empowerment: A Theory of Agency through Bridge Interfaces"** (arXiv:2605.06346)
  — landed **2026-07-24 under this very task-angle**, and its overwrite-vs-identification probe is
  running inside the file this landing touches. The bridge-interface decomposition, the separations,
  BGP: all embodied. I picked it, then found it, and dropped it.
- **Age of Information / AoII** — landed **today** on `mesh-chat-sync`
  (`distributed-systems-age-of-incorrect-version-semantic-divergence-chat-sync-2026-08-17.md`).
- Also checked and rejected as covered: information bottleneck / bandwidth-gated multi-agent
  communication (Farooq & Iqbal, arXiv:2602.02035, Feb 2026 — the mesh already gates its expensive
  channels: `mesh-room-address --ambient` logs 794 SILENT / 55 REACT / 3 ERROR, a 93.5% suppression
  rate, already instrumented); submodular/MI sensor placement (Krause & Guestrin — a 2008 classic, not
  live); noisy-TV/entropy-seeking selection (landed on `mesh-novelty`).

**Zero hits anywhere in `docs/` or the 676 `scripts/`: `whittle`, `multi-armed`, `index policy`,
`indexability`.** That is the gap.

## The live source

- S. Jonah, S. K. Yoo & S. Sthapit, **"Adaptive Scheduling: A Reinforcement Learning Whittle Index
  Approach for Wireless Sensor Networks"**, **arXiv:2601.01179** (January 2026) — read via
  <https://arxiv.org/pdf/2601.01179>. Found through a live search for 2026 information-theoretic
  sensor-scheduling work, not from a reading list.
- Its foundation: P. Whittle, **"Restless bandits: activity allocation in a changing world"**,
  *Journal of Applied Probability* **25A**:287–298 (1988).

The formulation: a network that cannot poll everything models each sensor as a **restless arm** — an
arm whose underlying state **keeps evolving whether or not you observe it**. The **Whittle index** is
the *subsidy for passivity*: the reward you would have to be paid to leave the arm alone that makes you
exactly indifferent between polling it and not. Where **indexability** holds, greedily taking the top-k
by index is near-optimal, and — the part that transfers — the index is a **single currency that makes
heterogeneous arms comparable under one budget**. The 2026 paper's contribution is learning those
indices online when the arms' dynamics are unknown, which is the mesh's situation exactly.

## What the mesh does not have

Every scheduled sense in this genome carries its own `# reflex-cadence:` — an **independent, hand-set
constant**. There is no currency in which two reflexes are comparable, so *"should this tick go to psi
or to bt-census"* has never been a question the mesh could even pose. The doctrine's existing pacing
axis is **coverage = sampling window / cadence** (`docs/window-cadence-coverage-2026-08-15.md`; the psi
disaster, fe35dd9: a 10s kernel average read once per 600s = 1.7% of wallclock, CALM for 14.2 days).
That axis is about the **sensor's duty cycle**.

The restless-arm framing supplies the axis nobody measured: **the rate at which the WORLD moves between
looks.** A reflex can pass coverage and fail this one, and vice versa. And the two ends are different
faults:

| move-rate over scheduled looks | meaning | mesh today |
|---|---|---|
| ≈ 0 | **over-polled** — many looks per change | `value-frozen`, reported (correctly hedged as a lead) |
| mid | tracking | — |
| ≈ 1 | **aliased** — the world changed between *every* look, so the reading is a SAMPLE, not a state | **no flag at all** |

The ingredient was already on disk. `overwrite_probe()` in `scripts/mesh-reflex-health` answers, once
per scheduled run, *did this artifact's bytes change since the last look* — and the loop threw the
answer away after using it in the one direction. The mesh had been computing the numerator of a Whittle
index for weeks and reading it only as an alarm.

## The change (uncommitted, in tree) — `scripts/mesh-reflex-health`

1. **The refrain store grows two fields**: `runs` and `moves`, accumulated per scheduled probe.
   Backward-compatible — a store written before today has two fields, parses, and floors the counters
   at 0 (a pacing counter that crashed on its own older store would take the freshness verdict down
   with it on every node that upgrades).
2. **`pace_probe()`** — read-only accessor; never writes, never counts.
3. **`aliased` on the `--check` line** (report-only, its own `· pacing:` clause, never the stale
   vocabulary `mesh-needs` scrapes): `name(aliased M/N runs moved ≥90% at Ns — the world changed
   between every look, so this reads a SAMPLE not a state)`.
4. **Two floors, both real**: `MESH_PACE_MIN_RUNS=8` (2/2 is not a rate) and `MESH_PACE_ALIAS_PCT=90`.
5. **Report-only, and it stops there.** An index may order nothing until **indexability** is proven,
   and nothing here has proven it. This publishes the quantity a pacing decision would be made *from*.

Live `--check` right now: `ok (7 per-run reflex(es) fresh · overwrite-only: router-watch(value-frozen
9209s) psi(value-frozen 78810s) · cohort 3/6 held while 3 moved)`. **No pacing verdict yet, and that is
correct** — the counters start at zero on every existing store, so the first verdict lands after 8
scheduled ticks per reflex. What the cohort line already shows is the mid-band this axis exists to
resolve: half the valued artifacts move on a given tick.

## Gates — seen RED, then GREEN

`--test` passes (`rc=0`) with the pacing block added. Every new gate was broken **from a scratch copy
named `mesh-reflex-health`** and watched fail:

| mutant | result |
|---|---|
| peek writes the store across a content change | **RED** — "a read-only probe that persists consumes the transition" |
| first sight counted as a move | **RED** — `5 1` → `5 2` |
| the `aliased` label never emitted | **RED** — e2e all-moving artifact |
| `aliased` fires regardless of move-rate | **RED** — "a FROZEN artifact must never read aliased" |
| the run floor removed | **RED** — below-floor leg publishes |
| torn/garbage counter guards removed | **RED** — `pace_probe` returned `notanumber alsonot` |

Three of those gates were **vacuous on the first attempt** and had to be rebuilt, which is the part
worth keeping:

- The first mutation run had **every** mutant red — on an *unrelated* `fanin_count` assertion, because
  the scratch copy was named `r.sh` and the tool's self-exclusion is by filename. All six were red for
  the wrong reason. Naming the copy `mesh-reflex-health` and adding an **unmutated control run** (which
  must be green) is what exposed it.
- The peek gate compared store bytes across *unchanged* content — where a stray peek-write rewrites the
  same four fields, so it passed with the guard deleted. Moved to assert across a **content change**,
  where a persisting peek would silently consume the transition.
- The run-floor gate was tested at 90% with 3 runs. First sight is never a move, so with `n` runs the
  maximum attainable rate is `(n-1)/n`: **below 10 runs the 90% threshold is unreachable by
  construction**, and the floor test passed with the floor deleted. Re-tested at 60% with 4 runs (75%),
  where only the floor stops publication.

## The doctrine line this earns

**A cadence has two failure directions and the mesh only ever named one.** `value-frozen` is the
over-polled end, already read (as a possible-death lead). The under-polled end — the state moving
between every look — produces a perfectly fresh mtime, an honest reading, a green reflex, and a value
that is a sample of a process rather than a description of a state. Coverage (window/cadence) will not
catch it: that measures how much of the interval the *sensor* was awake, not how many times the
*world* turned over while it slept. Measure both, and never let a per-tool hand-set cadence stand as
though it were commensurate with any other.

Siblings with the same shape and no move-rate today (flagged, not fixed — each needs its own
measurement, not this one's number copied): `scripts/mesh-pulse`, `scripts/mesh-reflex-decay`,
`scripts/mesh-sense-monitor`.
