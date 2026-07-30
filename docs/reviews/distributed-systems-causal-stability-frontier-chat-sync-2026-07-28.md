# Distributed-systems coordination — the causal-stability frontier (live review, 2026-07-28)

**Area:** distributed systems coordination — gossip / CRDTs / eventual consistency, from the angle of a
concrete metric the field uses to measure itself.

## What the mesh already embodies (checked the artifact first, did not re-propose)

`scripts/mesh-chat-sync` is the mesh's eventual-consistency substrate: the board (`~/.mesh/chat.log`) is
a **grow-only set (G-Set)** — the simplest state-based CRDT — converged by union/sort/dedup anti-entropy.
Its header already cites and embodies, explicitly:

- **Convergence mechanism** — G-Set union (idempotent/commutative/associative). `:5-22`
- **Latency metric — PBS t-visibility** (Bailis et al., *Probabilistically Bounded Staleness for
  Practical Partial Quorums*, VLDB 2012) → `--lag` = now − last-successful-pull, per peer.
- **Version-age / vAoI** (Age-of-Gossip line — Kaswan/Mitra/Srivastava/Ulukus, IEEE Trans. Comm. 2025,
  arXiv:2312.16163) → realized version deficit `gained@last` per peer.
- **HLC sort-ordering** (hlc-causal-order, 2026-07-23) → same-second posts get a causal total order.
- **Merkle-tree anti-entropy efficiency** (Dynamo, DeCandia et al., SOSP 2007) → documented as the
  missing *efficiency* metric, HELD/steward-gated. `:461-478`

Two of my first candidates (PBS/t-visibility, delta-state anti-entropy) turned out **already embodied** —
exactly the "check the artifact, don't propose the embodied" trap. Went further.

## The concept we do NOT embody: causal stability

**Causal stability** — Baquero, Almeida & Shoker, *Making Operation-Based CRDTs Operation-Based*, DAIS
2014 (https://hal.science/hal-01287738); metadata-reduction application in Bauwens & De Koster, *From
Causality to Stability: Understanding and Reducing Meta-Data in CRDTs*, MPLR 2020
(https://soft.vub.ac.be/~jibauwen/publications/mplr20-from-causality-to-stability-jimbauwens.pdf).

> A message with timestamp *t* is **causally stable** at node *i* once every message subsequently
> delivered at *i* has timestamp *t′ ≥ t* — i.e. no operation concurrent to it can still occur. It is
> the **safety predicate for garbage collection / settlement**: only a causally stable operation is safe
> to treat as final and to strip of its causal metadata.

This is **distinct from everything the mesh has**. `--lag` and vAoI are **per-peer and backward-looking**
("how stale is each peer's view of us"). Causal stability is **fleet-wide and forward-looking** ("below
which timestamp is a line *final* — safe to settle, safe to GC"). The mesh measures how far behind each
peer is; it never certifies that a given board line will **never be contradicted** by a late arrival.
That gap is load-bearing: `mesh-promises` settles claims (`[task]→[done]`, `[taking]→redeemed`) purely
from the **local** board view — grep confirms zero propagation/stability awareness — so a claim can be
flagged **leaked** while its settling `[done]` is merely in-flight on an unsynced peer. Premature-settle
is precisely the double-dispatch hazard the whole board discipline exists to prevent.

## Application (implemented, uncommitted): `scripts/mesh-chat-sync --frontier`

The data is **already on disk** — `~/.mesh/.chat-sync-lag` (LAGF) holds each peer's last-successful-pull
epoch. The causal-stability frontier is one min-reduction over it:

> **S = min over KNOWN peers of (last-successful-pull epoch).** At epoch e_p we merged peer p's *whole*
> board (G-Set union), so any line older than min_p(e_p) has been heard from **every** peer and cannot
> be contradicted by a late arrival — causal stability for an append-only log.

`--frontier` reports S (ISO-8601), the limiting peer, and partitions the current board into **stable**
(ts ≤ S) vs **in-flight** (ts > S). ISO-Z timestamps sort lexically == chronologically, so the partition
is an `awk` string compare — no per-line `date` spawn on a 3000-line board.

**Honest-fusion (n/a-is-a-claim):** a **never-converged** peer (epoch 0) forces `S = UNKNOWN` + rc1 — it
may hold an arbitrarily old un-merged line, so *nothing* can be certified stable. An unreachable input
renders UNKNOWN, never a faked all-clear.

**Consumer named (not yet wired, steward-gated):** `scripts/mesh-promises` should not flag an open claim
as LEAKED while its settling `[done]` may simply be in-flight above the frontier — a claim inside the
board's in-flight window is *un-settleable-yet*, not leaked.

### Verification

- Live `--frontier` on crafted state: board `21:00 / 22:13:20(=S) / next-day-05:00`, peers at epochs
  min=1700000000 → **`STABLE<=2023-11-14T22:13:20Z (limiting peer nodeA@n); board 2 stable / 1 in-flight`**
  (the exactly-at-S line counts stable; correct).
- `--test`: added assertions for the happy partition AND never-converged→UNKNOWN+rc1. Passes 5/5.
  (The one pre-existing flaky assertion — a flock-serialization race — fails ~1/5 on **untouched HEAD**
  too; orthogonal to this change.)
- **RED-first:** flipping the min-selection to max makes the frontier `--test` assertion fail with
  `S must be min peer epoch as ISO` — the gate bites. Restored.

**Artifact:** `scripts/mesh-chat-sync` (+56 lines, uncommitted) — `--frontier` verb + `--test` gate.
