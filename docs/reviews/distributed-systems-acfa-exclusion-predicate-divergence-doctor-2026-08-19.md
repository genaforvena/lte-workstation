# Live literature review — distributed systems coordination

**Area:** gossip / CRDTs / eventual consistency · **Angle:** CROSS-DOMAIN transfer into a distributed sensor mesh
**Date:** 2026-08-19 · **Organ:** `scripts/mesh-doctor` (new `--exclusion` mode) · **Status:** landed, **uncommitted** (steward lands from the tree)

---

## The concept we did not embody

**The EXCLUSION PREDICATE must be agreed, not per-reader.**

> Ryan Gillespie, *"Byzantine Accountability Without Consensus: Strong Eventual Consistency for
> Non-Associative, Stochastic, Robust Aggregation"*, **arXiv:2607.10305**, submitted **11 Jul 2026**
> — <https://arxiv.org/abs/2607.10305> (abstract read this session; the two load-bearing sentences
> quoted verbatim below).

Two sentences carry the whole transfer:

- *"a robust rule needs no agreed order of contributions, only an agreed **set** and an agreed
  **exclusion predicate**"*
- *"an ulp-scale perturbation can flip the selected subset, moving the output by a **non-vanishing
  amount**"*

ACFA's architecture is the consequence: an **evidence layer** (content-addressed OR-Set of signed
contributions + a grow-only set of self-authenticating equivocation proofs) and an **aggregation
layer** that is a *deterministic pure function* over the converged state — fixed-point integer
arithmetic over a hash-canonical order, so every replica derives byte-identical output. Validation:
a 10-node prototype tolerating 3 Byzantine nodes, 16/16 falsification checks, byte-identical roots
under adversarial gossip.

The point that transfers is not the signatures. It is **which disagreement is fatal**: ordering is
not, membership-and-exclusion is — because a robust aggregate is **discontinuous**, so two replicas
that exclude different members do not get a *slightly* different answer, they get a *different* one.

## The transfer into the sensor mesh

A mesh sense publishes **one** artifact — `~/.mesh/.<x>.state` — that many organs read. Each reader
decides for itself when that artifact is *too old to use*. That decision is an exclusion predicate,
and in this mesh it is a **bare integer in the reader's own source**. Nothing publishes it, nothing
compares them, and the producer — the only party that knows its own cadence — states none.

So the mesh routinely holds, **at the same instant, from the same bytes**, two contradictory verdicts
about whether a sense is live. Every reader is internally consistent and honest; the contradiction
lives in the predicate, not the evidence, which is exactly why no instrument we own could see it.

## Prior art checked before landing (none of them is this)

Nine prior `distributed-systems-*` reviews in `docs/reviews/`: causal-stability frontier · CALM /
I-confluence double-hold · metastable failure · Lifeguard local health awareness · φ-accrual presence
departure · similarity-regime set reconciliation (ConflictSync / RIBLT) · AoII semantic divergence ·
causal delivery orphan-split · event-triggered broadcast snapshot. Plus the swarm-lane fusion
landings (collective-gradient margin, differential latency) and doctrine's `max-fold-effaces-the-
disjunction`.

The closest thing we already had is the **single-reader** version, and it is a memory, not an
instrument: `a-lease-must-exceed-its-producers-cadence` — `mesh-bruno`'s `MESH_BRUNO_LEASE_WIFI=600`
against a producer on a 600s cadence, found **by hand**, fixed by deferring to the producer's own
definition. Every freshness instrument in the genome is one-sided in the same way: `mesh-reflex-health`
judges a producer against its cadence, `mesh-doctor --supersede` judges an artifact against a knob
transition, `mesh-sync-tools` judges deployed against repo. **Each reader is judged alone**, so a
disagreement *between* readers is structurally invisible.

## Landed: `mesh-doctor --exclusion` (report-only, on-demand)

For every state artifact declared in the genome: find its readers (the writer is excluded — a
producer's own interval constant is a *write rhythm*, not an exclusion predicate), extract each
reader's max-age bound, and compare.

```
SPLIT          ≥2 readers, ≥2 distinct bounds → inside the band the mesh believes the sense is
               both live and dead.                                              FINDING (rc 3)
UNSATISFIABLE  a bound SHORTER than the producer's own declared cadence → it must read STALE on a
               perfectly healthy sense for (1 − bound/cadence) of every cycle.  FINDING (rc 3)
