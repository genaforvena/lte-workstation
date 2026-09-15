# Witness chat-range review: physical lines 60513–60870

- Reviewed: 2026-09-15T22:02Z
- Source: `~/.mesh/chat.log`, physical lines 60513–60870
- Count: exactly 250 accepted source messages. The 108 excluded rows were
  `[task-state]`/`[task-ledger]` structural rows; malformed rows: 0; prior
  `witness-chat-range-review-` rows: 0.
- Reviewer: witness

## Findings

1. **The UTF-8 truncation defect was fixed with red-then-green evidence.**
   Lines 60519–60523 and 60577–60579 identify multiple byte-wise cut sites,
   then report the character-boundary helper, multibyte fixture, and live
   symlink verification. Current `tasks.journal` records
   `chatlog-byte-truncation-20260913/fix-byte-based-truncation` DONE with
   `docs/chat-range-reviews/chatlog-byte-truncation-20260913.md`. No duplicate
   repair should be opened.

2. **Device churn attribution correctly retained an explicit residual unknown.**
   Lines 60525, 60543, 60548–60549, and 60617 report 991/2039 attributable
   uevents, Docker-veth correlation, and residual unattributed events rather
   than inventing process ownership. Current ledger evidence records
   `device-churn-attribution-20260913/correlate-high-uevent-bursts` DONE with
   its receipt. The residual is an evidence limitation, not permission for a
   substrate change.

3. **Health warning and delivery-expiry loops were settled as bounded history.**
   Lines 60552–60570, 60597–60610, 60627, 60639, and 60651 show autonomy and
   chat-delivery age-expiry warnings followed by health receipts that preserve
   the unknown failed hop and avoid resend storms. Current ledger rows for
   `health-warning/3558bdcb65a553510b2a/triage`,
   `health-warning/295f415cd853ddc2aff9/triage`,
   `health-warning/74ae9a268a1d7b8055b4/triage`, and
   `health-warning/4658087ce57cf7584fef/triage` are DONE. No fresh warning
   task should be duplicated from this historical range.

4. **The Tiny Fleet chain stopped before unsupported generation.** Lines
   60529–60535 and 60582–60593 record one passing preflight, five blocked
   suites, partial-freeze status, null corpora/adapters, and an open independent
   VPN gate. The current ledger has the preflight, registration, and independent
   verification receipts DONE; the evidence explicitly prevents treating an
   audit-only PASS as a gate-level PASS. Preserve that boundary and do not run a
   matrix from this window.

5. **Repeated mesh-land strand emission was a real duplicate-output defect, now
   covered by a later owner receipt.** Line 60822 identifies identical aged
   `land-strand` IDs re-emitted across refreshes because the deployed code read
   the posted-state marker after its own check. Current `tasks.journal` records
   `land-idempotent-output-20260915/dedupe-land-done-output` DONE with
   `docs/task-receipts/land-idempotent-output-20260915.md`; do not reopen the
   historical task.

6. **Artifact durability became an explicit follow-up rather than a silent
   claim.** Lines 60619 and 60839–60845 identify DONE rows pointing at vanished
   `/tmp` artifacts and the resulting focused rejection/repair task. Current
   ledger evidence records `task-artifact-durability-20260913/reject-ephemeral-
   done-artifacts` DONE with a durable receipt. This closes the observed defect;
   future completions should continue using repository or mesh receipt paths.

## Verification

- `mesh-dash --once witness` consumed the current state.
- `~/.mesh/chat.log`, `~/.mesh/tasks.journal`, and `mesh-task audit` were read
  during the live sweep; audit returned `chain_steps=1599 findings=93 status=FAIL`.
- `mesh-task queue --dispatch --owner witness` returned this exact row first.
- `mesh-task check dispatch witness-chat-range-review-medium-60513-60870/review witness`
  exited 0.
- Owner-authored `MESH_TASK_ACTOR=witness mesh-task take
  witness-chat-range-review-medium-60513-60870 review` returned `claimed`.
- Range audit returned `physical=358 source=250 malformed=0 structural=108 own=0`.
- Current ledger verification confirmed the cited DONE receipts before writing
  this review.
