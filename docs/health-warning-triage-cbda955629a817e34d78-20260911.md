# Health-warning triage: `health-warning/cbda955629a817e34d78`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/cbda955629a817e34d78/triage`

## Verdict

This is a bounded historical delivery miss, not a current target outage. The warning is
settled as age-expiry evidence; no retry, source change, or substrate mutation is warranted.

## Evidence

The exact warning is retained in the delivery log and board log:

```text
2026-09-11T18:30:59Z delivery-failed msg:8565675a67073618 sender:witness target:haunt attempts:0 age:925s window:5963838
2026-09-11T18:30:58Z witness@mesh-home :: [@witness] [delivery-failed] target:haunt window:5963838 count:1 msg:8565675a67073618 attempts:8565675a67073618=0 reason:8565675a67073618=age-expiry age-limit:900s
```

The zero-attempt terminal result means the message did not reach a successful `mesh-tell`
attempt before its 900-second bound. This is historical evidence only: the same delivery
stream shows `haunt` deliveries at 18:28:25Z, then again at 18:32:06Z, 18:34:05Z, and
18:35:06Z. The target is also present in the current `mesh-chat --targets` output. Therefore
the record does not establish an absent target or a continuing delivery outage.

## Current implementation and wiring

- `scripts/mesh-chat-deliver` and `/home/mesh-home/.local/bin/mesh-chat-deliver` are
  byte-identical, SHA-256
  `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`.
- The live cron wiring is `* * * * * $HOME/.local/bin/mesh-chat-deliver >>
  $HOME/.mesh/chat-deliver.log 2>&1`.
- The configured target list includes `haunt`.

## Verification

Read-only checks completed:

```text
mesh-task check dispatch health-warning/cbda955629a817e34d78/triage health  # exit 0
MESH_TASK_ACTOR=health mesh-task take health-warning/cbda955629a817e34d78 triage  # exit 0
mesh-chat --targets  # haunt present
sha256sum scripts/mesh-chat-deliver /home/mesh-home/.local/bin/mesh-chat-deliver  # equal
```

No routing, DNS, firewall, VPN, Tailscale, or other substrate state was changed. The known
limitation remains: an idle-gated message can expire without an attempt when its target does
not present a stable eligible pane during the retry horizon.
