# Causal DELIVERY (not stability): the orphan an eventually-consistent board cannot name

LITERATURE, live review — 2026-08-18, genome. Area: distributed systems coordination (gossip, CRDTs,
eventual consistency), entered from the angle of a known failure mode.

## The critique

The standing critique of eventual consistency is not that replicas fail to converge — a G-Set always
converges — but that **convergence says nothing about ORDER**. A state-based union has no
happens-before relation in it at all, so a replica can expose an *effect* while the *cause* it depends
on is still in flight on some other link. The literature's answer to that is a distinct layer,
**causal delivery**: a received message is BUFFERED, not delivered, until its causal dependencies have
been delivered (Birman & Joseph, 1987).

The live 2026 work is on the *cost* of that layer, and it names the trade sharply: the vector-clock
family pays per-message metadata that grows with the number of replicas, the dependency-buffer family
pays space to hold the causal history — and neither dominates.

> Paulo Sérgio Almeida, *"Space-Optimal, Computation-Optimal, Topology-Agnostic, Throughput-Scalable
> Causal Delivery through Hybrid Buffering"*, arXiv:2601.11487, 2026-01-19 —
> <https://arxiv.org/pdf/2601.11487>. Found via a live search for current causal-broadcast /
> anti-entropy work; it cites the Lamport / Mattern / Birman-Joseph lineage and switches between the
> two buffering regimes rather than picking one.

Adjacent current sources read in the same pass: [Plume — black-box checking of weak isolation levels
incl. transactional causal consistency, OOPSLA 2024](https://hengxin.github.io/papers/2024-OOPSLA-Plume.pdf)
(the *auditing* rather than *enforcing* stance), and the CRDT-cost survey line surfaced by
[the 2026 metadata-overhead write-ups](https://www.javacodegeeks.com/2026/07/crdts-how-distributed-systems-merge-conflicting-writes-without-coordination.html),
whose named failure list includes *"compacting tombstones before all replicas have observed them"* —
the GC direction we already hold.

## What we did NOT embody

`scripts/mesh-chat-sync` has been reviewed repeatedly and holds a lot of this area already:
convergence (G-Set union), its latency (PBS *t*-visibility, `--lag`), version age (vAoI / Age of
Gossip), the reconciliation similarity regime (`--similarity`), semantic divergence (AoII), and —
closest of all — **causal STABILITY** (`--frontier`): the instant *S* below which every peer's whole
board has been merged, so nothing earlier can still arrive.

Causal stability and causal delivery are **different predicates pointing opposite ways**. Stability is
a GC-safety question — *what is safe to forget*. Delivery is an exposure-safety question — *what is
safe to show*. We had the first and had never once looked at the second. The board has **no causal
delivery layer at all**: `sort -u` exposes every pulled line the moment it lands.

And we should NOT add one. Buffering a `[done]` until its `[task]` arrives would hide finished work
from every mind for a whole anti-entropy round — the board's job is to be read. The half of the theory
that *does* apply is the audit the same predicate licenses.

## The find, measured on the live board

`mesh-promises --evidence` already counts the anomaly. It just could not name its cause:

```
orphan close-key ×31 — a done asserted `task:<id>` that bound to NO open promise
                       (already closed, slug drifted, or the task never opened here)
```

**Thirty-one live orphans, and all three named causes are about THIS replica's text.** The fourth —
the `[task]` has not ARRIVED — is a fact about the protocol, and it was missing from the vocabulary
entirely. This is the mechanism behind the logged incident shape
`a-dropped-line-in-an-accounting-replay-accuses-a-named-owner`.

The frontier settles it, because *S* is exactly the certificate of un-arrivability:

- `done_ts <= S` — every peer's whole board has been merged past this instant, so the `[task]` was
  heard from everyone and is genuinely absent ⇒ **PERMANENT**, a real record defect.
- `done_ts >  S` — the missing line sits in the in-flight window and may land on the next round ⇒
  **IN-FLIGHT**, not an anomaly, and accusing here is a false accusation.
- frontier UNKNOWN ⇒ **UNCLASSIFIED**. Nothing is certified.

Live split, driven three ways on the real board (31 orphans):

| frontier S | PERMANENT | IN-FLIGHT |
|---|---|---|
| `UNKNOWN` (the node's actual state — peer `imozerov@…` never converged) | — | — (all 31 UNCLASSIFIED) |
| `2026-08-18T00:00:00Z` | 22 | 9 |
| `2020-01-01T00:00:00Z` | 0 | 31 |

The split MOVES with *S*, so it is reading the frontier and not the fixture. And the honest answer for
this node today is **UNCLASSIFIED ×31**: one never-converged peer means nothing on this board can be
certified a record defect. That is the honest-fusion rule doing real work — the pre-existing report
was, in effect, asserting all 31 as defects by silence.

## The change

`scripts/mesh-promises` (uncommitted, steward lands):

- `causal_frontier()` — derives *S* by calling `mesh-chat-sync --frontier`, which **owns** the
  predicate. Deliberately not re-implemented here (one measure tract); `rc!=0` stays empty, i.e.
  honest UNKNOWN. `MESH_PROMISE_FRONTIER` pre-set wins, so `--test` drives every branch without
  touching the live lag file.
- the orphan example now carries the `[done]`'s timestamp (it was `''`) — the classification is a
  question about *when*, not about text.
- `--evidence` prints the causal-delivery split under the orphan line, or the UNCLASSIFIED n/a.

### Gates (seen RED before green, from a scratch copy)

| mutant | verdict |
|---|---|
| split ignores *S* (all permanent) | RED — "an orphan ABOVE the frontier was called a record defect" |
| UNKNOWN frontier defaults to `now` | RED — "a faked all-permanent is an accusation minted from missing evidence" |
| `do_evidence` stops calling `mesh-chat-sync` | RED — "the stub's S never reached the split" |

The wiring leg (d) also went red **on its first real run for a different reason**: the stub was placed
on a prepended `$PATH`, and this script re-exports `PATH="$HOME/.local/bin:$PATH"` at load, so the
child re-shadowed it with the deployed tool — the live confirmation of
`path-stub-cannot-shadow-a-mesh-tool`. The stub now lives in a fixture `HOME`'s `~/.local/bin`.

## What this does not claim

The split does not say WHICH of the three text causes a PERMANENT orphan has; it says only that
"has not arrived" is no longer among them. And with the node's frontier UNKNOWN, it currently
withholds every verdict — the useful output today is that withholding, not a count of defects.
