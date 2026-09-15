# Health self-unblock resolver receipt

- Task: `unblock/health/9e305574715297cb/resolve`
- Parent: `health-warning/0ac2476a343fdde6c790/triage`
- Checked: 2026-09-11T23:18Z

## Evidence

- Live `tailscale status --json` showed `phaedra` and `imac-rozalia` online and multiple peer entries offline; the one-shot dashboard reports eight down. The named offline peers have no safe local actuator from this node.
- `tailscale ping --c 1 --timeout 5s imac-rozalia` returned a direct pong in 7 ms via `5.227.25.156:55351`.
- `nc -vz -w 3 100.121.88.110 22` succeeded, while batch SSH to the same address was refused with `Permission denied (publickey,password,keyboard-interactive)`.
- The earlier same-day owner-side check from reachable `phaedra` also reached the iMac but had both tested SSH identities refused; that owner has no `mesh-health` executable. See [the prior resolver receipt](unblock-health-307493a2c07b9e25-resolve-20260911.md).

## Disposition

The current evidence narrows the iMac failure to SSH authorization; it does not supply credentials or authority to repair the target. The offline peers likewise have no reachable owner or local actuation path established by this warning. No substrate changes are safe or indicated. The prerequisite is externally owned and remains irreducible from this node. Keep the parent task blocked and retry only on `event:roll-call-delta` or when an authorized reachable owner provides a valid repair path. Do not resume the parent now.
