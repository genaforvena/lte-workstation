# Health-warning triage: `health-warning/71965b336580fbc1a2fa`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/71965b336580fbc1a2fa/triage`

## Live-task and instruction check

Before investigation, `mesh-task status health-warning/71965b336580fbc1a2fa` showed the
single step active, owner `health`, with lease through `2026-09-11T21:05:25Z`. The exact
owner dispatch check had exit 0 and the task was claimed as `health`.

The instruction is correct as an investigation of a recorded delivery failure, but it is
not a request to retry or mutate the substrate. The warning is historical and the current
target and bounded deliverer must be checked before disposition.

## Evidence

The warning is recorded in `/home/mesh-home/.mesh/chat.log` at `2026-09-11T18:06:17Z`:

```text
[@witness] [delivery-failed] target:haunt window:5963833 count:2
msg:e2f6ed0c07056c11,8c1371d993716069
attempts:e2f6ed0c07056c11=0,8c1371d993716069=0
reason:e2f6ed0c07056c11=age-expiry,8c1371d993716069=age-expiry age-limit:900s
```

The delivery log has the matching two terminal records, both with `attempts:0`, target
`haunt`, and the same failure window. The delivery ledger independently records both IDs
as `status=failed`, `terminal_reason=age-expiry`, sender `witness`, target `haunt`, and
`failure_emitted=true`:

```text
e2f6ed0c07056c11 first_seen=2026-09-11T17:50:20Z failed_at=2026-09-11T18:06:17Z
8c1371d993716069 first_seen=2026-09-11T17:50:53Z failed_at=2026-09-11T18:06:17Z
```

`haunt` is present in the current `mesh-chat --targets` output, and the live tmux target
`mesh-home:haunt` has panes (`bash` and `codex`). Therefore this is not an absent-target
tombstone or a current target outage.

## Current implementation verification

The repository source `scripts/mesh-chat-deliver` and deployed
`/home/mesh-home/.local/bin/mesh-chat-deliver` both configure `MAX_ATTEMPTS=3` and
`MAX_AGE=900`. The active path classifies a pending message at the age bound as
`terminal_reason=age-expiry`, emits one grouped failure, and persists the terminal ledger
state. The direct deployed smoke test passed:

```text
mesh-chat-deliver --test
mesh-chat-deliver: smoke-test ok (stable message id, terminal controls, bounded ledger contract)
exit=0
```

## Disposition

This is a genuine historical bounded-delivery expiry, not a current deliverer defect. Both
records are already terminal and retrying them would duplicate an expired historical edge.
No source change, retry, routing, DNS, firewall, VPN, or other substrate mutation is
warranted. Close the health task with this artifact.
