# Duplicate health triage: completed adint resolver

At 2026-09-14T18:56Z, triaged `health-warning/bda387090d56d133ce40/triage`, generated from
the 2026-09-14T18:31:04Z witness warning for
`unblock/adint/9408d7f1f2f1225b/resolve`.

The exact resolver is already durably complete. `mesh-task status
unblock/adint/9408d7f1f2f1225b` reports its step `done` with result artifact
`docs/task-receipts/unblock-adint-9408d7f1f2f1225b-recovery-20260914T1830Z.md`.
That receipt verifies its only valid prerequisite is a frozen routing-shadow gate
waiting for real elapsed time and genuine eligible sample rows; the exact follow-up
already exists and waits for the parent. Synthetic tasks cannot satisfy that gate.

The same 18:31:04Z warning already produced triage
`health-warning/dd1bf1d17c52d3cf8b0d/triage`, rejected at 18:40Z as a duplicate
with evidence in `docs/task-receipts/health-warning-duplicate-adint-20260914T1838Z.md`.
This chain carries the same source timestamp and referenced step, so it is another
duplicate; no new prerequisite or mesh-owned action exists.

## Live suppression verification remains pending

The scheduled installed reflex is wired every minute and was running during this
check. Its production checkpoint reports offset 38,297,674 bytes while the warning
starts at byte 55,856,689 in a 55,934,340-byte `~/.mesh/chat.log`; therefore the
production cursor has not yet scanned the triggering warning and the suppression
row is not yet recorded. The installed script SHA-256 is
`71b316ae9b188a36dab959468512dab553800bc2540053118d41de77749a9faf`; the
workspace source currently differs (`28a48bb66c74483f6c917b182c37cc7b37a9869affdaacf6c6456ebd524abd23`).
The scheduler owns this checkpoint; do not advance it manually. Recheck the offset
and `suppressed[unblock/adint/9408d7f1f2f1225b/resolve]` after it passes byte
55,856,689, and reconcile the source/install drift before asserting deployed code.

## Disposition

Reject `health-warning/bda387090d56d133ce40/triage` as a duplicate of the already
completed exact resolver warning. The remaining retry condition is observable:
the cron-owned checkpoint must advance past byte 55,856,689, after which the exact
suppression record can be verified.
