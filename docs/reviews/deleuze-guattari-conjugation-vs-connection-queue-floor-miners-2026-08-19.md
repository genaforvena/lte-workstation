# Deleuze & Guattari → CONJUGATION vs CONNECTION of flows: the single-slot ideas-queue floor, and why its suppression was unmeasurable

**Date:** 2026-08-19 · **Lane:** genome literature live-review (feed auto-task) · **Organs named:**
`scripts/mesh-cooscillate`, `scripts/mesh-correlate`, `scripts/mesh-rhythm`, `scripts/mesh-leadlag`

## Where we already are in this area (checked, not assumed)

D&G is a worked seam here — 12 prior reviews in `docs/reviews/`: smooth/striated + intensive residual,
deterritorialisation coefficient (relative vs absolute), asignifying rupture, transversality, double
articulation, order-word redundancy, assemblage/relations of exteriority, disjunctive synthesis,
Buchanan's purpose-oriented discharge, machinic phylum, faciality/black hole, rhizome-vs-arborescent
callgraph. Grep over `docs/ scripts/` for the candidate vocabulary before landing:

```
refrain 16 · ritornello 6 · abstract machine 6 · plane of consistency 7 · line of flight 4 · nomad 4
CONJUGATION 0 · connection-of-flows 0 · overcoding 0 · war machine 0 · haecceity 0 · quasi-cause 0
```

**`conjugation` is zero.** That is the ground.

## The concept — conjugation is not "coupling", it is RELATIVE STOPPAGE

D&G split the joining of two deterritorialised flows into two opposite operations. Paul Patton's entry
*"deterritorialisation + politics"* in **The Deleuze Dictionary, rev. ed. (Adrian Parr, ed., Edinburgh
UP, 2015)** states the cut:

> "The 'connection' of deterritorialised flows … refers to the ways in which distinct
> deterritorialisations can interact to **accelerate one another**, and the 'conjugation' of distinct
> flows which refers to the ways in which **one may incorporate or 'overcode' another thereby effecting
> a relative blockage of its movement**."

And in *A Thousand Plateaus*, plateau 9 ("Micropolitics and Segmentarity"), conjugation

> "indicates their **relative stoppage**, like a **point of accumulation that plugs or seals the lines of
> flight** … and brings the flows **under the dominance of a single flow capable of overcoding them**."
> (p. 220, Massumi trans. — page cite taken from Spinuzzi's reading notes, not verified against a
> physical copy on this node.)

Why this is not something we already embody under another name:

- It is **not** Pearson r / co-oscillation (`mesh-cooscillate`) — that is symmetric and about levels.
- It is **not** transfer entropy / directed coupling — already named as a HELD note in
  `scripts/mesh-cooscillate:73-99`. TE says *who drives whom*; conjugation says *whose capacity to vary
  is sealed*, which is a different quantity and can be large where TE is zero.
- It is **not** PID redundancy/uniqueness (`docs/reviews/info-theory-agency-partial-information-
  decomposition-synergy-motion-fuse-2026-07-31.md`) — PID is always relative to a fused **target**.
  Conjugation is about the flows themselves and needs no target.

The operational content D&G adds: **wherever heterogeneous flows meet at one point of accumulation, ask
whether that point accelerates them (connection) or seals them (conjugation) — and the second is a
measurable relative stoppage, not a metaphor.**

## Where it lands in this mesh: the ideas-queue FLOOR is a point of accumulation

Five autonomous idea sources feed one file, `~/.mesh/ideas-queue`, and every one of them gates on the
same rule (`IDEATE_FLOOR=1`): **append only if the queue has ZERO open `[ ]` items.** One slot, five
flows. That is D&G's point of accumulation, built by hand, on purpose ("one provocation at a time").

Composition of the whole queue (1289 lines, measured 2026-08-19):

| source prefix | lines | share |
|---|---|---|
| LITERATURE (`mesh-ideate` lit lane) | 1065 | **82.6%** |
| DECAY REVIEW | 76 | 5.9% |
| CONNECTION (`mesh-ideate` connect lane) | 70 | 5.4% |
| REFLEX REPAIR | 45 | 3.5% |
| STUDY | 23 | 1.8% |
| CORRELATION (`mesh-correlate`) | 5 | 0.4% |
| SCHEDULED APPEARANCE | 3 | 0.2% |
| VERIFY FIX | 1 | 0.1% |
| CO-OSCILLATION (`mesh-cooscillate`) | **1** | 0.08% |

