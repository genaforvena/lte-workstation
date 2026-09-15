# Health warning triage: repeated DNS and peer-path roll-call

Task: `health-warning/04128aaf3f7cc073b0d9/triage`

The Sep 10 roll-call describes DNS values `213.87.2.89` / `217.66.16.35` changing to
`160.79.104.10`. These are different kinds of values: the first pair are current configured DNS
server addresses; `160.79.104.10` is the current A answer for `api.anthropic.com`.

Current `resolvectl status` is unchanged from the prior DNS receipt: `enp42s0` lists
`213.87.2.89` and `217.66.16.35`, while `tailscale0` lists `100.100.100.100` and
`fd7a:115c:a1e0::53` with `~.` routing all names there. Current `dig +noall +answer A
api.anthropic.com` returns `160.79.104.10`, matching both the prior A observation and the earlier
tailnet/public resolver comparisons. The prior receipt documents direct queries to the physical
link resolvers timing out over the Tailscale route; this task supplied no evidence that those
resolver addresses or the A answer have changed again.

The latest check pane at 13:59:35Z reports egress `OK loss=0%`, supervised `4UP/0DOWN`, and path
`OK peers=8 direct=2 relay=0`. Live `tailscale status` shows `phaedra` direct and active as the
exit node and `imac-rozalia` direct/active; the pane sees the iMac's ICMP response but no SSH. The
exit-node SPOF remains. The pane still reports 0 LAN nodes; the direct LAN probe at 13:57Z returned
UNKNOWN for lack of an address in `192.168.8.0/24`, ARP visibility, or a known-host ICMP response.
Doctor data is cached from 13:35:58Z (`3F/34W`), not a fresh completed run.

Verdict: current egress and peer paths are healthy in this sample, but they do not clear the exit
node dependency or LAN visibility gap. The reported DNS change compares resolver addresses to a
record answer; the current answer remains `160.79.104.10`. The prior route proposal remains
retired. No DNS, route, VPN, firewall, or other substrate state was changed.

Verification: `mesh-dash --once check` at 13:59Z; `tailscale status`; `resolvectl status`;
`dig +noall +answer A api.anthropic.com`; and the 13:57Z `mesh-lan-presence --nodes` result
(exit 1/UNKNOWN), with the resolver-timeout probes documented in
`health-warning-20d10f9590203ff1e74f-20260912.md`.
