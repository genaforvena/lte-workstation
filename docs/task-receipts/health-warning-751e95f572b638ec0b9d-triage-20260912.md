# Fleet check-stream delta triage — 2026-09-12

Task: `health-warning/751e95f572b638ec0b9d/triage` (owner `health`).

## Historical report

The 2026-09-09 14:54:58Z `[check]` line records a 14:30Z comprehensive
`mesh-doctor` result of 2 FAIL / 34 WARN, compared with 3 FAIL / 33 WARN at
11:42Z. It attributes the improvement to `mesh-claude-deepseek` smoke clearing
and the extra warning to a new category. The same report explicitly says
`mesh-lan-presence --nodes` was UNKNOWN/router unreachable, observed Tailscale,
egress, and DNS were unchanged, and no substrate was touched. This is a
reporting delta, not an instruction to alter routing or DNS.

## Current evidence

- A fresh `mesh-dash --once check` at 10:39:28Z reports fleet PATH `OK` with
  8 peers (2 direct, 0 relay, 6 offline), alongside a warning that high local
  load makes reachability probes unreliable. It shows egress on `tailscale0`
  and the exit-node SPOF as known failures.
- The dashboard's comprehensive doctor result is cached from 09:32:30Z and
  reads 3 FAIL / 34 WARN, including the two frozen egress/exit-node findings
  and recent vitality-log errors. This is not a fresh comprehensive result, so
  the old smoke-test delta cannot be carried forward as current.
- A direct `mesh-lan-presence --nodes` read returned `UNKNOWN`: no local
  `192.168.8.0/24` address and the router was unreachable. LAN/router presence
  remains a known blind.
- A current comprehensive `mesh-doctor` sweep was inadvertently started by
  `--help` (the command ran the doctor instead of showing usage). Its partial
  live output independently reproduced the egress-via-Tailscale and exit-node
  FAILs and reached nested smoke tests, but did not complete; it was interrupted
  after about four minutes. No conclusion is drawn from that partial run.

## Disposition

The historical `[check]` accurately described its 2026-09-09 observation and
made no substrate change request. Current route/exit-node findings remain
frozen; no routing, DNS, VPN, firewall, or other substrate state was changed.
The present comprehensive doctor count is unresolved because its cache is
stale and the attempted live sweep did not finish; router/LAN presence is
explicitly UNKNOWN. These are named visibility limits, not inferred healthy
states.

Verification: original timestamped board line; fresh check pane; direct LAN
presence result; and partial live doctor output were inspected. The live doctor
sweep exit status was 130 after interruption, so it is not counted as passing.
