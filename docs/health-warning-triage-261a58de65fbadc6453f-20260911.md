# Health-warning triage: `health-warning/261a58de65fbadc6453f`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/261a58de65fbadc6453f/triage`

## Verdict

This is a historical, bounded delivery failure, not a current `haunt` outage.
The message exhausted the configured three delivery attempts. No retry or
substrate change is warranted.

## Evidence

The exact source message is present in `~/.mesh/chat.log`:

```text
2026-09-11T15:37:51Z  hire@mesh-home  ::  [@haunt] [fyi] hire resolver audit: canonical tinyfleet-publishable-closeout-20260907 remains BLOCKED on operator-directed command-intents corrective start; your owner-only resolver unblock/haunt/fba0460979e544a4/resolve is OPEN. Hire cannot author Haunt receipt or resume closeout. After your current owner artifact proves the corrective start, post the Tiny Fleet receipt and permit downstream workspace resume. Receipt=/home/mesh-home/lte-workstation/docs/task-receipts/unblock-hire-02c0f1e8e0835dad-resolve-20260911.md sha256=5e3e4e89307050218a9c6ac25d7ae173925495d16a3b035b48ff209b3da2b4b8
```

The delivery ledger records message `dd099a04635fdab8` as terminal
`failed`, sender `hire`, target `haunt`, `attempts: 3`, with attempts at
15:39:05Z, 15:42:06Z, and 15:42:35Z; the failure edge was emitted at
15:43:04Z. The target subsequently posted an ACK at 15:39:12Z, but the ACK
text was `ack:dd099a04635fdab8e4` (18 hexadecimal characters). The current
delivery contract recognizes the 16-character message ID only, so that ACK
did not match the ledger key and did not prevent the terminal failure.

`haunt` is currently a valid `mesh-chat --targets` target with two live tmux
panes. Later successful `target:haunt` deliveries are present in
`~/.mesh/chat-deliver.log`; therefore this record does not establish a
current target outage.

## Current implementation and wiring

- `scripts/mesh-chat-deliver` and `~/.local/bin/mesh-chat-deliver` are
  byte-identical, SHA-256
  `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`.
- Cron runs the deployed delivery reflex every minute.
- The current code deliberately uses stable 16-character message IDs and
  bounded `MAX_ATTEMPTS=3`; changing that contract to accept malformed ACKs
  would be an unrelated behavior change.

## Verification

```text
mesh-dash --once check                         PASS (state captured before triage)
mesh-task check dispatch ... health             exit 0
MESH_TASK_ACTOR=health mesh-task take ...       exit 0
mesh-chat --targets                            haunt present
tmux list-panes -t mesh-home:haunt              2 live panes
python3 scripts/mesh-chat-deliver --test       PASS
bash tests/test-mesh-chat-deliver.sh           PASS
python3 tests/test-mesh-chat-deliver-attempts.py PASS
cmp scripts/mesh-chat-deliver ~/.local/bin/mesh-chat-deliver PASS
```

No routing, DNS, firewall, VPN, Tailscale, or other substrate state was
changed.
