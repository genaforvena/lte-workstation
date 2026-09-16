# Health warning triage — 2026-09-16

- Task: `health-warning/f86cfd755268f3238974/triage`
- Owner: `health`
- Live pane: `pane:check` (top-pane health stream)
- Delegation: none; this was a tightly coupled live-health triage over mutable mesh/task state.

## Evidence

`mesh-dash --once check` completed with `rc=0` at 2026-09-16 16:55:40Z and rendered on
`pane:check`. The fresh stream reported:

- `PROBE-WARNING: LOCAL LOAD HIGH` and reachability probes unreliable
- `load-audit(1m): CPU=MIND-LOAD`, `load1=100.63/16c`
- `GPU-IDLE`, VRAM `1/12288M`, utilization `0%`
- egress currently `OK`, but cached doctor state had `FAIL=1 WARN=42`

`mesh-load-gate --quiet-hours witness` returned `rc=1` at the same turn. No substrate
mutation was attempted because the node is under active mesh-owned load and the gate is
explicitly a witness predicate.

## Disposition

Typed dependency/resource block: keep this warning open until the load gate passes. Retry
with a fresh `mesh-dash --once check`, require no `PROBE-WARNING: LOCAL LOAD HIGH`, then
rerun `mesh-load-gate --quiet-hours witness`; only after `rc=0` proceed to witness-task
autonomy verification. The exact live owner/resource predicate is the load gate, not an
operator approval or an external dependency.
