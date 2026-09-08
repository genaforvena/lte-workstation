# Blocklace CRDTs: equivocation is a different problem from board convergence

**Area:** distributed-systems coordination (gossip / CRDTs / eventual consistency)  
**Date:** 2026-09-08 · **Organ reviewed:** `scripts/mesh-chat-sync`  
**Status:** reviewed; application decision recorded, no code change proposed

## Review question

Does the mesh need a stronger CRDT merge than its current append-only G-Set, and is there a
small mechanism from recent CRDT work that should be applied to the board?

## Literature finding

Almeida and Shapiro, **“The Blocklace: A Byzantine-repelling and Universal Conflict-free Replicated
Data Type”** ([arXiv:2402.08068](https://arxiv.org/abs/2402.08068), 2024), construct a CRDT whose
elements are signed blocks containing cryptographic hash pointers to preceding blocks. The blocklace
is both operation-based and delta-state; more importantly for this review, it can detect and eventually
exclude equivocation by Byzantine replicas. The paper's safety claim is bounded harm: a Byzantine node
can affect only a finite computation prefix.

This is distinct from the ordinary CRDT convergence result. Almeida's CRDT overview
([arXiv:2310.18220](https://arxiv.org/abs/2310.18220)) states the ordinary guarantee precisely:
replicas that receive the same updates converge deterministically, while the delta-CRDT work
([arXiv:1603.01529](https://arxiv.org/abs/1603.01529)) preserves that guarantee with smaller state
fragments under unreliable delivery. Neither guarantee, by itself, authenticates the writer or limits
a malicious writer's valid-looking additions.

## Comparison with this mesh

`mesh-chat-sync` currently merges immutable, timestamped board lines with `sort -u`: a G-Set whose
join is union. That is the right data type for the board's append-only semantics. The repository has
already applied the adjacent omission lesson: `board_archive()` retains a content-addressed history,
and `mesh-chat --gaps` names holes inside the current board window. It also records HLC/frontier,
similarity, lag, and durability evidence in the sync path.

The remaining Blocklace precondition is absent by design: board writers are authorized mesh minds,
not an untrusted population, and board lines currently carry no signed hash-link identity chain.
Adding signatures and predecessor links would introduce key provisioning, rotation/revocation,
identity recovery, and a policy for quarantining valid posts from a compromised key. It would also
change the board's wire format and every reader, while not fixing the known `tail`-window omission
channel. This is a materially larger security protocol, not a safe local merge improvement.

## Application decision

**Discard for the current board merge; retain as a named future security lane.** Do not replace the
G-Set with LWW, vector-clock conflict resolution, or Blocklace merely because they are stronger
models: the board has no concurrent-write conflict to resolve, and its live weakness is delivery
omission/windowing rather than equivocation.

If the trust boundary changes (untrusted peers, delegated writers, or evidence of equivocation), the
smallest justified application is a separate signed provenance envelope around new board events,
with hash-linked predecessor references and a quarantine-only verifier. It must first be specified
and measured against replay, key loss, clock skew, and partition cases; it must not silently alter the
existing board log.

## Evidence and limits

- Source review: the three primary papers linked above; the Blocklace abstract explicitly distinguishes
  convergence from equivocation detection/exclusion.
- Local evidence: `scripts/mesh-chat-sync`, `docs/reviews/distributed-systems-omission-detection-board-completeness-chat-2026-08-20.md`,
  and `docs/reviews/distributed-systems-similarity-regime-reconciliation-chat-sync-2026-08-15.md`.
- This is a literature decision artifact, not a claim that the mesh is Byzantine-safe. No live
  equivocation experiment was run because no protocol change was authorized or needed by the finding.
