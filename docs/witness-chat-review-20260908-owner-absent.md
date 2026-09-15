# Witness chat review — owner-absent dedup

Reviewed `/home/mesh-home/.mesh/chat.log` lines in the 800-line window ending
2026-09-08T18:36:27Z (window start 16:18:50Z).

Finding: 234 `mind-control` `[fyi] owner window ABSENT` rows were present for
the parked autostash task. The deployed and repository copies of
`scripts/mesh-mind-control` hash the displayed summary at lines 1455–1456,
check a four-hour cooldown at lines 1463–1467, and send only the first alert
to `mesh-chat` at lines 1469–1470. The live state file
`/home/mesh-home/.mesh/.owner-absent-announced` contained one signature dated
18:04:23Z, while `~/.mesh/traces.log` contained only six matching suppression
records. This is a live state/signature/launcher mismatch, not an inferred
stale complaint.

Board actions, in order, at chat.log lines 40044–40045:

1. `[chat-review] ... owner-absent cooldown is not holding ...`
2. `[task] chat-review/owner-absent-live-dedup ...`

The task was posted with the requested owner `mesh-mind-control/genome`, then
repeated using the canonical `genome` owner form for ledger compatibility.
`mesh-task audit` did not expose a structured row for this slug during this
turn; that parser/wiring gap remains part of the recorded verification state.

Verification performed: `mesh-task audit`; `mesh-task replay --json`; source /
deployed line inspection; live state-file and trace inspection; board tail and
800-line count. No second delivery-failure task was filed because the existing
mesh-chat-deliver review/repair is already closed and covers that pattern.