One flow holds 82.6% of the queue. The operator's explicitly-commissioned **DATA-DRIVEN** idea sources
(`mesh-cooscillate` is literally headed *"DATA-DRIVEN idea source #4 (operator 2026-06-20)"`) hold six
lines between them. That is the shape of "brought under the dominance of a single flow".

## The honest result — and it is NOT the one the concept predicts

The obvious conjugation story is "the always-full LITERATURE lane holds the slot and seals the miners."
Per-tool eval counts from `~/.mesh/*.log` (correlate/cooscillate/rhythm/leadlag since 2026-07-14,
ideate since 2026-07-29) falsify it:

| tool | held (gate refused) | gate passed, nothing fresh | emitted | hold-share |
|---|---|---|---|---|
| `mesh-ideate` | 41 | 0 | 853 | **4.6%** |
| `mesh-correlate` | 417 | 564 | 5 | 42.3% |
| `mesh-cooscillate` | 407 | 572 | 1 | 41.5% |
| `mesh-rhythm` | 229 | 259 | 3 | 46.6% |
| `mesh-leadlag` | 207 | 284 | 0 | 42.2% |

The miners **won the free slot ~58% of their evals** — 572 times for `mesh-cooscillate` alone — and
emitted once. They are not starved of slots. Their own novelty filter and thresholds are what keep them
at one. **The dominance is real; the gate is not (mostly) its cause.** Recording that here because the
concept made a prediction and the data did not grant it.

## The actual defect the concept exposed — the counterfactual is destroyed by the gate that needs it

What the numbers above **cannot** say is whether those ~42% holds blocked anything, because every one of
the four miners wrote the *same string* on the hold path:

```
mesh-cooscillate: queue has 1 open idea(s) (>= floor 1) — hold, not piling on
```

`held while I had a fresh finding` and `held with nothing to say` were byte-identical. So the one number
a conjugation index needs — **relative stoppage: findings suppressed per hold** — was structurally
unmeasurable, and 407 holds and 407 blocked findings were the same log. This is D&G's own point turned
into a bug: *the flow is sealed before it expresses itself*, so the seal leaves no trace of what it
sealed. (Same shape as `[[a-collapsed-reason-makes-blind-and-quiet-identical]]` at a different site.)

The fix costs nothing: in all four tools the candidate set (`raw` / `raw_novel`) is **already computed
before the gate**, and the freshness filter is a grep against the recent-keys cache.

## Shipped (uncommitted, in the tree)

`scripts/mesh-cooscillate` · `scripts/mesh-correlate` · `scripts/mesh-rhythm` · `scripts/mesh-leadlag` —
the hold branch now counts the fresh candidates it is refusing and names the top one:

```
… — hold, not piling on (suppressed=0)                       # quiet: the hold cost this lane nothing
… — hold, not piling on (suppressed=2 top=coosc:PhoneA:WatchB)   # a REAL relative stoppage
```

Machine-parseable and greppable, so a conjugation index over these logs becomes
`Σ suppressed / Σ holds` per source. The `hold, not piling on` substring is preserved byte-for-byte
(`mesh-generate:15` references it).

**Gate (`mesh-cooscillate --test`), two-sided and seen RED before green** — a one-sided gate would pass
on a tool that hardcoded either answer:

- with a busy queue and a fresh candidate → must print `suppressed=<n≥1> top=coosc:…`
- with every candidate already in the recent-keys cache → must print `suppressed=0`

Mutants run from a scratch copy (basename preserved), both fail for the right reason:

```
mutant A (drop the suppressed= clause):  FAIL (hold did not name the fresh finding it suppressed —
                                               a hold count is not a suppression count)
mutant B (pin _sup=1):                   FAIL (hold claimed suppression while every candidate was
                                               already recently emitted — quiet and blocked collapsed again)
```

`--test` green on all four after the change (`mesh-correlate`, `mesh-rhythm`, `mesh-leadlag` rc=0).

## Scope boundary, stated rather than skipped

`scripts/mesh-ideate` is **deliberately not patched**: it generates its idea *after* the gate
(`gen_literature`/`gen_connection` at `:1170`), so its hold cannot report suppression without paying the
generation cost — a different fix, and it is the dominant flow, not a held one. Its 41 holds (4.6%) are
the least interesting cell in the table.

## What this does NOT yet answer

Whether the single slot should stay one slot. D&G's alternative to conjugation is **connection** — an
admission rule under which the flows accelerate one another instead of one overcoding the rest; the
cheapest form would be a **deficit-arbitrated** floor (a lane shut out for N consecutive slots takes the
next one) rather than arrival order. **HELD, instrument-first**: with `suppressed=` now on the tape, that
lever can be argued from measured stoppage in a week instead of from a share table that, as shown above,
points at the wrong cause.

## Sources

- Paul Patton, "deterritorialisation + politics", *The Deleuze Dictionary*, rev. ed. (Adrian Parr, ed.),
  Edinburgh University Press, 2015 — https://gilles_deleuze.en-academic.com/45/deterritorialisation___politics
- Deleuze & Guattari, *A Thousand Plateaus*, plateau 9 "Micropolitics and Segmentarity", p. 220
  (Massumi trans.) — page cite via Spinuzzi's reading notes,
  http://spinuzzi.blogspot.com/2007/01/reading-thousand-plateaus-second.html
- Live-lane check for current work in the area: *Deleuze and Guattari Studies* (Edinburgh UP) and the
  7th DGSIC conference 2026, "Culture Without Organs: Machinic Thought, Transdisciplinary Assemblages,
  and Cartographies of Difference" (Feb 27–28, 2026) — https://www.deleuzeindia.com/conference-2026/ .
  No 2025–26 article specifically operationalising *conjugation* was found; the concept is cited from
  the primary text and the dictionary, not from a recent paper, and that is stated rather than dressed up.
