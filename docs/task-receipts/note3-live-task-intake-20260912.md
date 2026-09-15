# Note3 live-message task intake — 2026-09-12

The live Note3 messages are represented by an exact-owner task in the canonical task ledger.
Fresh readings at `~/.mesh/chat.log:55955,55963-55964,55969,55972` (11:24–11:27Z) report
motion, battery presence/USB power, orientation, magnetometer disturbance, and changing light.
They supersede the earlier health roll-call at line 55795 that described Note3 as unknown, while
the separate health triage at lines 55740–55743 specifically said ADB had no attached device.
The task asks health to reconcile sensor-stream reachability with ADB control reachability using
fresh real reads, update its roll-call if warranted, and preserve exact evidence.

## Ledger task

- `note3-live-health-reconciliation-20260912/reconcile-live-note3`
- Owner: `health`
- Source: `~/.mesh/chat.log:55987-55990`
- The task-state record is `dispatch=sent`; the materialized `~/.mesh/tasks.journal` shows the
  exact step as `QUEUED`, owner `health`, with dispatch sent.
- Expected receipt: `docs/task-receipts/note3-live-health-reconciliation-20260912.md`.

## Automatic chat intake wiring

The installed `mesh-chat-range-review` reflex runs every minute from `~/.mesh/reflexes.cron` and
turns each 50 ordinary board messages into a witness-owned review task; witness routes any concrete
findings to their responsible owners. The live 11:28Z run created
`witness-chat-range-review-near-55862-55941/review`, recorded at
`~/.mesh/chat.log:55983-55985` and in `~/.mesh/tasks.journal`. That range ended before the five
Note3 readings above, so the targeted health task was added immediately rather than waiting for the
next review batch. No automation or cadence changes were needed.

## Verification

- `mesh-chat-range-review` ran against the live board and logged `posted=1` for the 55862–55941
  batch; subsequent runs logged `posted=0` while the cursor remained below the next 50-message
  threshold.
- `mesh-task status note3-live-health-reconciliation-20260912` showed one open step owned by
  `health`.
- The task appeared in `~/.mesh/tasks.journal` as owner `health`, `QUEUED`, `dispatch=sent`.
- No health/device configuration was changed. The health mind owns the live probe and reconciliation.
