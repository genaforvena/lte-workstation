# Job Telegram delivery and follow-through diagnosis — 2026-09-16

## Result

Correction: the 15-vacancy package was sent by the Telegram userbot at 2026-09-15
23:16–23:28 UTC, but those messages were addressed to `me` (Saved Messages), not the
operator's Telegram chat. The earlier job-window turn had no delivery receipt yet and
accurately reported that the TG window was occupied. A correct operator-chat delivery was
performed at 2026-09-16 00:11:13 UTC through `/home/mesh-home/.local/bin/mesh-tg`, uploading
`/home/mesh-home/.mesh/job/shortlist-15-ownership-20260915.md` to chat `51010427`; the
wrapper returned `sent to operator TG` after Telegram's `ok:true` response.

The underlying request still had a follow-through defect: no durable `mesh-task` chain was
created for the 15-vacancy send. The only durable work product before delivery was the
private shortlist file and the conversational result in the Codex lifecycle record
`~/.mesh/codex-lifecycle/job/512a1308d7b3b236bfb94dad9e7537b9ce25b44e7ccdb121496d084ebb1a8457.md`.
The corresponding task-context and `mesh-task audit` contain no `shortlist-15` or
`direct-outreach` task. Therefore “it is queued” was not an authoritative queue state:
there was no owner, lease, retry edge, or terminal delivery receipt to wake or reassign.

## Why requests often appear not done

1. **Conversation-level handoff instead of durable task state.** The request was left in a
   pane handoff while another TG operation was busy. A handoff records context but does not
   itself schedule work. This is the primary cause for this incident.
2. **The shared HH browser is a serialized bottleneck.** The live `.mesh/job/.apply.lock`
   is currently held by `mesh-job-apply --reconcile --dry` (PID 1551889), while the browser
   driver PID 687073 has been alive since 22:17 UTC. Recent `job-chatwatch` receipt
   `docs/task-receipts/job-chatwatch-20260915.md` records a fresh-read failure after the
   explicit 150-second bound; older logs repeatedly record the same writer-lock contention,
   navigation failure, and logged-out states. A watcher cannot complete while the writer
   monopolizes the organ.
3. **Telegram delivery has had real, distinct transport failures.** `~/.mesh/job-answers.log`
   records `FileNotFoundError: mesh-tg` under the cron environment, and
   `~/.mesh/job-act.cron.log` / `~/.mesh/job-cal.log` record `send FAILED` network failures.
   `~/.mesh/job-scan-getmatch.log` records userbot failures with `Network is unreachable`
   and connection failure to Telegram. These are not evidence that the 15-package send failed,
   but they explain why an unreceipted “send later” is unsafe.

## Verification performed

- `mesh-task audit`: all 27 current `job` rows are terminal `DONE`; none names the 15-vacancy
  request.
- `mesh-task queue --dispatch`: no current job row for the request.
- `~/.mesh/tg-userbot-sent.log` plus `mesh-tg-user dump`: complete 15-row text/file delivery
  is present in Saved Messages (`me`), not the operator chat.
- `~/.mesh/tg-sent.log`: corrected operator-chat file delivery at 00:11:13Z.
- `docs/task-receipts/job-chatwatch-20260915.md`: browser read failure is explicitly recorded,
  not silently treated as zero new work.
- Live process/lock inspection: PID 1551889 owns `.mesh/job/.apply.lock`; PID 687073 is the
  long-lived HH driver.

## Open corrective obligation

Future operator-facing multi-step requests need a durable task chain before the first
side-effect, with an explicit delivery artifact that joins the request ID to the Telegram
message/file ID. A TG send receipt alone must not be used as proof that the underlying job
work was completed.
