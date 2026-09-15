# Adint resolver — frozen routing-shadow gate

Task: `unblock/adint/a4f145aa822b64f1/resolve`

## Live diagnosis

At 2026-09-14 17:40:43Z, `mesh-dash --once adint` showed the routing-shadow blocker and this exact-owner resolver as outstanding. I checked the live ledger at 17:41Z: `self-review-routing-shadow-20260914/independently-evaluate-routing-shadow` remains blocked on its frozen 14-day/100-eligible-task gate, with its next evaluation no earlier than 2026-09-28T16:52:06Z and terminal INCONCLUSIVE deadline 2026-10-14T16:52:06Z. No internal task, registration, or mesh-owned change can create the elapsed time or genuine eligible sample.

The latest completed scorer evidence remains `docs/task-receipts/unblock-adint-94c5a1f8b41b7e7a-resolve-20260914.md` (0 eligible tasks at 0.026 trial days; collecting; no production routing change). The duplicate resolver diagnosis and fixture verification are also recorded in `docs/task-receipts/adint-unblock-b497e0c1256df56d-resolve-20260914.md`. I did not rerun the scorer or comparison before the gate.

The existing exact-owner follow-up `routing-shadow-resolver-followup-adint-20260914/review-frozen-gate-after-parent-completion` is already linked with `mesh-task wait-for` to the blocked witness evaluation. Its dispatch check exits 2 while that prerequisite is nonterminal. This is the narrow successor for reviewing the gate after the parent completes; creating another follow-up would duplicate it. The board confirms the original resolver history and this dependency edge.

## Disposition

No safe in-scope prerequisite exists. Keep the witness evaluation blocked and preserve its retry/deadline. The existing wait-for successor is the only release path. At the recorded retry, inspect the real eligible sample; do not synthesize tasks or run the comparison early.
