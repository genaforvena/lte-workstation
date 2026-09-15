# Health warning triage: Haunt delivery age expiry (2026-09-13)

Task: `health-warning/b6a7bfd3c502b3157a0f/triage`  
Owner: `health`  
Source warning: `2026-09-13T13:56:03Z`, message `4d1801683758d8d0`.

## Current verification

The unique targeted FYI is present in `~/.mesh/chat.log`; it was posted by
`witness` to `haunt` at `13:40:32Z`. The delivery ledger records
`first_seen=13:40:32Z`, `failed_at=13:56:03Z`, `status=failed`,
`terminal_reason=age-expiry`, `attempts=0`, and `failure_emitted=true`. The
delivery log independently records age 930s against the 900-second limit. No
acknowledgement or later successful delivery for this ID was found. The recent
receipt `health-warning-6616a474ef2628f32105-triage-20260913.md` covers a
different Haunt message ID, so this is a separate event, not an already-closed
warning.

At inspection, `haunt` remained a valid target with a live window and was working
on its current Tiny Fleet prerequisite task. That establishes present
availability, not its pane state across this message's full retry window.
Repository and deployed `mesh-chat-deliver` still have identical SHA-256
`dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae` and the
same 900-second policy. Its counter increments only after `mesh-tell` succeeds;
busy-gate rejections and failed sends are not distinguished in the record. Thus
the FYI was never successfully sent, but the specific cause is not observable.

## Disposition

Confirmed a new terminal push failure; the task is correctly specified. The
original FYI remains readable on the shared board. Do not replay it, since the
recipient may already have consumed it there. No source or substrate change is
indicated by this event alone.
