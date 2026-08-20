# Two complete samples are not one instant — maxwait on the BLE fusion

**Area:** distributed-systems coordination (gossip / CRDTs / eventual consistency)
**Angle:** an OPERATIONAL mechanism from the live literature, not a philosophy
**Date:** 2026-08-20 · **Lands on:** `scripts/mesh-presence-fuse`
**Status:** uncommitted in the tree; steward lands.

## How the search ran (live, not a fixed list)

`docs/reviews/` already holds **13** distributed-systems reviews, so the first job was to find where
we have *not* been. Covered already: causal stability frontier, AoII/version age, CALM/I-confluence,
causal delivery, era/epoch finality, event-triggered snapshot, phi-accrual, metastable failure,
omission detection, similarity-regime set reconciliation, ACFA, tunable quorum, local health
awareness. Two of the strongest hits in a plain web sweep — Brocco's content-addressed delta
reconstruction and the ACFA paper — were **already embodied**, which is the search working.

So the sweep went to the arXiv API sorted by submission date
(`abs:"CRDT" OR "conflict-free replicated" OR "anti-entropy" OR "eventual consistency"`, 60 most
recent). That listing is genuinely live: 30 of the 60 were submitted in 2026. Candidates read in
full-abstract: *Relay-Based Synchronization of RDTs in Opportunistic Networks* (arXiv:2605.22491),
*Wait-free RDTs and Fair Reconciliation* (arXiv:2508.18193), *Asynchronous Checkpoint for
Eventually Consistent Databases* (arXiv:2510.06404), *Semantic Conflict Model* (arXiv:2602.19231),
*Holon Streaming* (arXiv:2510.25757), *Arbitration-Free Consistency* (arXiv:2510.21304).

## The concept we did not embody

**MAXWAIT** — Lee, Lohstroh, Menard et al., *"Maxwait: A Generalized Mechanism for Distributed
Time-Sensitive Systems"*, **arXiv:2601.21146** (Jan 2026), implemented as an extension to the
Lingua Franca coordination language. Read: §III (the advancement rule) and §IV-F (the handler).

The mechanism is one declared parameter, `@maxwait(d)`, on a consumer. It gives a consumer **three**
outcomes where the usual design has two. A federate may advance its tag to *t* when:

- **1a** — "all input ports are known up to and including tag *t*": a **consistent cut**; or
- **1b** — the physical clock reads ≥ *t* + maxwait: **proceed without knowing**.

An input that then arrives bearing a tag earlier than the tag already advanced past is **tardy** — a
safe-to-process (STP) violation — and it is a **first-class event with its own handler**
(`reaction(...) {= … =} tardy {= … =}`). The paper's own framing is what makes it bite here: a CRDT
*is* `@maxwait(0)` (§IV-C) — process whatever arrived, whenever it arrived. That is sound for a
join-semilattice, because a join is order-independent. **It stops being sound the moment a consumer
compares two replicas' values to derive a verdict, because a comparison is not a join.**

Nothing in the mesh carries this distinction. Our honest-fusion doctrine ("an unreachable input
renders UNKNOWN/partial, never a faked all-clear") is a **completeness** predicate with no clock in
it — precisely maxwait(0) with no tardy notion. It asks *did every input arrive*, never *were they
of the same instant*.

## Where it bites: `scripts/mesh-presence-fuse`

`check_tracked_zones` already carries the right sentence, and it is half the rule:

> A missing peer is not a movement event. Require both observations before changing zonal state,
> otherwise peer loss can fabricate MOVED/GONE edges.

`SCAN_COMPLETE` implements exactly that and no more. But `scan_both` is **sequential**: the local
BLE window runs, *then* the peer window runs over SSH. Measured from the code's own constants:

| cycle | gap between the two sampling windows |
|---|---|
| healthy, no retry | ~26–45 s (bounded by `scan_to = scan_win + 35` by construction) |
| either arm takes its retry-once | ≥ `MESH_FUSE_RETRY_DELAY_S` (25 s) + a whole failed `scan_to` → **70–160 s** |

`closest_node` then compares `self_rssi` against `peer_rssi` as if simultaneous, and that comparison
is the *entire* zonal verdict — the `Closest` column, the person-zone map in `ble-spacemap.state`,
and the `ARRIVED`/`A→B` edges `check_tracked_zones` posts to the board. A person crossing the flat
inside that gap is not merely measured noisily: they are localized to whichever vantage happened to
sample them nearer, so **the skew itself fabricates the very MOVED/ARRIVED edge the completeness
gate exists to prevent**. Same fabrication, second cause, and the gate is structurally blind to it —
there is no timestamp anywhere in the fusion path to be blind *with*.

Note which half is fine. BLE **membership** is join-shaped: "device X was in this vantage's range"
is monotone and skew-tolerant, so `overlap` / `unique` stay valid at any gap. Only the cross-vantage
comparison needs a cut. The fix must not throw the good half away with the bad.

## What landed (uncommitted, in the tree)

`scripts/mesh-presence-fuse` gains the missing **time axis** — not a new sense:

1. `scan_both` stamps each arm's **final (post-retry) attempt** with its own epoch — the window the
   RSSI values actually came from, not the first try. An arm that produced no sample gets **no**
   epoch, so a half-failed cycle can never render a fake `0 s` "perfectly simultaneous".
2. `skew_verdict <local> <peer> <maxskew>` — pure, no globals, no side effects → `ok` / `skew` /
   `na` (rc 0/1/2). `na` is its own word: *could not check* and *checked and fine* are different
   facts.
3. `MESH_FUSE_MAXSKEW_S` defaults to **`scan_to`**, i.e. `scan_win + 35` — **derived, not invented**.
   A non-retried cycle is bounded by `scan_to` by construction; any retried arm exceeds it by
   construction. The bound separates the healthy path from the retried one with **no new constant**.
4. Behaviour on `skew`, deliberately narrow: membership columns still print; the `Closest` column
   prints under a banner saying it is not a cut; person-zone and `ble-spacemap.state` render
   UNKNOWN; and `check_tracked_zones` **retains state and fires no edge**, logging why. A real move
   is *deferred, not lost* — state is retained, so the next clean cycle fires it.
5. `skew=<n>s/<verdict>` is written to `presence-fusion.log` **every** cycle, ok or not, so the knob
   is calibrated against the real corpus of sequential-scan gaps instead of defended in prose.
6. `FUSELOG` (`MESH_FUSE_LOG`) — the zonal log is now a variable so `--test` drives the real
   functions against a throwaway file. A dry-run appending to the durable log forges the liveness
   evidence a reader uses to believe the reflex ran (09f7914).

This is a maxwait bound **without** a tardy handler, and the review is explicit about why: a BLE scan
cannot be re-tagged after the fact, so at the bound the only honest option is to refuse the
comparison rather than publish an unmarked guess.

`closest_node`, `resolve_tracked` and `check_tracked_zones` were **hoisted above the arg-parse loop**
— the same reason `scan_both` already sits there. A `--test` that cannot *call* a function can only
assert its source text, and source text is never behaviour; this is what let the new gate drive the
real edge path. A structural gate keeps them there.

## Gates — and each one seen RED

`--test` gains 8 pure `skew_verdict` assertions, a REAL-DRIVE of `scan_both`'s stamping (both arms
stubbed on PATH, the local stub sleeping 1 s so the gap is *measured*, driven once under a 999 s
bound and once under a 0 s bound), and a REAL-DRIVE of the edge suppression **with a control arm**
(same inputs, consistent cut → the edge must fire; without that arm the suppression gate would also
pass on a function that emits nothing at all).

