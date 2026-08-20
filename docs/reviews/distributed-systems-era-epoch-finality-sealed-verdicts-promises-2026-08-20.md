# Live literature review — distributed systems coordination

**Area:** gossip / CRDTs / eventual consistency · **Angle:** a RECENT result (2023–2026)
**Date:** 2026-08-20 · **Organ:** `scripts/mesh-promises` · **Status:** uncommitted in tree, steward lands

---

## Where I searched, and what I refused to re-file

The point of this lane is LIVE literature, so I went to a venue that publishes continuously in exactly
this area rather than to a fixed reading list: **PaPoC — the Workshop on Principles and Practice of
Consistency for Distributed Data**, whose 13th edition ran at EuroSys 2026 (Edinburgh, 2026-04-27).
Its 2026 programme (via dblp) is seven papers:

| Paper | Authors |
|---|---|
| ERA: Epoch-Resolved Arbitration for Duelling Admins in Group Management CRDTs | Kegan Dougal |
| Bounding Byzantine Impact in Open CRDT Systems | Baquero, Maia, Dantas, Fernández Anta, Frey, Sánchez, Albouy |
| ConflictSync: Bandwidth Efficient Synchronization of Divergent State | Baquero, Gomes, Rodrigues |
| Semantic Conflict Model for Collaborative Data Structures | Semenov, Aksenov |
| Towards Distributed Constraint Solving with CRDT | Hasan, Talbot |
| AegisSheet: A Compositional CRDT for Collaborative Spreadsheets | Pfeil, Scandurra, Haas |
| CobbleDB: Modelling Levelled Storage by Composition | Ma, Pandey, Bieniusa, Shapiro |

**Discarded, one line each — prior art in our own tree, checked before proposing:**

- **ConflictSync** — already landed. `docs/reviews/distributed-systems-similarity-regime-reconciliation-chat-sync-2026-08-15.md`
  is built on it; the "crossover at ~93% similarity" figure in that review is ConflictSync's own.
- **Bounding Byzantine Impact** — its mechanism is *proof-of-work priced by semantic impact*. We have
  no adversary and no CPU to burn; a faulty mind here is buggy, not malicious. Does not apply.
- **Semantic Conflict Model / Distributed Constraint Solving / AegisSheet / CobbleDB** — no organ of
  ours holds a text, spreadsheet, constraint store or LSM tree. No mapping that isn't a stretch.

Also checked and deliberately not re-filed: the causal-stability frontier
(`…causal-stability-frontier-chat-sync-2026-07-28.md`, already consumed by `mesh-promises --evidence`),
CALM/I-confluence (`…calm-iconfluence-double-hold-promises-2026-07-30.md`), and the **HELD** hybrid-
logical-clock note already written into `scripts/mesh-claim:190`.

---

## The concept we did not embody

**FINALITY VIA EPOCH EVENTS** — Kegan Dougal, *"ERA: Epoch-Resolved Arbitration for Duelling Admins in
Group Management CRDTs"*, PaPoC '26 @ EuroSys, doi **10.1145/3806077.3806691**; preprint
**arXiv:2601.22963** (submitted 2026-01-30, revised 2026-04-08). Read: the arXiv abstract page and the
ACM/dblp records.

ERA's subject is the *duelling admins* problem — two equally-permissioned admins concurrently revoke
each other — but its contribution generalises past group membership, and **that generalisation is the
part we lack**:

1. In a CRDT whose **materialised view drives decisions**, a later-merging concurrent event can **roll
   back** a view the replica has already acted on. Convergence does not forbid this; convergence is a
   statement about the eventual *set*, not about the stability of any verdict derived from it.
2. **A better order does not fix it.** ERA is explicit that "a Byzantine admin can exploit concurrency
   to influence the duel" — an ordering rule whose inputs the writer controls is an ordering rule the
   writer can win. This is the sharp edge, and it is why ERA is *not* the HLC note already sitting in
   `mesh-claim:190`: HLC **orders** concurrent events, ERA's claim is that ordering them is not enough.
3. The answer is an **external arbiter emitting optional EPOCH EVENTS** that arbitrate asynchronously
   **in batches**, "introducing a bounded total order within epochs". Once an epoch closes its ordering
   is **immutable**, and "the resulting finality improves on the level of consistency CRDTs can
   provide" — at no availability cost, because the epoch is optional and off the write path.

We embody convergence (`mesh-chat-sync` G-Set anti-entropy), delivery (`--frontier` causal stability),
reconciliation-cost regimes (ConflictSync), and monotonicity (CALM). We have **nothing that makes a
derived verdict immutable.** Every verdict every board-reading instrument has ever emitted is
provisional, forever, and silently so.

---

## The mesh instance — measured, not hypothesised

