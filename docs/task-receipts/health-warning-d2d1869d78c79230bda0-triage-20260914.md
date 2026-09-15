# Triage historical operator hold and CGNAT route-repair snapshot

Task: `health-warning/d2d1869d78c79230bda0/triage`  
Source: health FYI at 2026-09-13T19:30:38Z

The source records an explicit operator hold: no route, exit-node, DNS,
firewall, WireGuard, healer/deploy, or DMS changes until operator release. It
also says the then-active route-repair step was rejected for its obsolete
100.76/16 scope while healer, deploy, and independent-verification successors
remained open. Canonical status still shows the parent
`exit-node-lan-cgnat-repair-20260912` rejected at step 1, with the three
successors open. The 20:53:56Z check pane continues to report the node's egress
interface as `tailscale0`; its current sample is a DERP/UDP latency reading,
with 0 bad samples in its 24-hour summary.

I found no later operator-release message in the retained post-hold chat lines
searched. Treat the hold as still in force: this health triage made no route,
exit-node, DNS, firewall, WireGuard, healer, deploy, DMS, or other substrate
change. The old route and gateway values are not revalidated here, and no
mutation is authorized by this historical FYI. Existing current exit-node and
LAN visibility receipts retain their separate findings.

## Verification

- Confirmed the exact source FYI in `/home/mesh-home/.mesh/chat.log`.
- `rtk mesh-task status exit-node-lan-cgnat-repair-20260912` shows its first
  step rejected and the three successors still open.
- `rtk mesh-dash --once check` at 20:53:56Z reports egress through
  `tailscale0`, a current DERP sample with UDP true, and 0/438 bad 24-hour
  samples; it does not report a current route-repair authorization.
- Searched post-hold chat lines for an operator release; none was found.
- No substrate command that changes live state was run.
