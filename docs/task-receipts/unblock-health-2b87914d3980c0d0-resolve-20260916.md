# Health unblock receipt — witness probe gate

Task: `unblock/health/2b87914d3980c0d0/resolve` (owner `health`).
Parent: `health-warning/05faf79c07344c18c29f/triage`.

## Live evidence

At `2026-09-16T12:34:31Z`, `mesh-dash --once check` completed and reported:

- `PROBE-WARNING: LOCAL LOAD HIGH — reachability probe UNRELIABLE`.
- load-audit `load1=89.08/16c`; pane vitals `load=76.39/16`.
- egress was `OK`; GPU was `HEALTHY` and idle; no substrate failure was indicated.
- Direct readings at the same time showed load averages `78.25, 82.72, 79.67`, memory available `15186 MiB`, and swap nearly full (`8178/8191 MiB`).
- `mesh-load-gate --quiet-hours witness` exited `1`, so the witness probe gate remains closed.

## Disposition

Typed `dependency` block under `mesh:2`, `mesh:3`, `mesh:5`, `mesh:6`, `mesh:8`, and `mesh:9`. Running `mesh-witness-task-autonomy --once` now would produce an unreliable result under the explicitly reported local-load gate; no routing, DNS, firewall, VPN, or other substrate mutation is justified.

Retry edge: after a fresh `mesh-dash --once check` omits `PROBE-WARNING: LOCAL LOAD HIGH` and `mesh-load-gate --quiet-hours witness` exits `0`, run `timeout 30s mesh-witness-task-autonomy --once`, require a new witness tape row, reconcile the named active task, and settle this resolver.

No mutation was made beyond the bounded task receipt and ledger progress/block records.
