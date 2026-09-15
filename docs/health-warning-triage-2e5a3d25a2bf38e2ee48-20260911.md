# Health-warning triage: `health-warning/2e5a3d25a2bf38e2ee48`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/2e5a3d25a2bf38e2ee48/triage`

## Verdict

This is a bounded historical delivery miss, not a current `haunt` outage. The
zero-attempt `age-expiry` warning is settled as historical evidence; no retry,
source change, or substrate mutation is warranted.

## Evidence

The exact delivery record is present in `~/.mesh/chat-deliver.log`:

```text
2026-09-11T18:30:29Z delivery-failed msg:402133c6256c2752 sender:witness target:haunt attempts:0 age:956s window:5963838
```

The 900-second age limit expired before any delivery attempt. The same log
shows successful `haunt` deliveries at 18:32:06Z, 18:34:05Z, 18:35:06Z, and
18:35:14Z, so the target recovered/presented after the bounded miss rather
than remaining unavailable. `mesh-chat --targets` currently includes
`haunt`.

## Current wiring and implementation

- Cron runs `$HOME/.local/bin/mesh-chat-deliver` every minute and appends to
  `~/.mesh/chat-deliver.log`.
- `scripts/mesh-chat-deliver` and the deployed binary are byte-identical,
  SHA-256 `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`.

## Verification

```text
mesh-dash --once check                         PASS (state captured before triage)
mesh-task check dispatch ... health             exit 0
MESH_TASK_ACTOR=health mesh-task take ...       exit 0
mesh-chat --targets                            haunt present
python3 scripts/mesh-chat-deliver --test       PASS
bash tests/test-mesh-chat-deliver.sh           PASS
python3 tests/test-mesh-chat-deliver-attempts.py PASS
```

No routing, DNS, firewall, VPN, Tailscale, or other substrate state was
changed. Known limitation: an idle-gated message can expire without an
attempt when its target has no stable eligible pane during the retry horizon.
