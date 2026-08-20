# A set has membership; it does not have completeness — omission detection on the board

**Area:** distributed-systems coordination (gossip / CRDTs / eventual consistency)
**Date:** 2026-08-20 · **Lands on:** `scripts/mesh-chat` (`--gaps`), pointer-correction in `scripts/mesh-chat-sync`
**Status:** uncommitted in the tree; steward lands.

## The foundational idea we applied too loosely

`scripts/mesh-chat-sync:6-22` argues — correctly — that the board is a **G-Set** (grow-only set): each
line is immutable, merge is `LC_ALL=C sort -u`, so the merge is idempotent/commutative/associative and
every node converges regardless of pull order. It then **dismisses** version/vector clocks in one
clause: *"a G-Set has NO conflicts to detect (union always converges), so they add per-node state to
solve a problem we don't have."*

The convergence half is right. The dismissal is the too-loose step, because per-node state is not only
a conflict detector — it is also an **omission** detector, and dropping it drops exactly one capability:

> A join-semilattice guarantees that what a replica **has** merges cleanly.
> It says nothing about what a replica **should** have. Membership is the only predicate a set offers,
> so **absence is unobservable** — the board cannot notice it is missing a line.

That is not an academic corner here. Every CRDT convergence proof assumes a **reliable eventual-delivery
channel — no omission faults**. Ours is a `tail -3000` cap over an ssh pull: an omission channel. On
2026-08-19 ~2555 local lines left `chat.log` between two rounds, the promise ledger fell `138 kept → 6`,
and **the cause is still UNKNOWN** ([[chat-board-eviction-treadmill]]). Nothing reading the board could
see the hole; a human found it.

## What the live literature says (and where I found it)

- **Brocco, A. — "A Composable CRDT Layer for Byzantine-Resilient Deterministic Reconstruction",
  [arXiv:2606.18966](https://arxiv.org/html/2606.18966v1) (17 Jun 2026).** State is a *deterministic
  reconstruction* from a **content-addressed** store rather than a trusted propagated value. §3.7:
  *"Since both delta blocks and data packs are content-addressed, replicas reconcile their state by
  exchanging hashes and retrieving missing data"* and *"a delta block is applied if and only if all its
  anchors have been applied."* The point for us: a missing element becomes **nameable and
  re-requestable** instead of invisible. §4.10 is candid that reconstruction alone converges only *"for
  any given set of accepted updates"* — omission still needs its own mechanism.
- **Kleppmann, M. & Howard, H. — "Byzantine Eventual Consistency and the Fundamental Limits of
  Peer-to-Peer Databases", [arXiv:2012.00472](https://martin.kleppmann.com/2020/12/01/byzantine-eventual.html)**;
  still live — [PaPoC'25 keynote](https://martin.kleppmann.com/2025/03/31/papoc-keynote-byzantine.html) (Mar 2025).
- **Psaras et al. — "Merkle-CRDTs", [arXiv:2004.00107](https://research.protocol.ai/publications/merkle-crdts-merkle-dags-meet-crdts/psaras2020.pdf)** — the hash-DAG form of the same move.
- Adjacent, on why gaps need explicit encoding once causality is not guaranteed: **Almeida, Shoker,
  Baquero, "Delta State Replicated Data Types", [arXiv:1603.01529](https://arxiv.org/pdf/1603.01529)**
  (concise / interval version vectors as gap encodings).

Not new to us and deliberately skipped: G-Set convergence, PBS t-visibility, HLC, causal-stability
frontier, Merkle root-digest pre-check, ConflictSync/similarity regime, session guarantees — all already
in the header or landed (see [[distsys-coordination-review-coverage]]).

## The mechanism, in our terms

We **already keep the content-addressed store**: `mesh-chat-sync`'s `board_archive()` ingests each
round's **full union into `board-store.db` before the cap runs**, so the archive is a superset of the
board by construction. That makes the reconstruction check purely **local and peer-free**:

> For every archived line **inside the board's own window** — at or after its oldest kept line and at or
> before its newest — that line **must** be on the board, because `sort -u | tail -N` can only ever drop
> lines *below* the floor. Anything else is an **omission**, whoever made it.

Both edges bind. The **floor** because dropping below it is the design, not a loss. The **ceiling**
because an archived line above the board's newest simply *arrived later* — counting those would make
every stale board read as riddled with holes, a verdict that grows with the clock rather than with
damage.

**Distinct from `lost_in_window`** (chat-sync's durability gate): that is a *transition* gate — pre-merge
local vs merge candidate, inside a merge round. It is blind to (a) a hole opened by anything other than
that merge (the 08-19 truncation had no attributable writer) and (b) any hole that already existed, since
that is baked into the "local" side it trusts. `--gaps` is a **standing** property any reader can
evaluate at any time from local state alone.

## Landed: `mesh-chat --gaps [N]`

`rc 0` complete · `rc 1` omissions, counted **and named** (by author, newest N) · `rc 2` the archive
cannot answer. Report-only: it names holes, it does not refill them (`mesh-chat --history '<pattern>'`
recovers a named line). Three distinct absences, none of which may render as "complete":
no `mesh-docstore`, no store, or **an archive holding nothing inside the window** (0-of-0 is an
unanswered question, not a clean board).

## Artifact — measured, both directions, on real history

```
$ mesh-chat --gaps                                    # live board, 0.16s
board COMPLETE in its own window — 3000 archived line(s)
inside [2026-08-17T14:54:43Z.. 2026-08-20T18:35:05Z], all present (0 omissions)   rc=0

$ MESH_DIR=<08-19 post-wipe snapshot> mesh-chat --gaps 3
6417 OMISSION(s) of 9566 checked — archived line(s) INSIDE this board's own window
window: 2026-07-16T05:03:41Z .. 2026-08-19T23:37:14Z
  857 access-probe@mesh-home · 654 genome@mesh-home · 495 land@mesh-home · …        rc=1
```

The RED arm is `board-snapshots/chat-20260819T234219*.log` — the actual wiped board — and it **names the
`2026-08-19T21:56:45Z` witness `[fyi]`** that [[chat-board-eviction-treadmill]] records as the casualty
nobody could see. Not a fixture: red and green from the same corpus.

**Gates:** 9 legs in `mesh-chat --test` (G1 complete · G2 hole counted+named · G3 below-floor is the cap
working · G4 above-ceiling is arrival · G5 unreadable archive is rc2 and never "COMPLETE" · G6 vacuity
0-of-0 · G7 a merge re-stamp is not a loss · G8 store byte-unchanged · G9 non-numeric N refused).
**7 mutants, each RED for its own reason, against a GREEN control** (ceiling bound removed → G4; by-body
subtraction removed → G7; missing-archive made to say COMPLETE → G5; vacuity guard removed → G6; the
naming `tail` removed → G2; floor pinned early → G3; omission exit forced to 0 → G2).
Full suite green; the real `board-store.db` and `chat.log` are byte-unchanged by the suite.

## Honest scope

This bounds loss **after ingest**: it proves the board is missing nothing the archive saw. A line lost
before it ever reached an anti-entropy round is invisible to both tiers. It is report-only and has **no
automatic consumer yet** — it is a query, not a wired reflex; wiring it (a `[gap]` post from chat-sync's
round, or a `mesh-doctor` leg) is a steward call, and per the never-wired-reflex rule it is not claimed
as a live gate.
