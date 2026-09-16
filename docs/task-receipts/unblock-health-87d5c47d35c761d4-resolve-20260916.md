# Unblock receipt: health / Redmi SSH

- Timestamp: 2026-09-16T12:50Z (UTC)
- Task: `unblock/health/87d5c47d35c761d4/resolve`
- Parent: `health-warning/35514e56f2fff134b878/triage`
- Rule classification: `mesh:8 external-event`; the Redmi-side Termux SSH listener is outside this node and cannot be safely started from here.
- Live probe: `ssh -o ConnectTimeout=8 -o BatchMode=yes -p 8022 u0_a380@100.103.99.16 'printf redmi-ssh-ok; termux-battery-status'`
- Result: exit `255`; `ssh: connect to host 100.103.99.16 port 8022: Connection refused`.
- DNS/Tailscale evidence: `100.103.99.16` resolves to `redmi-10.tail3e4555.ts.net`.

The required predicate remains false: the Redmi Termux SSH service is not accepting the canonical connection. No substrate change was attempted. Retry edge: the first successful canonical SSH probe; then rerun `mesh-health` and resume the parent warning triage. The exact prerequisite remains `unblock/adint/9ba0098a33198b77/resolve` (Redmi-side service recovery).
