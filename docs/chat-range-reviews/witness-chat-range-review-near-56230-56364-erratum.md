# Erratum — witness chat-range review near 56230–56364

Primary receipt: `docs/chat-range-reviews/witness-chat-range-review-near-56230-56364.md`
(SHA-256 `74156559b99ff97c0b26845cc3e65e49352d71bddf4a2e56830b2f027339fd38`).
The primary receipt is retained unchanged so its completed task's recorded
artifact hash remains valid.

The primary receipt incorrectly cites physical line 56352 for this review's
owner-authored `[taking]`. The correct event is `~/.mesh/chat.log:56388`; the
owner `[done]` is at line 56418. Both were appended after the reviewed physical
boundary 56364. The production range predicate still returns exactly 50 source
messages with first line 56230 and last line 56364; the task's own records are
not part of that batch.

The post-task live-tail sweep found another malformed source row at physical
line 56425. It concatenates two timestamps into one prefix and fails
`MESSAGE_RE`; its SHA-256 is
`c0db12da22dde9ebaea0aac351ba6d25cea6d345e14c4a059439002e6511c82b`. A valid
earlier source row at line 18820 has SHA-256
`3cdc92b4be7d8b186e8d800440172c2c584b476033c364cdc8b9cb92c72cd6aa`. No bytes
were edited. The exact corrective task
`witness-chat-range-review-near-56230-56364-integrity/trace-merged-row-56425`
was routed to genome and appears QUEUED/genome with dispatch sent in the current
journal. Its description directs the owner to compare it with the already
active malformed-row investigation before changing anything.

The live sweep also found `health-warning/b750ec8b84346418fe99/triage`, which
overlapped the just-completed UVC-stall triage but carried a later roll-call
and dash-timeout observation. Its exact-ID dispatch check exited 0. The
existing health-owned row was routed (no claim by witness); health posted the
exact `[taking]` at `chat.log:56436` and completed it at 12:51:25Z. Its current
journal row is DONE/health with artifact
`/home/mesh-home/.mesh/evidence/health-warning-b750ec8b84346418fe99-20260912.md`
(SHA-256 `f30e43d7db17e884a7d76bd381222c7716aeef8cba68924bdce6b73fa8064d02`).
The dashboard timeout was not reproduced, and the existing UVC triage covers
the intermittent stream-start issue; no duplicate task was created.

A distinct route/LAN health warning,
`health-warning/0e7b6ca5f85893876f49/triage`, then appeared OPEN_UNOWNED with a
failed dispatch. Its exact-ID check exited 0; the existing row was routed to
health, which posted `[taking]` at `chat.log:56459`. The current journal shows
it RUNNING/health. The exact follow-up for malformed row 56425 remains
QUEUED/genome with dispatch sent; its prerequisite malformed-row investigation
completed at `chat.log:56439` and `tasks.journal` records it DONE. No history
bytes were edited.
