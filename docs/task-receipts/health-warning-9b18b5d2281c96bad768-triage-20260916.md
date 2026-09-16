# Health warning triage: `health-warning/9b18b5d2281c96bad768/triage`

- Owner: `health`
- Warning: mesh-land autoland overlap
- Verified: `2026-09-16T13:55:00Z`

## Live evidence

`~/.mesh/land.log` records overlap refusals at `13:03:02Z`, `13:18:03Z`, and
`13:33:04Z`. The corresponding holder observations were 76s, 25s, and 8s;
each was below the configured escalation threshold of 900s. The latest entry
also records `autoland batch=40/94`, 21 settled candidates, and processing of
eligible candidates, so the overlap was bounded writer contention rather than
an abandoned writer.

At triage time, `pgrep -af mesh-land` found no live mesh-land process outside
the inspection command, and the backlog remained present at
`~/.mesh/mesh-land-backlog.tsv` (43,260 bytes, modified 12:14:25Z). No lock,
substrate, routing, DNS, firewall, VPN, or Tailscale state was changed.

## Disposition

Retain as a known healthy collision. No corrective mutation is justified from
these observations. Retry only on a fresh overlap refusal whose measured holder
age reaches the 900s escalation gate; then inspect the holder file descriptors
and deployed/source hashes before proposing a fix.
