# Unblock receipt: adint / a8ae96857cfedae4

- Task: `unblock/adint/a8ae96857cfedae4/resolve`
- Owner: `adint`
- Parent blocked task: `unblock/health/47f1ba654a52aca9/resolve`
- Live predicate: the iMac is reachable, but this node is not authorized to
  authenticate over SSH; the external credential/account correction is still
  absent.

## Evidence

- `mesh-health --once` at `2026-09-16T12:19:07Z` returned rc=0 and rendered
  `PASS imac-rozalia 100.121.88.110`.
- Real bounded probe in the same `2026-09-16T12:19Z` live-check batch:
  `timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=8 imac-rozalia 'printf ssh-ok'`
  returned rc=255 with `Permission denied (publickey,password,keyboard-interactive)`.
- `mesh-task check dispatch health-warning/8a568c80615a3a8320e9/triage health`
  returned rc=2; the canonical chain remains `status=blocked` with
  `needs=authorized administrator corrects or authorizes SSH key/account
  configuration on imac-rozalia`.

## Result and retry

This is an `external-event` block, not a node-owned dependency: network reachability
is present, while changing the remote account/key authorization would cross the
authorized iMac boundary. The exact retry is: after an authorized administrator
corrects or authorizes SSH for `mesh-home@imac-rozalia`, rerun the dispatch check,
`mesh-health --once`, and the bounded SSH probe. Resume the parent only when the
probe succeeds.

## Delegation

Delegated `adint-unblock-diagnosis` through the shared coding-agent relay for
read-only diagnosis. The relay produced no worker shim or artifact during this
turn; no worker report was used as evidence. The evidence above was inspected
directly from live commands and canonical task JSON.

## Recovery wake recheck — 2026-09-16T12:48Z

Fresh bounded probe:

```text
timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no imac-rozalia true
-> Permission denied (publickey,password,keyboard-interactive), rc=255
```

The external credential/account correction remains absent. No mesh-owned
prerequisite can safely repair a remote iMac's SSH authorization; retry after an
authorized administrator changes that remote account/key configuration.
