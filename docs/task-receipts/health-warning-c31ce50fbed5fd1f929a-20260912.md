# Health warning triage: repeated peer-path change

Task: `health-warning/c31ce50fbed5fd1f929a/triage`

The Sep 10 roll-call reports an iMac relay-to-idle/offline change, a GL-MT3000 relay observation,
and unchanged egress/DNS. Current checks show that peer state is still fluctuating:

- The one-shot pane at 14:01:37Z reports supervised egress `4UP/0DOWN`, current probe `OK loss=0%`,
  but `PATH DEGRADED OK peers=8 direct=1 relay=1`; its fleet probe is flagged unreliable by
  current local-load sampling. `tailscale status` shows `phaedra` direct and active as exit node,
  `imac-rozalia` direct/active, and `gl-mt3000-1` with a relay entry marked offline/last seen
  85 days ago. These are dynamic observations, not a stable iMac relay repair. The configured
  phaedra exit-node SPOF remains.
- `mesh-lan-presence --nodes` at 14:01Z returns UNKNOWN because this host has no local address in
  `192.168.8.0/24`, cannot ARP that segment, and no known host answered ICMP. No route proposal is
  active; the old proposal remains retired.
- Current `dig` still returns `api.anthropic.com A 160.79.104.10`. `resolvectl status` in the
  preceding DNS check showed the link resolver addresses `213.87.2.89` and `217.66.16.35` plus
  Tailscale DNS; those server addresses were not the A answer. Their targeted timeouts and the
  successful tailnet/public resolver responses are documented in the prior DNS receipt.
- The pane's doctor summary remains cached from 13:35:58Z (`3F/34W`); a fresh full doctor result is
  still unavailable. The named microphone warning therefore remains unrefreshed.

Verdict: current egress probe passes, but traffic uses the configured exit node and the LAN remains
UNKNOWN. Peer path reports vary across samples. DNS A resolution is unchanged. No routing, VPN,
DNS, firewall, or audio setting was changed.

Verification: `mesh-dash --once check` at 14:01Z; `tailscale status`; `mesh-lan-presence --nodes`
(exit 1/UNKNOWN); and `dig +noall +answer A api.anthropic.com`.
