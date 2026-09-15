# Health warning triage: DNS delta, egress policy, LAN visibility

Task: `health-warning/dc221f87143bc683b504/triage`  
Source warning: 2026-09-12T06:47:08Z check-stream delta

## Current evidence at 2026-09-14 19:47Z

- The DNS observation is reproducible but not an outage. `getent ahostsv4 api.anthropic.com` and
  `resolvectl query` return `160.79.104.10`; direct queries to both `1.1.1.1` and `8.8.8.8` also
  return `160.79.104.10`. Cloudflare's AAAA answer is `2607:6bc0::10`. A credential-free
  `curl -sSI https://api.anthropic.com` completed TLS and returned HTTP/2 404, confirming the
  hostname and path are reachable; a 404 at the API root is not interpreted as an API request
  failure. This answer differs from the 2026-09-11 recorded values but is consistent across the
  current system and two public recursive resolvers.
- Public egress still uses `tailscale0 table 52` for `1.1.1.1`, as declared for this node's
  configured Phaedra exit-node consumer role. The fresh 19:35Z dashboard doctor cache reports
  `FAIL=0 WARN=33`; the completed role-aware policy receipt explains why the intentional exit-node
  dependency is not itself a doctor failure.
- The prior live `mesh-doctor --comprehensive` stall is historical. Its final count remains
  unavailable, and I did not repeat the broad comprehensive run for this DNS-only delta.
- Inward LAN/router presence remains a known `UNKNOWN`: `mesh-lan-presence --nodes` exits 1 because
  there is no local address in `192.168.8.0/24`, ARP cannot see that segment, and no known host
  answers ICMP. The current local exit-node-gateway route is separately healthy; the unknown
  presence state was already documented by the prior health triage and does not imply DNS or
  egress failure.

## Disposition

The recorded DNS answer changed since the older observation, but current system and public
recursive lookups agree and the API hostname completes TLS. Egress routing is intentional for the
configured consumer policy, the current doctor cache has zero failures, and the separate LAN
presence limit is already named. No DNS, route, rule, firewall, VPN, or service state was changed.
This warning is investigated and complete; retain LAN/router presence as an explicit blind and
rerun a comprehensive doctor only under its own bounded task if a fresh signal warrants it.

## Verification

- `getent ahostsv4 api.anthropic.com`: `160.79.104.10`.
- `resolvectl query api.anthropic.com`: `160.79.104.10`, `2607:6bc0::10`.
- `dig @1.1.1.1 A api.anthropic.com` and `dig @8.8.8.8 A api.anthropic.com`: both
  `160.79.104.10`; `dig @1.1.1.1 AAAA` returned `2607:6bc0::10`.
- Credential-free `curl -sSI --max-time 12 https://api.anthropic.com`: HTTP/2 404 after TLS.
- `ip -4 route get 1.1.1.1`: `dev tailscale0 table 52`; 19:35Z pane doctor cache: FAIL=0.
- Read the role-aware egress policy and live egress recheck receipts; the latter reports the
  intended public egress path and independent healthy local gateway route.
- `mesh-lan-presence --nodes`: exit 1, `UNKNOWN` with the documented absent-segment visibility
  limits.
