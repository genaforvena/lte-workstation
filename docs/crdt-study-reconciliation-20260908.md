# CRDT study reconciliation — 2026-09-08

## Decision

Defer `study-crdt-conflict-free-merge-20260908/reconcile-crdt-study` as a
future security lane. Do not add Blocklace, Opbox-style disk synchronization, a
second board log, or another merge substrate. The existing append-only G-Set
board remains the synchronization substrate.

## Live-task and review audit

The task was live at 2026-09-08T16:30Z: `mesh-task` replay showed the chain and
step `open`, owner `discover`, with the stated admission predicate and design
artifact. The instruction was correct against the current code. The existing
review, `docs/reviews/distributed-systems-blocklace-equivocation-board-20260908.md`,
already records that Blocklace addresses equivocation, while this board's live
weakness is delivery omission/windowing; replacing the G-Set would regress the
append-only board semantics and expand the trust/key-management surface.

## Consumer price

The named consumer is `mesh-promises`; its admission predicate is owned by
`mesh-chat-sync --frontier` and classifies the board before leak resolution.
The real current read was:

```text
DARK|board=8ffa266d372f src=chat.log admitted=1/4 partial-board: ilya@100.107.198.111(1894831s) imozerov@100.125.157.75(never-converged) imozerov@100.73.170.56(1024350s)
```

This is an honest non-admission, not evidence that Blocklace is needed: the
current board has one admitted peer out of four, one never-converged peer, and
two stale peers. Independent live pricing reported `--lag` worst peer lag
1,894,818 seconds and `--similarity` J=0.0% for the measured divergent peer,
with 5,517 needed lines in the last round. `--frontier` returned UNKNOWN because
of the never-converged peer. `mesh-promises --check` still passed parity and
replay agreement (80/80 promises, 136/136 claims, 60/60 holds, 48/48 asks), so
the consumer's ledger is internally consistent while its board admission is
not globally final.

The consumer is therefore bounded and wired for admission, but the proposed
CRDT change has no current bounded security consumer: no untrusted writer,
delegated writer, or equivocation evidence exists in the reviewed board path.
The material does not clear the study's requirement for a named current
consumer plus a new nonempty convergence artifact that justifies an
implementation task.

## Verification artifacts

- `scripts/mesh-chat-sync --test` — PASS (`smoke-test: ok`).
- `scripts/mesh-promises --check` — PASS for parity and replay agreement.
- `mesh-promises --admission` — real live result `DARK`, `admitted=1/4`.
- `scripts/mesh-chat-sync --lag` — real live result, rc 1 because peers are stale/never-converged.
- `scripts/mesh-chat-sync --similarity` — real live result, worst measured J=0.0%, LOW regime.
- `scripts/mesh-chat-sync --frontier` — real live result, UNKNOWN due to a never-converged peer.

Reopen only if the trust boundary changes or live evidence of equivocation
appears. At that point the smallest bounded steward task is to specify and
measure a quarantine-only signed provenance envelope around board events; it
must not alter the existing board log without a separate steward decision.
