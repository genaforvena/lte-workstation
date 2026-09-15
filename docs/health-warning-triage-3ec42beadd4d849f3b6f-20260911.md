# Health-warning triage: `health-warning/3ec42beadd4d849f3b6f`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/3ec42beadd4d849f3b6f/triage`

## Evidence

The source warning is present in `/home/mesh-home/.mesh/chat.log`:

```text
2026-09-11T18:05:26Z mesh-home/mesh-chat-deliver@mesh-home ::
[@witness] [delivery-failed] target:haunt window:5963833 count:1
msg:9556a1fc2e24513b attempts:9556a1fc2e24513b=0
reason:9556a1fc2e24513b=age-expiry age-limit:900s
```

The delivery tape independently records the same terminal event:

```text
2026-09-11T18:05:26Z delivery-failed msg:9556a1fc2e24513b sender:witness
target:haunt attempts:0 age:961s window:5963833
```

The ledger entry for `9556a1fc2e24513b` has `status=failed`,
`terminal_reason=age-expiry`, `attempts=0`, `failure_emitted=true`,
`first_seen=2026-09-11T17:49:02Z`, and `failed_at=2026-09-11T18:05:26Z`.

`haunt` remains a current `mesh-chat --targets` target and the `mesh-home:haunt`
tmux window is present with two panes. The delivery log also shows later successful
Haunt deliveries, including `7ecce4f51c94a2e8` at 18:28:25Z and
`af41c2982a8fd58e` at 18:32:06Z. This is therefore a historical expiry, not proof
of an absent target or a current target outage.

## Implementation check and disposition

Source and deployed `mesh-chat-deliver` use `MAX_ATTEMPTS=3` and `MAX_AGE=900`;
the age-bound path records `terminal_reason=age-expiry` and emits the bounded
failure. `mesh-chat-deliver --test` passed:

```text
mesh-chat-deliver: smoke-test ok (stable message id, terminal controls, bounded ledger contract)
```

No retry, source change, routing, DNS, firewall, VPN, or other substrate mutation
is warranted. Retrying this terminal zero-attempt record would duplicate historical
work. The task is complete with this artifact.
