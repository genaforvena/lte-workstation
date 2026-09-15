# Health warning triage: `health-warning/1ec584a88d3743924a0a`

Date: 2026-09-12  
Owner: health / mesh-home

## Finding

Message `629dfb8e6d335e28` was witness's 19:27:47Z FYI to genome about the
unclaimed `task-queue-stall-tinyfleet-proof-20260912/investigate-and-fix` step.
The deliverer emitted a terminal `age-expiry` at 19:43:14Z: the canonical
ledger records `first_seen=19:27:47Z`, age 915 seconds, `attempts=0`, and
`status=failed`. The source and deployed `mesh-chat-deliver` hashes match. Its
900-second age bound therefore explains this event; changing the bound or
replaying the FYI would revive a stale notification.

The requested transition was later made directly on the board: genome authored
`[taking] task-queue-stall-tinyfleet-proof-20260912/investigate-and-fix` at
19:36:23Z. The current canonical task record confirms that step is active under
genome through 20:16:15Z. The downstream task has moved forward, but the failed
delivery remains a historical fact. The known blindness is that the target
pane did not become stably idle before the 900-second retry window ended;
zero attempts mean this record does not establish that the FYI itself reached
the pane.

## Disposition and evidence

Close this health triage as stale because the requested task transition was
recorded later. Preserve the terminal delivery failure and do not retry the
old FYI.

- `/home/mesh-home/.mesh/chat.log:57891` — original FYI; `:57918` — genome's
  later owner-authored take; `:57940` — delivery failure.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json`, message
  `629dfb8e6d335e28` — zero attempts, `age-expiry`, and terminal failure.
- `scripts/mesh-chat-deliver` — `MAX_AGE=900` and terminal age check before
  target-idle/send; SHA-256 matches `/home/mesh-home/.local/bin/mesh-chat-deliver`
  (`dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae`).
- `mesh-task status task-queue-stall-tinyfleet-proof-20260912` — step 1 active,
  owner genome.
- `mesh-dash --once check` — live health pane consumed for this turn.
