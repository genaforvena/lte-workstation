# Health warning triage: `health-warning/e91fff3ebe82d19c4cbc`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/e91fff3ebe82d19c4cbc/triage`

## Finding

The delivery failure at `2026-09-09T02:58:07Z` was a false failure. The targeted
message `dfb3bde5b3594666` was delivered to genome three times, and genome
posted an acknowledgement after every send. All acknowledgements used the
canonical board form `[ack] ack:msg:dfb3bde5b3594666`. The worker's ACK parser
accepted `[ack] ack:<id>` but rejected the extra `msg:` segment, so the ledger
never recognized any of the three receipts and reached the attempt limit.

Evidence in `~/.mesh/chat-deliver.log`:

- 02:49:33Z: attempt 1; board ACK at 02:49:46Z.
- 02:51:05Z: attempt 2; board ACK at 02:51:16Z.
- 02:56:06Z: attempt 3; board ACK at 02:56:15Z.
- 02:58:07Z: terminal `attempt-limit` failure emitted with attempts=3.

The corresponding ACK lines are in `~/.mesh/chat.log`. The affected source
message was witness's task dispatch at 02:49:29Z; these receipts confirm pane
delivery and acknowledgement, so this incident is not evidence of a genome
pane or mesh-tell outage.

## Repair and verification

`scripts/mesh-chat-deliver` now accepts both `ack:<id>` and `ack:msg:<id>`,
including whitespace after the colon. The shell regression now exercises the
observed `ack: msg:<id>` spelling; the worker self-test covers both forms.
The historical failed ledger row was left untouched.

- `bash tests/test-mesh-chat-deliver.sh` — PASS, including the new ACK spelling.
- `python3 tests/test-mesh-chat-deliver-attempts.py` — PASS.
- `python3 scripts/mesh-chat-deliver --test` — PASS.
- `python3 -m py_compile scripts/mesh-chat-deliver` — PASS.
- `/home/mesh-home/.local/bin/mesh-chat-deliver` resolves to the edited source
  symlink; source and deployed SHA-256 match.
- Live crontab retains the one-minute `mesh-chat-deliver` cadence.

No further action is needed for this historical warning. A separate current
delivery outage was not indicated by this evidence.
