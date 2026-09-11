# Health-warning triage: `d95eb5b5d018eb3a3f93`

Date: 2026-09-11

## Claim liveness

The task was still live when dispatched: `mesh-task` ledger state was `open` for
`health-warning/d95eb5b5d018eb3a3f93/triage`, owner `health`.

## Current evidence

Commands run at 2026-09-11 03:26 UTC:

- `mesh-health` completed successfully. `mesh-home` and `phaedra` were PASS;
  seven peers were OFFLINE (GL-MT3000, Redmi 10, ilya, imac-rozalia,
  imozerov-Default-string, imozerov-IdeaPad-3-15IIL05, and rip). This disproves
  the warning's historical count of eight nodes down, but confirms peer
  reachability remains degraded.
- `mesh-fleet-health` reported `LOCAL LOAD HIGH` and explicitly marked the
  reachability probe `UNRELIABLE`; it did not establish that non-answers were
  node failures.
- `mesh-doctor --comprehensive` reached the live egress section and persisted a
  current sweep. The current summary is `2 FAIL, 33 WARN`: chronic FAILs are
  egress via `tailscale0` and a configured exit-node SPOF. Current WARNs include
  untimed peer SSH, sole-path bypasses, absence/timeout verdict conflation,
  smoke-test temporary-file leaks, unassessed tools, stale serial-confirm
  verdicts, orphan/dead-sign vehicles, topology leaks, and other known
  observability debt.

## Result

This warning is a stale snapshot of a known degraded/observability state, not a
new actionable node-down event. The only change from the source report is the
peer count; probe unreliability prevents honest promotion of the remaining
non-answers to confirmed failures. No routing, DNS, firewall, VPN, or other
substrate mutation was made.

Evidence sources: `~/.mesh/health-check.log`, current `mesh-health`,
`mesh-fleet-health`, and `mesh-doctor --comprehensive` output.
