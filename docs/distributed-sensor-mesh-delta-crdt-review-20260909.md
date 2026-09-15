# Delta-state CRDTs for the sensor mesh — live literature review

**Review date:** 2026-09-09  
**Disposition:** applicable; propose one bounded application, implementation deferred.

## Finding: delta-state CRDT anti-entropy with causal delta intervals

The uncovered mechanism is not “use a CRDT” or “gossip more.” It is a **delta-state CRDT**: a
state-based CRDT whose mutation produces a small joinable delta, so replicas exchange recent
state fragments rather than the entire state. The important safety refinement is the paper’s
**causal delta-merging condition**: a receiver joins a delta interval only when it already
subsumes the state at the interval’s start. That preserves the result of full-state merging while
allowing lossy, duplicated, reordered transport.

Almeida, Shoker, and Baquero define the delta-CRDT model and show both eventual-convergence
anti-entropy and a causal interval-based algorithm in *Delta State Replicated Data Types*
(arXiv:1603.01529, 2016), especially §§4–6 and the causal-consistency corollary:
[paper and full text](https://arxiv.org/abs/1603.01529). This remains relevant to the live edge
case because the 2025 ECOOP/PLF+PLAID work explicitly targets microcontrollers with 520 KB of
SRAM; it reports that ordinary vector-clock metadata scales poorly and presents an optimized
delta-vector-clock design integrated with causal-stability bookkeeping, reducing the added
overhead from O(n²) to O(n): [Vandermotten, Bauwens & Gonzalez Boix, “Optimizing CRDTs for Low
Memory Environments”](https://2025.ecoop.org/details/plf-plaid-2025-papers/3).

## Why this is genuinely absent here

The mesh already has a G-Set-shaped append-only board and gossip/anti-entropy. `scripts/mesh-chat-sync`
does union/sort/dedup over pulled board lines; `scripts/mesh-knowledge-sync` uses bidirectional
`rsync --update` of whole knowledge files. Those are convergence mechanisms, not delta-state
transport. Neither `scripts/mesh-sensor-log` nor the sync tools maintain per-sensor causal
intervals, per-peer acknowledged frontiers, or a rule that rejects a delta whose causal anchor is
not present. The codebase mentions delta-CRDT literature, but does not embody this mechanism.

## One concrete cross-domain application

Apply it to the **sensor/reflex lane in `scripts/mesh-sensor-log`**. Keep each reading as an
immutable event identified by `(node, sensor, sequence)` and maintain a per-node sequence frontier.
On each five-minute collection, package only the new rows since the last acknowledged frontier as
a delta interval; gossip that interval to a reachable mind or phone. The receiver should:

1. persist the interval’s predecessor/frontier and rows atomically;
2. join duplicate or reordered intervals idempotently, but hold an interval whose causal anchor is
   missing; and
3. acknowledge the highest contiguous sequence, so the sender can compact already-stable rows
   without losing a partitioned phone’s readings.

The first consumer should be the existing `--edge` room-movement reflex in the same file: it would
classify `MOVED` only from a causally complete local window, and mark a gap as `UNKNOWN` rather than
mistaking “no row arrived” for “the room did not move.” This is a small, testable transfer: it
reduces LTE/phone sync bytes and makes sensor-history omissions observable while preserving the
mesh’s append-only evidence. It should begin as a local fixture-backed adapter, not replace the
chat board or introduce a second coordination substrate.

## Decision

**Land the concept as a design lead, not code:** the next implementation task is a bounded
`mesh-sensor-log` delta-envelope/ack-frontier experiment with a partition-and-reorder fixture.
Require a real artifact showing bytes sent versus full-log transfer, convergence after replay, and
an explicit `UNKNOWN` gap. No new reflex is wired by this review.