Falsification drill — three mutants, each run and each red:

| mutant | verdict |
|---|---|
| skew branch in `check_tracked_zones` removed | `FAIL (a SKEWED cycle fabricated a zonal edge: … 'Phone' ARRIVED near mesh-home (self=-40 peer=-80))` |
| peer epoch stamp removed | `FAIL (scan_both did not stamp the arms — SCAN_SKEW_S empty, the cut has no time axis)` |
| field validation re-concatenated (`"$le$pe$mx"`) | `FAIL (a missing local epoch must read na, never ok)` |

The third is not synthetic: the concatenated form was what I wrote first, and the gate caught it on
its first run — `le="" pe=1000 mx=45` reads `"100045"`, all digits, so an **unsampled arm sailed
through as a valid cut**. Fields are validated one at a time now.

Test-forgery control: `presence-fuse.log` (1632543 B) and `presence-fusion.log` (202417 B) were
byte-identical before and after a full `--test`.

Live artifact (bare run, this node): `skew=na/na` — mesh-home has **no second BLE vantage
configured** (`MESH_FUSE_PEER` = sentinel `none`), so the pair renders `na` and the cycle stays the
INCOMPLETE path's business, exactly as designed. The skew path is therefore **unexercised live on
this node** and is proven only by the driven gates; it engages wherever a real BLE peer is
configured.

## Discarded, with the one line each

- **Relay-Based Synchronization in OppNets** (arXiv:2605.22491) — a relay carries state without being
  a replica; discarded because `mesh-chat-sync`'s `sort -u` union already relays transitively through
  any node pair that syncs, so the mechanism is present under another name.
- **Wait-free RDTs / Fair Reconciliation** (arXiv:2508.18193) — starvation under constant reordering;
  discarded because the board is a G-Set that never reorders, so no client's line can be deferred.
- **Asynchronous Checkpoint / MuFASA** (arXiv:2510.06404) — consistent snapshots over a weakly
  consistent log; discarded as already held by `mesh-chat-sync`'s causal-stability-frontier review
  plus `board_archive()`.
- **Semantic Conflict Model** (arXiv:2602.19231) — three-way rebase over a replicated journal;
  discarded because the board has no conflicts to rebase.

## Sources

- [Maxwait: A Generalized Mechanism for Distributed Time-Sensitive Systems (arXiv:2601.21146)](https://arxiv.org/abs/2601.21146)
- [Relay-Based Synchronization of Replicated Data Types in Opportunistic Networks (arXiv:2605.22491)](https://arxiv.org/abs/2605.22491)
- [Wait-free Replicated Data Types and Fair Reconciliation (arXiv:2508.18193)](https://arxiv.org/abs/2508.18193)
- [Asynchronous Checkpoint for Eventually Consistent Databases (arXiv:2510.06404)](https://arxiv.org/abs/2510.06404)
- [Semantic Conflict Model for Collaborative Data Structures (arXiv:2602.19231)](https://arxiv.org/abs/2602.19231)
- [arXiv API listing used for the sweep](https://export.arxiv.org/api/query?search_query=abs:%22CRDT%22+OR+abs:%22conflict-free+replicated%22+OR+abs:%22anti-entropy%22+OR+abs:%22eventual+consistency%22&sortBy=submittedDate&sortOrder=descending)
