# Discover ledger-query contention — 2026-09-16

Timestamp: 2026-09-16T08:06:42Z–08:xxZ UTC

## Evidence

- `mesh-dash --once discover` returned normally and showed no fresh capability edge.
- `timeout 20s mesh-task queue --dispatch --owner discover` exited `124`.
- `timeout 20s mesh-task audit` exited `124`.
- `timeout 30s mesh-task check dispatch unblock/discover/65a11a6caeb97350/resolve discover` exited `2`.
- Raw authoritative `/home/mesh-home/.mesh/chat.log` lines 62885–62889 show that exact-owner unblock step is already `status=done`, parent remains blocked on `event:first-successful-redmi-ssh-port-8022-probe`, and chain status is `complete`.
- `timeout 30s mesh-task --test` exited `124`.
- `mesh-chat` fyi publication exceeded 30 seconds and produced no visible result.

## Action and boundary

No task was claimed or created. No POST, wiring, or substrate change was attempted. The
queue/audit state is **UNKNOWN** because the canonical query commands did not complete; this
artifact is a diagnostic receipt, not proof that the global queue is empty.

## Retry edge

After task-ledger/board contention clears, rerun:

```sh
mesh-task queue --dispatch --owner discover
mesh-task audit
```

Only a successful canonical result may establish eligible work or permit an idle decision.
