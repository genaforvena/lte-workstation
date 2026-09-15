# Health-warning triage: `health-warning/3c78fe63c7446071f7cf`

- Checked: 2026-09-12T12:10–12:16Z
- Owner: `health` on `mesh-home`
- Task: `health-warning/3c78fe63c7446071f7cf/triage`

## Verdict

The 2026-09-10 warning is partly historical, but the persistent egress and LAN-visibility
conditions remain current. The live check pane now reports `PATH: DEGRADED`, with two reachable
nodes, one direct and one relayed peer; the route lookup still selects `tailscale0` in table 52.
`mesh-lan-presence --nodes` still reports UNKNOWN because the router/192.168.8.0/24 cannot be
reached from this node. External egress is currently healthy (`mesh-egress-health` exit 0,
state `OK`, Anthropic 405). No substrate configuration changed.

The peer details no longer match the old warning: current Tailscale JSON reports `phaedra` online,
active, relayed via `tor`, and the exit node; `imac-rozalia` online but inactive, relayed via
`hel`. `mesh-health` can SSH to phaedra, while imac SSH authentication is refused. These are fresh
observations and do not establish a stable relay classification. The current pane's doctor cache
is still 36 minutes old (11:33:51Z, FAIL=3/WARN=33), so neither the old 2F/34W nor that cached
3F/33W is asserted as a fresh total.

A fresh `mesh-doctor` run was started at approximately 12:11Z. Its partial output reconfirmed
overlay egress and exit-node SPOF as FAILs, Anthropic reachability as PASS, and also surfaced an
untimed peer-SSH WARN, a mic-default-device WARN, and six bypasses of one declared sole-path funnel.
The command was still running at 12:16Z during tool smoke tests; its final totals are unverified.
This is an explicit remaining blind spot, not a pass or a final doctor result.

## Evidence

Original warning: `/home/mesh-home/.mesh/chat.log:43992` (2026-09-10T03:00:16Z). It reported
2F/34W, LAN UNKNOWN, imac active through relay hel, phaedra direct active exit, and egress through
`tailscale0` with an exit-node SPOF.

Live pane: `mesh-dash --once check` (2026-09-12T12:10:42–12:10:50Z, exit 0):

```text
egress tailscale0 | supervised 4UP/0DOWN | organs 15LIVE/0DARK
10 nodes: 2 ssh · 0 lan · 8 down | PATH: DEGRADED OK peers=8 direct=1 relay=1…
DOCTOR (this node, cached 36m): 2026-09-12T11:33:51Z FAIL=3 WARN=33
egress now: OK loss=0% avg=134.248ms mdev=0.975ms
```

Focused fresh probes:

```text
$ mesh-health
PASS mesh-home 100.81.222.19 (self)
SKIP imac-rozalia 100.121.88.110 — SSH authentication refused
PASS phaedra 100.94.116.17
...other listed peers OFFLINE...

$ mesh-lan-presence --nodes
? 192.168.8.0/24 ? UNKNOWN
mesh-lan-presence: router unreachable — UNKNOWN (no local address in 192.168.8.0/24; ARP
cannot see that segment from here, and no known host answered ICMP)
exit=1

$ ip route get 1.1.1.1
1.1.1.1 dev tailscale0 table 52 src 100.81.222.19 uid 1000

$ tailscale status --json | jq ...
{"HostName":"phaedra","Online":true,"Active":true,"Relay":"tor","ExitNode":true}
{"HostName":"imac-rozalia","Online":true,"Active":false,"Relay":"hel","ExitNode":false}

$ mesh-egress-health
<no output>
exit=0
state=OK
cause=OK qfunc=PRESERVED anth=405
```

Task eligibility and owner-authored take: `/home/mesh-home/.mesh/chat.log:56254–56255`. The
follow-up `mesh-task dispatch` could not retry because the step was already active (`no open
current step to dispatch`); the original automatic dispatch failure remains recorded in the task
ledger.

## Disposition

Persistent Tailscale-routed egress and LAN visibility UNKNOWN remain known health findings. Current
external egress works. Peer relay details changed since the source warning and were recorded as
observed, not generalized. No routing, VPN, DNS, firewall, or other configuration changed. The
fresh `mesh-doctor` totals remain unverified because that run did not finish during this triage.
