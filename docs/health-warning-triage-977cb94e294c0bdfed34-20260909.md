# Health-warning triage `977cb94e294c0bdfed34` — 2026-09-09

## Live-task and instruction check

- `mesh-task status health-warning/977cb94e294c0bdfed34` showed one active step,
  `health-warning/977cb94e294c0bdfed34/triage`, owned by `health`.
- The current ledger description still matches the dispatched instruction: investigate
  the 2026-09-08 check-stream delta and report only; it explicitly says no substrate changes.
- No code change or substrate mutation was authorized or performed.

## Fresh read-only evidence

- `mesh-doctor --once`: completed; egress still rides `tailscale0` and the exit node
  `n2sbt7yy6t11CNTRL` remains set (both reported `FAIL`); Anthropic reachability and all
  supervised loops reported `PASS`. Existing microphone-default `WARN` also remains.
- `timeout 20 mesh-lan-presence --nodes`: timed out, `rc=124`; therefore LAN presence is
  still not positively observed and is recorded as `UNKNOWN`, not `DOWN`.
- `tailscale status`: `mesh-home` is present; `gl-mt3000-1` is `active; relay "fra"; offline,
  last seen 82d ago`; `imac-rozalia` is active/direct; `phaedra` is active/direct and is the
  exit node.
- `mesh-egress-health`: completed, `rc=0`.
- Read-only substrate observations: `ExitNodeAllowLANAccess=true`, `OperatorUser=mesh-home`,
  and `ip route get 192.168.8.1` resolves via `enp42s0` (`100.74.0.1`, source `100.74.20.47`).

## Disposition

This is a known degraded/observability condition, not evidence for a routing, DNS, firewall,
VPN, or Tailscale change. The warning's reporting-only instruction is correct. Close with the
fresh UNKNOWN/relay evidence and retain the next action: re-check LAN availability after the
existing ruling expires; do not mutate substrate on this receipt.
