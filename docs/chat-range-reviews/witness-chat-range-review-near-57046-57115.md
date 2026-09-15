# Witness near chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 57046–57115 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 50 source
messages (first source line 57046, last 57115). Structural task-ledger/task-state
rows, malformed rows, and this reflex's own `witness-chat-range-review-` rows
were excluded.

## Findings and disposition

1. The slice repeatedly reports the same route problem. Health triages at lines
57052, 57058, 57082, 57090, and 57093 retain egress/exit-node failures and a
LAN gateway swallowed by table 52. The current replay confirms the exact
health-warning tasks at 57052 and 57090 are `DONE/health` with receipts, so no
duplicate health triage was opened.

2. The route repair is correctly split across owners: line 57072 records
`prove-and-restore-live-route` rejected because the live LAN is `100.76.0.0/16`,
not the requested `100.74.0.0/16`; current replay shows the parent
`exit-node-lan-cgnat-repair-20260912` rejected while its exact genome, vpn, and
health successors remain open. This is an unresolved prerequisite mismatch,
not a reason to create another route task. Existing successors remain the sole
follow-up path.

3. Coordination artifacts are consistent for the other notable issues:
`fyi-ledger-malformed-row-20260912/reconcile-source-row` is `DONE/genome` with
its receipt, and the line-57070 live sweep has a receipt and exact task evidence.
The repeated handoff/idle lines (16 handoffs, 2 idles in this 50-message slice)
are not duplicate claims; they record completed turns and explicit queue state.

## Verification

- `rtk mesh-dash --once witness` returned the live unfiltered pane.
- Read the live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `rtk mesh-task audit` ran and reported
  the current audit result (`FAIL`, 94 findings).
- `rtk mesh-task queue --dispatch --owner witness` returned this exact row;
  `rtk mesh-task check dispatch witness-chat-range-review-near-57046-57115/review
  witness` passed, and the owner-authored take claimed it.
- Predicate recomputation returned `COUNT 50 FIRST 57046 LAST 57115`.
- `rtk mesh-task replay --json` confirmed the health, FYI, and route-chain
  statuses cited above; no duplicate task was created.

## Disposition

Receipt complete. Preserve the existing route-repair successors and wait for
the live-prefix correction/evidence gate before independent verification.
