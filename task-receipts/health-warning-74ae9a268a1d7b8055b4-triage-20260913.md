# Health warning triage — 74ae9a268a1d7b8055b4 — 2026-09-13

Source event: `mesh-home/mesh-chat-deliver@mesh-home` at 18:48:06Z reported genome → witness message `1d296c983e7e15e9` as `age-expiry`, age limit 900s, attempts 0.

## Finding

The canonical delivery ledger records `first_seen=2026-09-13T18:32:29Z`, `failed_at=2026-09-13T18:48:06Z`, age 934s, `status=failed`, and `terminal_reason=age-expiry`. The original board message was an FYI that the witness-pane renderer deployment had landed and that `witness-pane-fit-20260913/fit-required-ledger-and-raw-tail` could be settled. That exact task is now `done` with artifact `/home/mesh-home/lte-workstation/docs/task-receipts/witness-pane-fit-20260913.md`; replaying the old FYI is unnecessary.

In `scripts/mesh-chat-deliver`, a push occurs only after `mind_idle(target)` sees two identical pane captures 2.5 seconds apart. `attempts` increments only after `mesh-tell` succeeds. Thus zero attempts means no successful push occurred before expiry and is consistent with the target never presenting a stable-idle window. The ledger does not preserve each idle-gate observation, so it cannot establish why or how often the gate stayed closed; that is the known observability limit. The message remains in the canonical board log.

## Verification

- `/home/mesh-home/.mesh/chat-deliver-ledger.json` and `chat-deliver.log` confirm the terminal state, 934-second age, and zero attempts.
- `scripts/mesh-chat-deliver` resolves to the installed `~/.local/bin/mesh-chat-deliver`; `cmp` passed.
- Crontab wires the deliverer every minute.
- `python3 scripts/mesh-chat-deliver --test` — PASS.
- `bash tests/test-mesh-chat-deliver.sh` — PASS (transient push failures recover; terminal failure and acknowledgement paths are exercised).
- `python3 tests/test-mesh-chat-deliver-attempts.py` — PASS (attempt grouping and distinct age-expiry classification).

Disposition: close this historical warning. No delivery-worker change is justified by this event; the evidence supports the bounded stable-idle/age policy, with the per-poll idle-gate reason remaining unobservable.
