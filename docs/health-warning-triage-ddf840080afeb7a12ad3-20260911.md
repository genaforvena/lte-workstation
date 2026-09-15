# Health-warning triage: ddf840080afeb7a12ad3

Date: 2026-09-11

## Verdict

This is a recovered, bounded historical delivery miss. No code or substrate mutation is
warranted. The warning is not stale as a board item: the exact task was open and was claimed
at 2026-09-11T20:18:32Z.

## Evidence

The failed record is present in the live delivery ledger:

```text
message=e3e244e8d0c96661
first_seen=2026-09-11T17:58:31Z
sender=witness target=haunt attempts=0
status=failed terminal_reason=age-expiry
failed_at=2026-09-11T18:14:09Z failure_window=5963834
```

The original board record was an FYI about D02/C05, not a control or acknowledgement. The
delivery log records the matching terminal edge at age 931 seconds. The current deployed
registry still contains `haunt`, and later records delivered to that target at 18:16:41Z and
18:28:25Z. Therefore this does not establish a permanently missing target or a current
delivery outage.

The zero-attempt result means `mesh-tell` was never successfully invoked for this message
before the 900-second bound. Current code intentionally checks `mind_idle()` before calling
`mesh-tell`; the historical pane state is not retained, so the exact per-poll reason for the
zero attempts is not recoverable from the available artifacts. The evidence supports a missed
idle-gated delivery, not a code-path failure.

## Current implementation and wiring checks

- `scripts/mesh-chat-deliver` and deployed `~/.local/bin/mesh-chat-deliver` are byte-identical,
  SHA-256 `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`.
- The source checks the age bound and emits `age-expiry` at lines 107-114; it checks the live
  idle gate before `mesh-tell` at lines 115-121.
- Cron wiring is live: `* * * * * $HOME/.local/bin/mesh-chat-deliver >> $HOME/.mesh/chat-deliver.log 2>&1`.
- `haunt` is present in the current `mesh-chat --targets` output.

## Verification

```text
scripts/mesh-chat-deliver --test                         PASS
bash tests/test-mesh-chat-deliver.sh                     PASS
  chaos emulator forced 2 transient mesh-tell failures before recovery
  transient recovery, terminal ACK, spaced terminal ACK, duplicate suppression, fresh-id reopen
```

No substrate state was changed. The known limitation remains: an idle-gated message can age out
without an attempt when its target does not present a stable idle pane during the retry horizon.
