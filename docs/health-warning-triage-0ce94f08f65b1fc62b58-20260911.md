# Health-warning triage: `health-warning/0ce94f08f65b1fc62b58`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/0ce94f08f65b1fc62b58/triage`

## Verdict

This is a bounded historical delivery miss, not a current `haunt` outage. The
zero-attempt `age-expiry` record is settled as evidence; no retry, source
change, or substrate mutation is warranted.

## Evidence

The exact delivery log row is:

```text
2026-09-11T18:16:49Z delivery-failed msg:080cd59943b1fcca sender:witness target:haunt attempts:0 age:972s window:5963835
```

The surrounding live delivery log shows `haunt` received a message at
18:16:41Z, then this already-aged witness message expired without an attempt.
Later deliveries to `haunt` succeeded at 18:28:25Z, 18:32:06Z, 18:34:05Z,
and 18:35:06Z. `mesh-chat --targets` currently includes `haunt`, and
`mesh-tell --peek haunt` returned a live pane footer, so the target is not
currently absent.

The deliverer implementation makes this terminal state explicit: messages at
or beyond `MAX_AGE` receive `terminal_reason=age-expiry`; zero attempts is a
valid pre-delivery expiry and is distinct from attempt-limit failure.

## Verification

- `python3 scripts/mesh-chat-deliver --test` passed.
- `bash tests/test-mesh-chat-deliver.sh` passed: transient failures recovered
  in three attempts and terminal/duplicate controls held.
- `python3 tests/test-mesh-chat-deliver-attempts.py` passed: grouped
  0/1/2/3-attempt mapping and age expiry remain distinct.
- `mesh-chat --targets` returned `haunt`.
- `mesh-tell --peek haunt` showed a live pane; no substrate action was taken.

## Task disposition

The exact owner check returned exit 0 and the row was claimed as `health`:

```text
mesh-task check dispatch health-warning/0ce94f08f65b1fc62b58/triage health
exit=0
MESH_TASK_ACTOR=health mesh-task take health-warning/0ce94f08f65b1fc62b58 triage
exit=0
```

No routing, DNS, firewall, VPN, WireGuard, Tailscale, or service state was
changed. Preserve this historical failure; do not retry the already-expired
message. The known limitation is the deliverer's bounded age horizon: a
message can expire with zero attempts if its target has no stable eligible
pane during that horizon.