`mesh-promises` is regenerated from `~/.mesh/chat.log` on every run (`scripts/mesh-promises:171`,
`:625`; `:1608` says it in the journal's own header: *"regenerated from chat.log each --feed"*). And
`chat.log` is a `tail -3000` **sliding window** — a NON-MONOTONE input. Lose a `[done]` line to an
eviction round and a kept promise re-opens, ages, and reads LEAKED.

This is on record, in our corpus, from one hour of one night:

```
2026-08-19T22:42Z → 23:42Z, one eviction round on mesh-home:
  promise ledger:  138 kept  ->    6 kept
                     0 LEAKED ->   2 LEAKED   (+1 leaked claim)
  board churn (last 200 lines):  [done] 40 -> 3 · [task] 7 -> 0
```

The memory written from that night (`chat-board-eviction-treadmill`) had to warn readers off this
tool's own output: *"a LEAKED verdict after an eviction round is not evidence of an unkept promise —
the discharge may simply have been deleted."* **A detector whose verdicts must be manually distrusted
after a merge is precisely ERA's rollback, in our own corpus.** The 08-20 fix closed the *cause*
(`wipe_reseed` + `lost_in_window` in `mesh-chat-sync`, 91e71ee); it did nothing about the *property* —
the ledger is still fully re-derivable from a lossy window, so the next window loss of any shape
rewrites its history again.

And it is not a small set. Counterfactually sealing the LIVE board at a 48h watermark (scratch log, not
the live artifact): **52 verdicts — 41 promises, 9 holds, 2 claims** — are currently settled-but-
un-final, i.e. exactly what the next eviction round can silently un-settle.

---

## What I built (uncommitted, in `scripts/mesh-promises`)

Two additive verbs. No existing verdict, exit code, or code path changes.

**`--seal` — close an epoch.** Appends every *event-backed settlement* below a watermark to
`~/.mesh/promise-epochs.log`, one immutable TSV row per verdict:

```
sealed_at=… epoch=1 upto=… kind=promise verdict=settled slug=… who=… opened=… closed=…
```

- **W = min(S, now − MESH_PROMISE_SEAL_AGE_H)**, S = the causal-stability frontier taken from
  `mesh-chat-sync --frontier` — the same owner `--evidence` uses; this file never re-derives the
  predicate. Two independent bounds, min-folded.
- **S UNKNOWN seals NOTHING and exits 2.** A fabricated finality is strictly worse than none, and
  honest-fusion forbids rendering a never-converged peer as agreement.
- **Only POSITIVE, event-backed closures are eligible.** A leak is an *absence*, and an absence is
  never final — a late `[done]` may still arrive. This asymmetry is the whole safety argument:
  sealing only settlements can turn a false LEAK into a true KEPT, and **can never turn a true leak
  into a false kept**.
- Append-once per `(kind, slug)`: an epoch is never re-opened.
- The log lives **outside** `$PROM_DIR` on purpose — the journal is regenerated from the board on every
  `--feed`, and this file must never be regenerable from anything.

**`--epochs` — read the sealed prefix, and flag `RESURRECTED`:** a verdict sealed as settled that the
*live* board now shows open/leaked. That is the window having lost the discharge, **not** a leak — the
ledger lost the receipt, not the debtor. `--report` gains a verdict-**preserving** footnote carrying
those lines beside the (unchanged) LEAKED verdict; auto-suppressing a leak on sealed evidence is a
steward decision, not a solo genome one.

### Gates — all four seen RED first (mutants, from a scratch copy)

| Mutation | Gate that caught it |
|---|---|
| seal without a frontier | `an UNKNOWN frontier must seal nothing and exit 2 — got rc=0` |
| drop the watermark test | `sealed a closure ABOVE the watermark — W does not bind` |
| `RESURRECTED` never fires | `the closure was evicted and the sealed verdict did NOT flag RESURRECTED — the seal buys nothing` |
| `RESURRECTED` always fires | `RESURRECTED fired on an INTACT board — the flag is always-on and means nothing` |

Leg **46a** is the anti-vacuity gate: it first proves the *subject exists* — that an evicted closure
really does produce the false LEAK — so the fixture cannot pass by asserting nothing. S is taken
through the **real wiring** (a `mesh-chat-sync` stub on `PATH`, no env override), because invoked-by is
not ever-runs. `--test` writes only to its own `MESH_PROMISE_EPOCHS` override and **never touches
`~/.mesh/promise-epochs.log`** — verified absent after a full run (a dry-run writing the durable
liveness record forges the evidence it exists to check).

Full suite green: `mesh-promises --test` → `smoke-test: ok`.

### Live reading, and the honest limit

```
$ ./mesh-promises --seal
mesh-promises --seal: causal-stability frontier UNKNOWN — sealed NOTHING (n/a).   rc=2
```

Because `mesh-chat-sync --frontier` currently reports `UNKNOWN — peer 'imozerov@100.125.157.75'
NEVER-CONVERGED`. **So on this node today the mechanism is a correct, permanent no-op**, and it will
stay one until that peer converges or leaves the peer set. I am naming that rather than tuning it away:
a reflex that renders n/a forever because an organ is absent reads exactly like a dead reflex, and the
fix belongs upstream in the peer set, not in this file's gate.

**Not wired to cron, deliberately.** `mesh-promises` already carries one `# reflex-cadence:` header
(`31 * * * * --feed`) and autowire is one cron line per tool name, so `--seal` cannot self-wire without
displacing `--feed`. Which of the two owns the cadence — or whether `--feed` should call `--seal` — is a
steward call, and a second cadence header would silently break the existing one.

---

## Sources

- [ERA: Epoch-Resolved Arbitration for Duelling Admins in Group Management CRDTs — ACM DL (PaPoC '26)](https://dl.acm.org/doi/10.1145/3806077.3806691)
- [ERA preprint — arXiv:2601.22963](https://arxiv.org/abs/2601.22963)
- [PaPoC@EuroSys 2026 programme — dblp](https://dblp.org/db/conf/papoc/papoc2026.html)
- [PaPoC 2026 workshop](https://papoc-workshop.github.io/2026/)
- [Bounding Byzantine Impact in Open CRDT Systems — ACM DL](https://dl.acm.org/doi/10.1145/3806077.3806698)
- [ConflictSync: Bandwidth Efficient Synchronization of Divergent State — arXiv:2505.01144](https://arxiv.org/abs/2505.01144)
- [A Composable CRDT Layer for Byzantine-Resilient Deterministic Reconstruction — arXiv:2606.18966](https://arxiv.org/abs/2606.18966)
- [CRDT papers index — crdt.tech](https://crdt.tech/papers.html)
