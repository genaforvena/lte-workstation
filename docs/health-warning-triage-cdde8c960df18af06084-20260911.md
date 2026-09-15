# Health-warning triage: `health-warning/cdde8c960df18af06084`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/cdde8c960df18af06084/triage`

## Verdict

The warning is a historical, bounded delivery miss, not a current `witness`
outage. Message `12cf3723e4b5f7f6` reached the 900-second age bound with zero
attempts at 2026-09-11T17:35:23Z. Retrying a terminal record or changing
substrate is not warranted.

## Evidence

The primary delivery tape records:

```text
2026-09-11T17:35:23Z delivery-failed msg:12cf3723e4b5f7f6 sender:haunt target:witness attempts:0 age:939s window:5963827
```

The same tape shows `witness` deliveries immediately around the warning and
continuing afterward, including successful `witness` messages at 17:42:24Z,
17:44:06Z, 17:45:16Z, 17:46:17Z, and later through 20:39:06Z. Thus the target and deliverer were
live; this event is a stale historical miss.

## Delivery contract verification

Current source and deployed `mesh-chat-deliver` are byte-identical:

```text
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  scripts/mesh-chat-deliver
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  /home/mesh-home/.local/bin/mesh-chat-deliver
```

Fresh checks passed:

```text
python3 scripts/mesh-chat-deliver --test                 PASS
bash tests/test-mesh-chat-deliver.sh                     PASS
python3 tests/test-mesh-chat-deliver-attempts.py         PASS
cmp scripts/mesh-chat-deliver /home/mesh-home/.local/bin/mesh-chat-deliver  PASS
```

`witness` is present in `mesh-chat --targets`, and cron wires the deployed
deliverer every minute. No routing, DNS, firewall, VPN, Tailscale, or other
substrate state was changed.
