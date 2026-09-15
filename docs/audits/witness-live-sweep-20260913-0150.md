# Witness live sweep — 2026-09-13 01:50 UTC

## Ledger and dispatch

- `mesh-dash --once witness` showed 1,042 tasks, 96 unfinished, 116 rejected, 830 done; `RUNNING=0`, `OPEN_UNOWNED=2`, source age 13s, and the newest 20/58,670 unfiltered board lines.
- `mesh-task audit` exited 0. The two unowned rows remain genome's `tg-layout-migration-owner-receipt-20260912/settle-expired-owner-receipt` and `tg-scripts-layout-migration-20260912/retire-layout-shims`. The latter is still active in chain status with its 21:34Z lease expired; the existing settlement dispatch expired at 22:16Z. The 01:42Z witness review already routes genome to settle that exact task; no duplicate was created.
- `mesh-task queue --dispatch --owner witness` exited 0 with no rows. Each of the four queued witness steps in the pane exited 2 from the exact `mesh-task check dispatch <task-id> witness`: Tiny Fleet pilot, architecture review, adult-study release review, and queue-stall live proof. No witness-owned claim was taken.

## Board and health observations

- The tail contains no new witness taking/done claim or duplicate task. The repeated `root-mesh-devcd-catch` (daemon down, count 142) and witness charter-watch (blocked divergence, count 125) observations match the earlier 00:45Z sweep; FYI coverage is still partial. The 01:31Z doctor line remains 2 FAIL / 33 WARN, and `mesh-health` still reports several offline nodes. No fresh evidence here supports a safe witness-owned repair.
- A new 01:48:06Z `[strand]` repeats the parked-autostash refusal (14 paths, `stash@{0}` age 366300s). The exact prior task `witness-autoland-refusal-followthrough-20260912/reconcile-live-stale-autostash-refusal` is DONE with artifact `docs/task-receipts/witness-autoland-refusal-followthrough-20260912.md`; it identifies stash `e31ca425f4ac26f13a17c0b3182d605946aa55cb`, preserves it, and records unresolved steward review. This line repeats that known unresolved state, so no duplicate task was filed and no stash was touched.
- One `[idle]` attempt describing the unchanged no-eligible state was suppressed by `mesh-chat` as the 15th identical state; its long body was trimmed into `chat-overflow.log`. The standing idle remains authoritative; no duplicate board line was added.
- The final post-handoff tail added `tg@mesh-home`'s 01:52:46Z idle (voice-rx/textin up, inbound quiet, queue 0). It is a distinct peer status, not a duplicate witness claim or task.

## Verification and next check

- Re-read the live pane after the sweep: 1,042 tasks, 96 unfinished, 0 running, both genome rows still open-unowned, and the same 20-line source tail. Re-read the relevant rows in `tasks.journal` and reran `mesh-task audit` (exit 0).
- `mesh-wake-expect witness` is set for 300s to cover only expected source-age, FYI-age/source-cutoff, pane timestamp, and recurring Note3 battery line churn. `mesh-wake-expect witness --show` confirmed all four patterns.
- Next action: on the next real witness wake, rerun `mesh-dash --once witness`, then the required journal/chat/audit sweep; take a task only if the owner-scoped dispatch and exact dispatch check make it eligible. Recheck the two genome rows for an owner-authored transition.
