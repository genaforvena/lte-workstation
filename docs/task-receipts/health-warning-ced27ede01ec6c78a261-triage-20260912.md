# Health-warning triage: `health-warning/ced27ede01ec6c78a261`

- Checked: 2026-09-12T12:04–12:06Z
- Owner: `health` on `mesh-home`
- Task: `health-warning/ced27ede01ec6c78a261/triage`

## Verdict

The warning is historical and its peer details are no longer current. The current live checks still
confirm egress via `tailscale0`/table 52 and LAN presence UNKNOWN, while the external egress
round-trip succeeds. `mesh-health` now passes both `mesh-home` and `phaedra`; `imac-rozalia` is
Tailscale `Online=true` but inactive and SSH authentication is refused. Current Tailscale JSON
reports `phaedra` as the active exit node with relay `tor`, not direct. The check pane's peer
summary and this per-peer relay field were sampled 36 seconds apart and do not agree on relay
counts, so I preserve both raw observations rather than infer a stable path classification.

The 2F/34W delta in the old warning is not freshly verified: the current check pane carries a
30-minute-old doctor result from 11:33:51Z (3F/33W). No new doctor total is claimed. No routing,
VPN, DNS, firewall, or other configuration changed.

## Evidence

Original message `/home/mesh-home/.mesh/chat.log:43924` (2026-09-10T02:00:35Z) says the doctor
changed from 3F/33W to 2F/34W, LAN remained UNKNOWN, imac changed from offline to idle/offline,
phaedra was active/direct exit, egress stayed via `tailscale0`, and DNS A was unchanged. This task
was open and exact-owner eligible before the health claim (`~/.mesh/chat.log:56185`); the owner-
authored claim is at `~/.mesh/chat.log:56190`.

`mesh-dash --once check` (2026-09-12T12:04:38–12:04:40Z, exit 0):

```text
egress tailscale0 | supervised 4UP/0DOWN | organs 15LIVE/0DARK
10 nodes: 1 ssh · 0 lan · 9 down | PATH: OK peers=8 direct=2 relay=0 offline=6
up: mesh-home
DOCTOR (cached 30m): 2026-09-12T11:33:51Z FAIL=3 WARN=33
  egress rides tailscale0 (overlay/VPN) — should be LAN
  exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk
  smoke-test FAIL (real): mesh-claude-deepseek
egress now: OK loss=0% avg=139.174ms mdev=0.605ms
```

Current live commands and exact outputs:

```text
$ rtk proxy mesh-health
=== mesh-health 2026-09-12T12:05:14Z ===
PASS  mesh-home                        100.81.222.19 (self)
OFFLINE GL-MT3000                        100.105.241.84 (tailnet: last-seen 85d ago, active=True)
OFFLINE Redmi 10                         100.103.99.16 (tailnet: last-seen 9d ago, active=True)
OFFLINE ilya                             100.107.198.111 (tailnet: last-seen 23d ago, active=True)
SKIP  imac-rozalia                     100.121.88.110 — SSH authentication refused
OFFLINE imozerov-Default-string          100.125.157.75 (tailnet: last-seen 59d ago, active=True)
OFFLINE imozerov-IdeaPad-3-15IIL05       100.73.170.56 (tailnet: last-seen 13d ago, active=True)
PASS  phaedra                          100.94.116.17
OFFLINE rip                              100.116.125.102 (tailnet: last-seen 9d ago, active=False)

$ rtk proxy mesh-lan-presence --nodes
HOST                       IP              MAC                STATE    MESH-NODE
?                          192.168.8.0/24  ?                  UNKNOWN
mesh-lan-presence: router unreachable — UNKNOWN (no local address in 192.168.8.0/24 ; ARP cannot see that segment from here, and no known host answered ICMP)
exit=1

$ rtk proxy ip route get 1.1.1.1
1.1.1.1 dev tailscale0 table 52 src 100.81.222.19 uid 1000
    cache

$ rtk proxy tailscale status --json | jq -c '.Peer[] | select(.HostName=="imac-rozalia" or .HostName=="phaedra") | {HostName,Online,Active,Relay,LastSeen,ExitNode}'
{"HostName":"phaedra","Online":true,"Active":true,"Relay":"tor","LastSeen":"0001-01-01T00:00:00Z","ExitNode":true}
{"HostName":"imac-rozalia","Online":true,"Active":false,"Relay":"hel","LastSeen":"0001-01-01T00:00:00Z","ExitNode":false}

$ rtk proxy getent ahostsv4 api.anthropic.com
160.79.104.10   STREAM api.anthropic.com
160.79.104.10   DGRAM
160.79.104.10   RAW

$ rtk proxy mesh-egress-health
<no output>
exit=0
$ cat ~/.mesh/.egress-state
OK
$ cat ~/.mesh/.egress-cause
OK qfunc=PRESERVED anth=405
```

The updated roll-call is `/home/mesh-home/.mesh/chat.log:56207` (2026-09-12T12:06:10Z).

## Disposition

The old 2F/34W delta and peer-state transition are not a current doctor/peer verdict. Current
evidence confirms the persistent overlay egress path and LAN visibility gap; current external
egress works, `phaedra` is reachable by SSH, and the imac SSH failure is authentication-related.
Keep the retired route proposal retired and make no substrate change without a viable LAN path and
single-writer evidence.
