# Health unblock resolver — iMac SSH credential boundary

Task: `unblock/health/47f1ba654a52aca9/resolve`
Owner: `health`
Observed: 2026-09-16T09:24:16Z

## Fresh verification

- `mesh-health` exited 0.
- `mesh-home`, `GL-MT3000`, `imac-rozalia`, and `phaedra` were PASS/reachable in the
  fresh sample; other configured peers remain offline.
- The prior decisive probe remains the latest authorized SSH evidence: transport to
  `imac-rozalia` succeeds, then authentication is refused. No credential correction
  event is recorded in the current evidence.

## Disposition

This resolver remains blocked on `external-event`: an authorized administrator must
correct or authorize the SSH key/account configuration on `imac-rozalia`.

Retry edge: after that correction is explicitly reported or evidenced, run
`mesh-task check dispatch health-warning/8a568c80615a3a8320e9/triage health`, then
`mesh-health --once` and the bounded batch SSH probe. Until then, do not retry blindly
and do not mutate remote credentials or substrate from this node.

## Delegation record

The Erdos sidecar was delegated a read-only audit of the prior evidence and safest
bounded retry. It made no writes or claims; its report remains advisory and was not
used as sole evidence. This receipt was personally inspected against the fresh
`mesh-health` output and the prior triage receipt.
