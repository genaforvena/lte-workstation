# Unblock receipt — `unblock/adint/5a366973cb848010/resolve`

Recorded: 2026-09-16T09:47:02Z
Owner: `adint`
Parent: `unblock/health/47f1ba654a52aca9/resolve`

## Fresh verification

`mesh-health --once` exited 0 and reported `imac-rozalia` PASS at
`100.121.88.110`. The bounded batch SSH probe reached the host but authentication
was refused:

```text
timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true
mesh-home@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
SSH_PROBE_RC=255
```

No credential or remote configuration was changed.

## Disposition and retry edge

This is a typed `external-event` block. An authorized administrator must correct
or authorize the SSH key/account configuration on `imac-rozalia`. After that
correction is evidenced, run:

```text
mesh-task check dispatch health-warning/8a568c80615a3a8320e9/triage health
mesh-health --once
timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true
```

Only a successful authorized SSH probe permits resuming the parent health triage.

## Delegation record

No subagent was launched: this was a tightly coupled owner/lifecycle recovery
check, and the safe action plus artifact verification had to remain in this pane.
The receipt was personally verified against the fresh `mesh-health` output and
the fresh bounded SSH probe.
