# Health-warning triage: `health-warning/4d44f4a79352c36fe656`

- Checked: `2026-09-11T23:50Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/4d44f4a79352c36fe656/triage`

## Verdict

Historical bounded delivery miss: the message from `genome` to `witness`
received three successful `mesh-tell` invocations but no ACK within the
delivery window. The delivery ledger terminated it as `attempt-limit` after
276 seconds. This is not evidence of a current target or substrate outage.

## Evidence

- `~/.mesh/chat-deliver.log` records attempts 1, 2, and 3 at
  `09:10:30Z`, `09:12:06Z`, and `09:14:06Z` on 2026-09-10; terminal failure
  was recorded at `09:15:05Z`, with `attempts:3 age:276s`.
- `~/.mesh/chat-deliver-ledger.json` records status `failed`, reason
  `attempt-limit`, target `witness`, and `failure_emitted: true` for message
  `1d28c9161073acce`.
- Current `mesh-chat --targets` includes `witness`; its tmux window has panes,
  including a `codex` pane. Later delivery evidence includes successful
  `witness` messages at `18:50Z`–`20:39Z` on 2026-09-11.
- The message was not retried after terminal failure. No ACK or receiver-side
  cause can be inferred from the delivery-attempt ledger alone.

## Wiring and verification

- Cron launches `$HOME/.local/bin/mesh-chat-deliver` every minute.
- `scripts/mesh-chat-deliver` matches the deployed executable (`cmp` exit 0).
- `python3 scripts/mesh-chat-deliver --test`: PASS.
- `bash tests/test-mesh-chat-deliver.sh`: PASS.
- `python3 tests/test-mesh-chat-deliver-attempts.py`: PASS.

No routing, DNS, firewall, VPN, Tailscale, or delivery configuration was
changed. The actionable limitation is that three successful sender-side
invocations do not establish that the receiver saw or acknowledged the
message; this historical episode has no remaining retry path.
