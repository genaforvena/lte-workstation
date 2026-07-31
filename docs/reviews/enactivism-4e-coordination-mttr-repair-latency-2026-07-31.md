# Enactivism/4E · coordination recovery latency (MTTR-A) as the *repair* axis of the promise ledger

**Date:** 2026-07-31 · **Lane:** LITERATURE (live review) · **Organ:** `scripts/mesh-promises` (new `--mttr`)

## The concept we did not embody

Enactivism's account of *social* cognition — **participatory sense-making** (De Jaegher & Di Paolo,
"Participatory Sense-Making: An Enactive Approach to Social Cognition", *Phenomenology and the
Cognitive Sciences* 6:485–507, 2007, doi:10.1007/s11097-007-9076-9) — turns on the **"autonomy of the
interaction process"**: when two or more autonomous agents couple, the *interaction itself* becomes a
relational domain with its own dynamics, sustained not by steady synchrony but by an ongoing cycle of
**coordination breakdown and repair**. The health of a coordination medium therefore lives in its
**repair dynamics** — how fast the joint process re-coordinates after a rupture — not in the momentary
count of things currently out of joint.

The **live operationalization** of exactly this, in the distributed-systems literature, is fresh:
**MTTR-A — "Measuring Cognitive Recovery Latency in Multi-Agent Systems"** (Barak Or, arXiv:2511.20663,
submitted 8 Nov 2025). It adapts classical dependability theory to agentic orchestration: a runtime
reliability metric = *the time required to detect reasoning drift and restore coherent operation*,
treating a multi-agent system "as a single cognitive organism whose communication and recovery pathways
determine runtime resilience" (complemented by MTBF and a normalized recovery ratio).

Found via live web search (July 2026): the enactive framing and the arXiv:2511.20663 operationalization
were located and cross-checked against the paper's abstract; neither is in the genome.

- Enactive source: <https://link.springer.com/article/10.1007/s11097-007-9076-9>
- MTTR-A: <https://arxiv.org/abs/2511.20663>

## The gap (applied too loosely)

`mesh-promises` replays the board into a double-entry ledger of promises/claims/holds. **Every axis it
reports is a STOCK measure** — the *open, aged, unrepaired* liabilities: leaks (`--report`), CALM
double-holds (`--collisions`), reflex-broadcast write-offs, order-word re-issues (`--redundancy`), Pask
teachback vs ack on redemption (`--teachback`). It answers "what is currently out of joint," never "how
long did the joints that *did* re-coordinate stay broken."

The striking part: the **repair latency is already computed** — the journal writer stamps
`lag:%sh = keep_ts − open_ts` on every kept episode (`mesh-promises:692/713/741`) — but it is **inert**,
buried in hledger tags, never aggregated or surfaced. A board with **zero leaks** but a *rising* close
latency is a coordination medium **degrading in precisely the dimension the stock detector is blind to**:
the interaction still repairs every rupture, but slower and slower. That is the enactive claim made
measurable, and the mesh was not measuring it.

## The application (report-only, additive)

`scripts/mesh-promises --mttr` — the **FLOW** axis complementing the stock axes. For every *kept*
episode across all three claim families it computes recovery latency `keep_ts − open_ts` and reports the
distribution per family and pooled:

```
mesh-promises MTTR (coordination recovery latency — repair, not stock; target 24h) · 13:28Z
  promise  n=78 median=0.4h p90=24.3h max=74.4h
  claim    n=6  median=17.6h p90=64.3h max=66.6h
  hold     n=39 median=0.2h p90=9.5h max=153.0h
  POOLED   n=123 median=0.3h p90=23.7h max=153.0h   (the mesh's coordination MTTR)
  slowest repairs (breakdowns that took longest to re-coordinate — the repair tail):
     153.0h  tg           operator-diary-transcription-batch2
      74.4h  health       sysfs-over-uxn-transport
      ...
```

Design guarantees, in the file's established idiom:

- **Still-open episodes are EXCLUDED** — an unkept promise is an *unrepaired* breakdown, not a recovery
  time; it already shows up in the leak (stock) axis. Counting it would conflate the two.
- **Report-only, exit 0** — a distribution, not a gate (like `--redundancy`/`--teachback`). The leak
  report stays the exit-1 signal; behaviour belongs to the steward. A soft `⚠ median>target` annotation
  fires per family, env-tunable via `MESH_PROMISE_MTTR_TARGET_H` (default 24h).
- **Data-frugal** — pure derivation over the existing episode replay; no new parse, no new state, the
  three open/leak paths and the journal are byte-identical.

### Verification (RED-first, `--test` leg 34)

A synthetic board with two kept promises at **known** latencies (2.0h, 10.0h) + one still-open. The leg
asserts `promise n=2` (open excluded), `max=10.0h` (latency measured from `keep_ts`), and that the open
slug never appears. Both mutations reddened distinct assertions and restore went green:

- latency from `now` instead of `keep_ts` → RED on `max=10.0h`
- include still-open episodes (`cts=now`) → RED on `n=2`

Full `--test` (34 legs) green after restore.

## Distinctness from prior enactivism landings

The 2026-07-27→30 landings on this frontier (complexity-matching lead/lag, reafference confirmation,
enactive valence, extended-mind trust-glue, representation-hungry absence) all live on *sensing/coupling*
organs. This one lands on the mesh's *social* coordination substrate — the board-as-interaction-process
— and adds the **temporal repair** dimension that participatory sense-making says is where coordination
health actually lives, using a Nov-2025 metric that did not exist when this file was first built.

**Status:** uncommitted in-tree for the steward. Not committed. Not deployed (genome source only).
