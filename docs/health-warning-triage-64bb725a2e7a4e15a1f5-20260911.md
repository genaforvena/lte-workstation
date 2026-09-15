# Health-warning triage: `health-warning/64bb725a2e7a4e15a1f5`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/64bb725a2e7a4e15a1f5/triage`

## Verdict

The warning is valid historical evidence of a bounded delivery miss, not a
current `witness` outage. The message reached the 900-second age bound with
zero attempts; retrying a terminal record or changing substrate is not
warranted.

## Current-state audit

The task was live when checked (`mesh-task status` reported `open`, owner
`health`), and the instruction matches the canonical records:

```text
2026-09-11T17:47:20Z delivery-failed msg:b50502c2abb8325a sender:vpn target:witness attempts:0 age:951s window:5963829
2026-09-11T17:47:20Z ... [@vpn] [delivery-failed] target:witness window:5963829 count:1 msg:b50502c2abb8325a attempts:b50502c2abb8325a=0 reason:b50502c2abb8325a=age-expiry age-limit:900s
```

`witness` remains a current `mesh-chat --targets` target. The delivery tape
also records successful deliveries to `witness` immediately before and after
the warning, including `06752d747d77c98a` at 17:46:17Z and attempts 2 and 3
at 17:47:52Z and 17:50:10Z. This is not evidence of a persistent target
failure.

## Implementation and verification

Current source applies `MAX_AGE=900` and checks `mind_idle(target)` before
calling `mesh-tell`; the age-expiry path emits one bounded failure record.
Source and deployed `mesh-chat-deliver` are byte-identical:

```text
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  scripts/mesh-chat-deliver
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  /home/mesh-home/.local/bin/mesh-chat-deliver
```

Passed checks:

```text
python3 scripts/mesh-chat-deliver --test
bash tests/test-mesh-chat-deliver.sh
python3 tests/test-mesh-chat-deliver-attempts.py
```

The deployed path is wired once per minute by cron. No routing, DNS,
firewall, VPN, Tailscale, or other substrate state was changed.
