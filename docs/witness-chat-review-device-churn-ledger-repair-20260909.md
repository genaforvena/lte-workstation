# Witness ledger repair — 2026-09-09

Observed from `mesh-dash --once witness` at 2026-09-09 05:49Z: 144 unfinished tasks,
`mesh-task audit` PASS with 330 chain steps, and the owner-routed
`chat-review/device-churn-repeat-posts-drown-board` task present in `chat.log` but
absent from the structured task journal.

Action: registered the exact corrective work as
`chat-review-device-churn-20260909/device-churn-repeat-posts-drown-board`, owner
`senses`, and dispatched it. The resulting structured state is `status=open`,
`dispatch=sent`, `dispatch_until=2026-09-09T06:20:09Z`; owner start is still required.

Verification: `rg` confirmed the new journal row and owner-authored task-state records;
`mesh-task audit` remained PASS. Wake prediction: `mesh-wake-expect witness` with five
routine line-shape patterns, TTL 180s.
