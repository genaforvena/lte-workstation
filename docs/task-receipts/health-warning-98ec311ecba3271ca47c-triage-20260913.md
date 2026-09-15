# Health warning triage: `health-warning/98ec311ecba3271ca47c`

Task: `health-warning/98ec311ecba3271ca47c/triage`  
Owner: health / mesh-home

## Verdict

This was a bounded age-expiry of discover's camera-verification task to health.
The notification expired without a delivery attempt; health later completed the
requested real camera read and posted the verification. This is a historical
delivery miss, not evidence of a current health or camera outage. The exact
reason no attempt occurred is not recorded, so no delivery-policy or source
change is justified from this event. The expired task was not replayed.

## Evidence

- `~/.mesh/chat.log` line 59682 is the source row for message
  `b53929eea6a0738c`, first seen at `2026-09-13T14:35:14Z`. It asks health to
  run `mesh-imac-cam --test` against discover's iMac SSH/USB finding.
- `~/.mesh/chat-deliver.log` line 2554 records
  `2026-09-13T14:51:04Z delivery-failed`, `sender:discover`, `target:health`,
  `attempts:0`, `age:949s`, `window:5964370`.
- `~/.mesh/chat-deliver-ledger.json` records the same ID with
  `status=failed`, `terminal_reason=age-expiry`, `attempts=0`,
  `first_seen=2026-09-13T14:35:14Z`, and `failure_emitted=true`.
- Health's `[verify] discover→health` board line at `2026-09-13T15:03:16Z`
  reports a fresh `mesh-imac-cam --test` result: `REAL capture 220722B JPEG`.
  The command output was `smoke-test: ok (reachable; consented; binary
  deployed; REAL capture 220722B JPEG)`.
- Current `mesh-chat --targets` includes `health`. `mesh-mind-state health`
  reports the pane working now; neither observation reconstructs its
  momentary eligibility during the expired message's retry window.

## Delivery path and verification

`scripts/mesh-chat-deliver` first expires records at its 900-second age bound;
before expiry it only attempts `mesh-tell` when `mind_idle(target)` succeeds.
It does not persist each idle-gate result, so the precise zero-attempt cause is
unknown. The live cron entry runs the deployed worker every minute, and source
and deployment match at SHA-256
`dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae`.

```text
python3 scripts/mesh-chat-deliver --test       PASS
bash tests/test-mesh-chat-deliver.sh           PASS
python3 tests/test-mesh-chat-deliver-attempts.py PASS
mesh-chat --targets                            health present
```

No delivery retry, chat-deliver source change, or substrate mutation was made.
