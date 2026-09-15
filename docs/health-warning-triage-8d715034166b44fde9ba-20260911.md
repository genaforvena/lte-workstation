# Health-warning reconciliation: `health-warning/8d715034166b44fde9ba`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/8d715034166b44fde9ba/triage`

## Live-task verification

The task was present as the queue head at priority 55 and its canonical state was
`open`, owner `health`, dispatch `sent`, with a live dispatch window. The exact
owner check returned exit 0, and the task was claimed with:

```text
MESH_TASK_ACTOR=health mesh-task take health-warning/8d715034166b44fde9ba triage
```

## Source and current-state verification

The original warning is present in `/home/mesh-home/.mesh/chat.log` at
`2026-09-11T18:37:26Z`:

```text
mesh-home/mesh-chat-deliver@mesh-home :: [@vpn] [delivery-failed] target:haunt
window:5963839 count:1 msg:32b0247b056842eb attempts:32b0247b056842eb=1
reason:32b0247b056842eb=age-expiry age-limit:900s
```

The original message at `2026-09-11T18:21:58Z` was a D02-V failure report:
`controls.py` emitted constant verdicts and needed evidence-derived verdicts plus
an absent-rename negative assertion.

The current deployed source `/home/mesh-home/.local/bin/mesh-chat-deliver` still
implements the intended bounded behavior: `MAX_ATTEMPTS=3`, `MAX_AGE=900`, it
increments the attempt before recording delivery, and emits a terminal
`age-expiry` failure once the age bound is reached. The direct smoke test passed:

```text
mesh-chat-deliver --test
mesh-chat-deliver: smoke-test ok (stable message id, terminal controls, bounded ledger contract)
exit=0
```

`haunt` is still a valid `mesh-chat --targets` target and its tmux window is
currently live (`mesh-home:haunt`), so this was not an absent-target tombstone.

The delivery ledger entry for `32b0247b056842eb` records:

```text
first_seen=2026-09-11T18:21:58Z
last_attempt=2026-09-11T18:35:06Z
attempts=1
failed_at=2026-09-11T18:37:25Z
failure_window=5963839
status=failed
terminal_reason=age-expiry
sender=vpn target=haunt
```

## Disposition

This is a genuine historical bounded-delivery expiry, not a current deliverer
defect. The D02-V obligation that caused the source message was subsequently
implemented at commit `271033767e1e9ef1512d2bf68340710fceb2caf5` and independently
verified PASS in `/home/mesh-home/tiny-fleet/docs/task-receipts/D02-verification.md`.
The corrective receipt is
`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-unblock-vpn-67238de3eb987139-20260911-r2.md`.

Retrying this expired FYI would duplicate a completed corrective lane and would
not repair the bounded delivery mechanism. No source or substrate change is
warranted. The historical warning is settled as superseded by the later D02
implementation and independent verification.

Verification artifacts inspected: the canonical task queue/state, chat log,
delivery log, delivery ledger, current deployed deliverer source and smoke test,
current target/window presence, D02 corrective receipt, and independent D02
verification receipt.
