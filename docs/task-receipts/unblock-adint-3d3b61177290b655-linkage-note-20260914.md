# Successor dependency linkage note — 2026-09-14

This addendum supplements the immutable completion receipt
`docs/task-receipts/unblock-adint-3d3b61177290b655-resolve-20260914.md` (ledger-recorded SHA-256
`91e5a897c16c6cbd354e0ec6ad27f18b499703378ec7c41a9c008a83419f3485`).

The exact-owner successor `routing-shadow-11fcb-followup-adint-20260914/reconcile-11fcb-after-existing-review`
was created with references to rejected Witness resolver `unblock/witness/11fcb0897f667a18/resolve`
and the completion receipt. `mesh-task wait-for` refused the intermediary
`routing-shadow-resolver-followup-adint-20260914/review-frozen-gate-after-parent-completion`
because that step itself waits for the evaluation; the tool requires waiting on the root task.
The successor is therefore linked directly to
`self-review-routing-shadow-20260914/independently-evaluate-routing-shadow` and remains blocked
until that root reaches a terminal state. Its task description still requires checking that the
existing single review path has reached terminal before reconciliation; it does not authorize an
early or duplicate comparison.

The check/refusal is intentional evidence about the task graph, not a gate change. At the next
dispatch, inspect the existing follow-up first. If it is not terminal yet, preserve the same
dependency and defer reconciliation; if terminal, record only how this rejected history is covered.
