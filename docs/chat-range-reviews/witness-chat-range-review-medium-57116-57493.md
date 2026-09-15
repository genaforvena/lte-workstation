# Witness medium chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 57116–57493 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 250 source
messages (first source line 57116, last 57493). Structural task-ledger/task-state
rows, malformed rows, and this reflex's own `witness-chat-range-review-` rows
were excluded.

## Findings and disposition

1. The dominant repeated coordination signal is the same live network finding:
   health reports at lines 57137, 57153, 57172, 57204, 57290, and 57315 retain
   egress through `tailscale0`/table 52 and an exit-node SPOF; line 57290 also
   records the requested `100.74/16` prefix versus the live `100.76/16` LAN
   mismatch. The exact health-warning triages in this interval are all
   `DONE/health` with receipts in the current replay, so no duplicate health
   tasks were created.

2. This is not fully resolved: current replay shows
   `exit-node-lan-cgnat-repair-20260912/prove-and-restore-live-route` as
   `REJECTED/vpn`, while its exact successors
   `repair-cgnat-lan-healer` (genome), `deploy-and-verify-healer` (vpn), and
   `independent-route-verification` (health) remain `OPEN`. The board's line
   57367 says the same step was rejected for the live-prefix mismatch. Existing
   successors are the correct owner-routed follow-up; this review did not create
   another repair or warning task.

3. The repository migration and sync activity is durably reconciled in the
   current journal: `operations-wrapper-pilot`, `communication-family-slices`,
   `repair-tracked-tool-link-parity`, `classify-untracked-gpu-fan`, and
   `reconcile-prism-divergence` are `DONE` with artifacts. The repeated
   autoland posts in lines 57124–57372 correspond to completed exact ledger
   steps or existing genome landing work; no duplicate closure was opened.

## Verification

- `mesh-dash --once witness` returned the live unfiltered pane.
- Read the live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `mesh-task audit` completed.
- `mesh-task check dispatch witness-chat-range-review-medium-57116-57493 witness`
  passed; owner-authored `MESH_TASK_ACTOR=witness mesh-task take ... review`
  claimed the exact step.
- Predicate recomputation returned `COUNT 250 FIRST 57116 LAST 57493`.
- `mesh-task replay --json` confirmed the statuses and artifacts cited above;
  the three open repair successors are exact existing tasks, not duplicates.

## Disposition

Receipt complete. Preserve the existing repair successors and require the live
prefix to be established before independent route verification can close.
