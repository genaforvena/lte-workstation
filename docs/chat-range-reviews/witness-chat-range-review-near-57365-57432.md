# Witness near chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 57365–57432 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 50 source
messages (first source line 57365, last 57432). Structural task-ledger rows,
malformed rows, and this reflex's own `witness-chat-range-review-` records were
excluded.

## Findings and disposition

1. A stale-warning path briefly violated the preferred pre-take check. At
   line 57395, health took `health-warning/94dea43506e23e22403a/triage` even
   though its source text already contained terminal evidence for
   `health-warning/4b0b9baf154ad5055cba/triage`; line 57397 then correctly
   classified the work as stale and already resolved, citing the existing
   receipt. Replay confirms the warning chain is complete. No new retry or
   duplicate task is warranted; future dispatch should reject this fingerprint
   before taking it.

2. `mesh-land` reports `mesh-tg-filter` landed at both lines 57414 and 57416.
   The surrounding migration step has a completed receipt and the exact
   communication-family autoland is recorded done at lines 57421–57422; replay
   shows `tg-scripts-layout-migration-20260912` blocked only at its later chain
   state, with the communication step done. Treat the repeated land line as
   duplicate output to monitor, not as permission to re-land or create a new
   migration task.

3. The route rejection is handled with the correct owner and evidence. Lines
   57374 and 57375 record the structured VPN rejection and no route mutation;
   lines 57377–57379 close the unrelated health warning with an explicit
   tailscale0/exit-node finding and retained LAN UNKNOWN gap. Existing receipts
   and successors provide the required verification, so this review makes no
   substrate change.

## Verification

- `mesh-dash --once witness` returned the live unfiltered pane.
- Read live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `mesh-task audit` ran before work.
- `mesh-task queue --dispatch --owner witness` returned the assigned row.
- `mesh-task check dispatch witness-chat-range-review-near-57365-57432/review witness`
  passed with exit 0; owner-authored `mesh-task take` returned exit 0.
- Predicate recomputation returned `COUNT 50 FIRST 57365 LAST 57432`.
- `mesh-task replay --json` confirmed the cited health and migration chains'
  terminal statuses and this review chain's active ownership.

## Disposition

Receipt complete. Preserve the existing stale-warning receipt, migration
receipt, and route successors; do not duplicate resolved triage or re-land
`mesh-tg-filter` from this review.
