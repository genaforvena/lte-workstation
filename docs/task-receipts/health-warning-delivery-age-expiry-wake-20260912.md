# Health triage: self-targeted chat delivery age expiry to wake

Date: 2026-09-12  
Task: `health-warning/6baadbccffcf469f6cdd/triage`

## Finding

Two posts from `wake` to its own `wake` target, at 2026-09-09T04:26:30Z and
04:26:38Z, ended in `age-expiry` at 04:42:08Z (ages 933s and 925s against the
900s limit). Their IDs are `b9fe7a6fbe02cddb` and `b0fc90fc3112c92f`; both
ledger entries have `attempts: 0` and terminal status `failed`.

The posts were a live-refresh `[fyi]` and an `[idle]` status update. Since the
sender and target were both `wake`, the worker had to pass its stable-idle
check on the same pane that produced the posts. The failure records only show
that no `mesh-tell` handoff succeeded. `scripts/mesh-chat-deliver` discards
`mesh-tell` output and increments attempts only on a successful return, so the
historical evidence cannot distinguish the idle gate skipping the pane from a
failed `mesh-tell` invocation.

At triage time, `wake` remains in `mesh-chat --targets` and
`mesh-mind-state wake` reports `WORKING`; this establishes a live, currently
busy target, not the pane state during the historical retry window. No
delivery policy or substrate change is justified by these records. The exact
failed hop remains a known visibility gap.

## Evidence

- `/home/mesh-home/.mesh/chat.log`, lines 41191–41192: the original `wake`
  posts; line 41246: grouped terminal failure.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json`: entries for both IDs,
  `attempts=0`, `terminal_reason=age-expiry`.
- `/home/mesh-home/.mesh/chat-deliver.log`, lines 2009–2010: age 933s/925s,
  no successful delivery.
- `scripts/mesh-chat-deliver`: stable-idle gate precedes `mesh-tell`; failed
  calls are not recorded, and only successful calls increment `attempts`.
- Live target check: `mesh-chat --targets` includes `wake`;
  `mesh-mind-state wake` reports `WORKING`.

Disposition: investigated and documented as a historical, bounded expiry with
an unresolved delivery-visibility gap. No code, delivery configuration, or
mesh substrate was changed.
