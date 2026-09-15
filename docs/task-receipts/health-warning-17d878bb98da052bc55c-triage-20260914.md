# Health roll-call triage: exit-node egress and LAN visibility

Task: `health-warning/17d878bb98da052bc55c/triage`  
Source warning: 2026-09-12T11:50:05Z roll-call

## Current evidence at 2026-09-14 19:43–19:52Z

- Public destination routing through `tailscale0 table 52` remains in place for this node's
  configured Phaedra exit-node consumer role. The fresh 19:52Z pane reports egress `OK loss=0%`;
  `tailscale status` lists Phaedra active and direct. The configured single-exit dependency is a
  real availability risk, but it is an existing policy constraint, not evidence that egress is
  currently failing.
- The current doctor cache is the policy-aware `FAIL=0 WARN=33` report. The completed
  `mesh-doctor-egress-policy-20260914.md` classifies the exit-node consumer path as intentional,
  while independently checking the local gateway FIB. The historical 11:48Z doctor failures
  predate this corrected policy.
- The separate local gateway path is healthy: `ip -4 route get 100.76.0.1` returns `dev enp42s0`,
  table 52 has `throw 100.76.0.0/16`, and the 19:43Z refreshed card reports
  `exit-node-lan: ok` plus `invariant-check: OK`.
- `mesh-lan-presence --nodes` remains `UNKNOWN` (exit 1) because no local address is present in
  `192.168.8.0/24`, ARP cannot see that segment, and no known host answered ICMP. This is a
  persistent visibility gap already recorded by prior health triages; it is not disproved by
  egress or gateway success.
- The retired route proposal remains `route:no | PROPOSE none`; no new route change was proposed by
  this warning.

## Disposition

This is a duplicate historical roll-call. The expected exit-node route and its single-node
availability risk remain known; the gateway FIB is verified healthy; historical doctor FAILs have
been superseded by the current zero-FAIL policy-aware report; and inward LAN presence remains an
explicit UNKNOWN. Reject the stale duplicate and keep those distinct facts visible. No route,
DNS, VPN, firewall, or service state was changed. Reopen only on a fresh egress failure, unexpected
local-gateway path, or a concrete resilience task with safe alternate-path evidence.

## Verification

- `mesh-dash --once check` at 19:52Z: current egress loss 0%, doctor FAIL=0 WARN=33.
- `tailscale status`: Phaedra active and direct; configured as exit node.
- `mesh-card --refresh` at 19:43:36Z: gateway FIB and invariant check OK.
- `ip -4 route get 100.76.0.1`: local `enp42s0`; table 52 includes the connected-prefix throw.
- `mesh-lan-presence --nodes`: exit 1, `UNKNOWN` for the stated visibility limits.
- Read the role-aware doctor and live-egress receipts; no new route proposal or actionable repair
  prerequisite was found.
