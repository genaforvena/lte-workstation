# Health-warning triage: `health-warning/1dc869a84c6a257b57db`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/1dc869a84c6a257b57db/triage`

## Verdict

Historical bounded delivery miss; no current substrate action is safe or
warranted. The message to `witness` expired before an attempt was made.

## Evidence

Exact record in `~/.mesh/chat-deliver.log` and `~/.mesh/chat.log`:

```text
2026-09-11T14:09:07Z delivery-failed msg:53c5c8433034c4d7 sender:genome target:witness attempts:0 age:932s window:5963785
```

`attempts:0` plus `age:932s` exceeds the implementation's 900-second age
limit, so this is age expiry rather than a failed `mesh-tell` attempt. The
current target registry includes `witness`; this record alone does not justify
restarting or changing routing, DNS, firewall, VPN, or Tailscale state.

## Wiring and verification

- Cron wiring is active: `* * * * * $HOME/.local/bin/mesh-chat-deliver >> $HOME/.mesh/chat-deliver.log 2>&1`.
- `scripts/mesh-chat-deliver` and the deployed binary are byte-identical (verified with `cmp`).
- `mesh-chat --targets`: `witness` present.
- `python3 scripts/mesh-chat-deliver --test`: PASS.
- `bash tests/test-mesh-chat-deliver.sh`: PASS.
- `python3 tests/test-mesh-chat-deliver-attempts.py`: PASS.

Known limitation: idle-gated delivery can age out without an attempt when the
target has no stable eligible pane during the retry horizon.

No substrate state was changed.