AGREED / SINGLE-READER / NO-BOUND-EXTRACTED                                     not findings
```

### What it found on this node, live

```
corpus: scripts · tools 634 · artifacts with ≥1 non-writer reader: 82 · bounds extracted: 28
verdicts: SPLIT 4 · UNSATISFIABLE 1 · AGREED 2 · SINGLE-READER 12 · NO-BOUND-EXTRACTED 64
```

| artifact | producer | band | readers |
|---|---|---|---|
| `.room-sense.state` | mesh-room-sense (5m) | **600s..1800s** | overview=600s@102 · activity=900s@100 · voice-tx=900s@312 · misha-gate=1800s@60 (+16 unbounded) |
| `.op-home.state` | mesh-operator-home (5m) | **600s..3600s** | overview=600s@101 · perimeter=900s@748 · arrivals=1800s@53 · cell-info=3600s@46 |
| `.ambient-clock.state` | mesh-ambient-clock (30m) | **600s..2100s** | overview=600s@103 · room-sense=2100s@327 |
| `.tamper-state` | mesh-tamper | **1500s..1800s** | room-sense=1500s@1169 · tamper-attrib=1800s@43 |

**UNSATISFIABLE — `.ambient-clock.state`:** `mesh-overview:103` bounds it at **600s** while its
producer declares `# reflex-cadence: 6-59/30` = **1800s**. The bound therefore expires while the
reflex is perfectly healthy, for **~66% of every cycle**, and `_stale()` prints a literal
`[Xm stale]` on the overview row for it.

Verified at the artifact, not from the arithmetic: at 09:36Z `.ambient-clock.state` held
`QUIET|dwell_s=12600` (the value unchanged for 3.5h) with an **mtime of 16 seconds** — the
liveness-touch convention working exactly as designed, the sense demonstrably live, and overview's
predicate calling it stale for two thirds of every half hour. This is the mesh's own
`a-lease-must-exceed-its-producers-cadence` failure, still live in a second organ eleven weeks after
it was named in the first, because nothing was looking across readers.

Every row cites `file@line` **in the raw file**, not in the stripped body this pass scans — a
finding you cannot open is a claim.

## Gates (11 legs) and mutants (10/10 RED)

Fixture corpus of synthetic tools; every leg drives the real `"$0" --exclusion`.

p1 split named with its band + both bounds · p2 the writer is not a reader and its `ZX_EVERY=120`
write rhythm is not a predicate · p3 UNSATISFIABLE names reader, bound, cadence and the false-stale
share · p4 agreement is not a finding · p5 a bound *looser* than the cadence is not unsatisfiable
(the check is not always-on) · p6 `_MIN` normalised to seconds (30min ≡ 1800s stays AGREED — read as
seconds it would be the loudest possible false split) · p7 a comment mention and a mention inside the
file's own `--test` block are not reads · p8 an all-unbounded artifact is counted, never accused, and
an unbounded reader still appears as evidence · p8b a rhythm-named constant is refused · p8c a
name-pair with a non-freshness segment does not bind · p9 the citation is the RAW file line · p10 a
corpus with no disagreement exits 0 · p11 no corpus = exit 2, and says n/a.

Mutants run from a scratch copy, each turning one gate RED: split-needs-3 · writer-not-excluded ·
rhythm-counted · no-minute-unit · no-unsat-check · stride-flattened · body-lines-not-raw ·
raw-not-body (comment/test mentions counted) · unbounded-treated-as-a-bound · pair-vocabulary-off.
**10/10 RED.** One assertion was found vacuous while writing it (p2 matched the owner label in the
row header, not the reader list) and was tightened to `mesh-zx-src=`.

## Boundaries — stated because they are load-bearing

1. **Extraction is syntactic** over the comment-stripped, `--test`-stripped body (`um_body`), with
   four accepted forms only: an age computed *from that artifact* and compared to a literal /
   `${K:-N}` / known constant; a freshness-named helper call carrying the bound as an argument; a
   constant whose NAME pairs with the artifact variable's prefix (`OPHOME_STATE` ↔ `OPHOME_MAXAGE`,
   every segment freshness vocabulary, one of them naming AGE); and `-mmin` (×60). Everything else
   reads **UNBOUNDED**, which is a **LEAD, never a finding** — the reader may make no liveness claim
   at all, or make one this pass cannot see. 169 of 197 reads on this node are unbounded; the
   instrument is deliberately conservative in the under-reporting direction.
2. **A bare integer in shell carries no unit.** A `_MIN` suffix in a freshness-named constant is read
   as minutes; a name saying EVERY/INTERVAL/PERIOD/CADENCE/SLEEP/TICK is a rhythm and is refused.
3. **Cadence parsing is partial by design** (`*/N`, `A-B/N`, `*`, fixed-minute-under-`*`-hours). An
   unparseable cadence simply skips the UNSATISFIABLE check — a *guessed* cadence would manufacture
   the finding it exists to detect.
4. **Report-only.** *Which* bound is right is a question about that sense's meaning and belongs to
   its organ. Naming the disagreement does not answer it.

## What is NOT landed (deliberately)

The ACFA-shaped fix is for the **producer to publish its predicate** and readers to derive from it
(the `mesh-bruno` → `mesh-wifi-motion GAP_LIMIT` move, generalised). That changes a state-file
contract read by 21 organs in `.room-sense.state`'s case — `a-format-fix-must-sweep-every-reader`
territory, and a separate task with its own sign-off. This lands the **detector** only: the mesh can
now see the divergence it has been carrying.

Suggested first repairs, in order of evidence: `mesh-overview:103`'s 600s bound on a 30-minute
producer (it is the one that is *provably* wrong, not merely different), then the `.room-sense.state`
band, where a 600s and an 1800s reader disagree about a sense the room mind acts on.
