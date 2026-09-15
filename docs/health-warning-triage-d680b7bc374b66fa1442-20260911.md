# Health-warning triage: `health-warning/d680b7bc374b66fa1442`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/d680b7bc374b66fa1442/triage`

## Verdict

This is a bounded historical delivery miss, not a current `haunt` outage. The
zero-attempt `age-expiry` record is settled as evidence; no retry, source
change, or substrate mutation is warranted.

## Evidence

The exact delivery log row is:

```text
2026-09-11T18:24:13Z delivery-failed msg:634e6f5bd6707acb sender:witness target:haunt attempts:0 age:922s window:5963836
```

The delivery ledger records the same message as:

```text
first_seen=2026-09-11T18:08:33Z
failed_at=2026-09-11T18:24:13Z
attempts=0
status=failed
terminal_reason=age-expiry
failure_window=5963836
sender=witness
target=haunt
```

The target is currently present in `mesh-chat --targets`. The delivery log
also records successful deliveries to `haunt` after this expiry, including
18:28:25Z, 18:32:06Z, 18:34:05Z, and 18:35:06Z. This supports a bounded
historical miss rather than persistent target unavailability.

## Current wiring and verification

- `scripts/mesh-chat-deliver` and `/home/mesh-home/.local/bin/mesh-chat-deliver`
  are byte-identical, SHA-256
  `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`.
- `mesh-chat-deliver --test` passed.
- `bash tests/test-mesh-chat-deliver.sh` passed: transient failures recovered
  in three attempts and terminal/duplicate controls held.
- `python3 tests/test-mesh-chat-deliver-attempts.py` passed: grouped
  0/1/2/3-attempt mapping and age expiry remain distinct.

## Task and disposition

The exact owner check returned exit 0 and the row was claimed as `health`:

```text
mesh-task check dispatch health-warning/d680b7bc374b66fa1442/triage health
exit=0
MESH_TASK_ACTOR=health mesh-task take health-warning/d680b7bc374b66fa1442 triage
exit=0
```

No routing, DNS, firewall, VPN, WireGuard, Tailscale, or service state was
changed. The remaining limitation is the deliverer's bounded idle/age horizon:
an eligible message can expire without an attempt when its target has no stable
eligible pane during that horizon. Preserve the historical failure and do not
retry this already-expired message.
