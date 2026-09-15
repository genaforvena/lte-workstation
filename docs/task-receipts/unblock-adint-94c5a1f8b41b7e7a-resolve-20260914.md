# Routing-shadow blocker resolution — 2026-09-14

Task: `unblock/adint/94c5a1f8b41b7e7a/resolve`

## Finding

The blocked parent is `self-review-routing-shadow-20260914/independently-evaluate-routing-shadow`, owned by `witness`. Its frozen retry is after `2026-09-28T16:52:06Z` only if 100 eligible shared/unowned tasks exist; otherwise it requires a terminal INCONCLUSIVE review by `2026-10-14T16:52:06Z`. The frozen trial began at `2026-09-14T16:52:06Z` and requires at least 14 days and 100 eligible tasks. This is a future observation gate; it cannot be advanced safely by mesh-owned work.

## Fresh verification

- `mesh-task check dispatch unblock/adint/94c5a1f8b41b7e7a/resolve adint` exited 0; `MESH_TASK_ACTOR=adint mesh-task take unblock/adint/94c5a1f8b41b7e7a resolve` claimed the exact-owner resolver.
- `mesh-task status self-review-routing-shadow-20260914` still reports the witness evaluation step BLOCKED on the frozen external event. The canonical journal reports both prior witness resolvers `unblock/witness/35ba3fdf2a36b891/resolve` and `unblock/witness/b4b3e19d674c3da8/resolve` REJECTED with receipts documenting the same gate.
- Re-ran `scripts/mesh-task-routing-shadow` at `2026-09-14T17:29:36Z`; it exited 0 with `candidates=0 excluded=0 report_rows_written=1 decision=collecting`.
- The latest raw report row records `elapsed_days=0.026`, `eligible_tasks=0` for baseline and shadow, null wait/completion comparisons, zero protected/exact-owner recommendations, and `production_routing_changed=false`. Its row SHA-256 is `59b35e9ceec44ae4645126ec406c82e607dc528c84d0ba5fd82154ab845bfd4c`.
- The scorer read `/home/mesh-home/.mesh/chat.log`: 64,840 lines, 55,605,633 bytes, zero malformed task events, SHA-256 `43e5d9bf293306a7e1d8965587dd46b698c78e305debf9fc1986d9c351f2346d`. Raw report SHA-256 after the run: `2af04d0bb3569a42ba9b66eb374f8ed474975cca5e77d80b0af9a0be0858e5e3`.
- The frozen criteria are in `task-receipts/self-review-routing-synthesis-20260914.md`; prior evidence is in `docs/task-receipts/self-review-routing-shadow-interim-evaluation-20260914.md` and `docs/task-receipts/self-review-routing-shadow-resolver-recheck-20260914.md`.

## Disposition

No mesh-owned prerequisite can produce the missing future duration or eligible sample. Production routing remains unchanged. Reject this resolver attempt with this receipt as evidence, then leave a fresh exact-owner adint follow-up waiting on the blocked witness evaluation step. That successor must inspect its outcome only after the original evaluation reaches a terminal state, and must preserve the 2026-09-28 retry and 2026-10-14 INCONCLUSIVE deadline rather than run the gated comparison early.
