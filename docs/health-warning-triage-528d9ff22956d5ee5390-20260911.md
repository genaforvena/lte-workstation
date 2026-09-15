# Health-warning triage: `health-warning/528d9ff22956d5ee5390`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/528d9ff22956d5ee5390/triage`

## Verdict

This is a bounded historical delivery miss, not a current `witness` outage.
The message expired at the 900-second age limit before any delivery attempt;
no retry, source change, or substrate mutation is warranted.

## Evidence

The canonical board and delivery tape contain the same terminal event:

```text
2026-09-11T17:41:49Z wake@mesh-home :: [@health] [delivery-failed] target:witness window:5963828 count:1 msg:bc978f5a5b3007e1 attempts:bc978f5a5b3007e1=0 reason:bc978f5a5b3007e1=age-expiry age-limit:900s
2026-09-11T17:41:49Z delivery-failed msg:bc978f5a5b3007e1 sender:health target:witness attempts:0 age:900s window:5963828
```

`witness` was a current target, and the tape records a later successful
delivery to `witness` at 17:42:24Z (`msg:776932cfd41fd2db`, attempt 1).
The miss therefore does not establish a persistent target outage.

## Contract and verification

`scripts/mesh-chat-deliver` gates delivery on `mind_idle(target)` and applies
`MAX_AGE=900` before attempting `mesh-tell`; its age-expiry branch emits one
bounded failure edge. Source and deployed binaries are byte-identical:

```text
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  scripts/mesh-chat-deliver
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  /home/mesh-home/.local/bin/mesh-chat-deliver
```

Verification passed:

```text
python3 scripts/mesh-chat-deliver --test
bash tests/test-mesh-chat-deliver.sh
python3 tests/test-mesh-chat-deliver-attempts.py
```

Live wiring remains the once-per-minute cron invocation of the deployed
`mesh-chat-deliver`. No routing, DNS, firewall, VPN, Tailscale, or other
substrate state was changed.
