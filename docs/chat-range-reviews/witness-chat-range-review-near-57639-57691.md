# Witness chat-range review: physical lines 57639–57691

- Reviewed: 2026-09-15T21:31Z
- Source: `~/.mesh/chat.log`, physical lines 57639–57691
- Count: exactly 50 accepted source messages. The 3 excluded rows were
  `[task-ledger]` structural rows; no malformed rows or prior
  `witness-chat-range-review-` rows occurred in this interval.
- Reviewer: witness

## Findings

1. **Direct→relay alerts repeated at one hourly cooldown.** Line 57668
   records the three alerts at 15:49, 16:49, and 17:49 after the earlier
   cooldown repair had completed. Witness routed the exact corrective task
   `mesh-path-watch-hourly-relay-repeat-20260912/diagnose-and-fix-hourly-repeat`
   rather than creating another copy. Current `tasks.journal` shows that
   task DONE with `docs/task-receipts/path-watch-hourly-relay-repeat-20260912.md`
   and the independent witness verification step DONE.

2. **The board contains substantial low-signal idle/handoff churn, but it is
   explicitly measured and not hiding an owner task.** Lines 57640–57660
   contain repeated idle/handoff notices; line 57659 reports approximately
   67 low-signal room/idle moves in the prior 800 board lines. The source
   evidence says the existing idle dedupe stands. No new task was opened
   because the current pane/ledger already distinguishes these posts from
   actionable work.

3. **Unreachable capability and operator-gated states remain honestly
   blocked.** Lines 57649–57654 record the adint resolver waiting for an
   operator revival decision and Termux SAF remaining unreachable; lines
   57681–57687 retain a stranded land test and an unwired land output warning.
   These are not presented as successful capability claims. Current ledger
   evidence contains the corresponding blocked/owner-routed work and the
   completed `land-idempotent-output-20260915/dedupe-land-done-output` fix;
   no duplicate task was created from this historical slice.

4. **Health evidence retained its uncertainty boundary.** Line 57683 says
   fleet probes were unreliable under high local load and reports cached
   doctor failures. The board records this as a limitation, not a substrate
   change or a clean-health claim; current health warning chains carry
   terminal receipts for the related historical alerts.

## Verification

- `mesh-task check dispatch witness-chat-range-review-near-57639-57691/review witness` exited 0.
- Owner-authored `MESH_TASK_ACTOR=witness mesh-task take witness-chat-range-review-near-57639-57691 review` exited 0.
- The production-shaped count returned `physical=53 source=50 malformed=0 structural=3 own=0`.
- `mesh-dash --once witness`, `~/.mesh/chat.log`, `~/.mesh/tasks.journal`,
  and `mesh-task audit` were read during the live sweep.
