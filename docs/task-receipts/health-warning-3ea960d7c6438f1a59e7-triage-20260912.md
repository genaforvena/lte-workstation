# Health warning triage: `health-warning/3ea960d7c6438f1a59e7`

- Checked: 2026-09-12T11:47–11:50Z
- Owner: `health` on `mesh-home`
- Task: `health-warning/3ea960d7c6438f1a59e7/triage`

## Verdict

The warning's proposed route action is stale/retired (`route:no | PROPOSE none`); do not revive
that proposal. The underlying state is still current: the FIB sends public egress via
`tailscale0` table 52, the doctor reports the selected exit node as an egress SPOF, and LAN
presence remains UNKNOWN because this node has no local address on `192.168.8.0/24` and the
router is unreachable. External egress itself currently works (`anth=405`, `qfunc=PRESERVED`),
which does not clear the topology risk. No routing, VPN, firewall, or other configuration changed.

## Source and current evidence

- Original health roll-call: `/home/mesh-home/.mesh/chat.log:43729` (2026-09-10T00:01:15Z):
  `route:no | PROPOSE none (retired 2026-09-07T08:59:10Z) | CHANGED check-stream deltas recorded; no substrate mutation | GAP LAN UNKNOWN; exit-node SPOF remains`.
- Task ledger: `/home/mesh-home/.mesh/chat.log:56042` creates this exact task, owner `health`;
  `/home/mesh-home/.mesh/chat.log:56106–56107` records the owner-authored claim and active lease.
- One-shot live pane `rtk proxy mesh-dash --once check`, 2026-09-12T11:47:24–11:47:34Z, exit 0:

```text
egress tailscale0 | supervised 4UP/0DOWN | organs 13LIVE/0DARK
-- FLEET --
  10 nodes: 2 ssh · 0 lan · 8 down | PATH: DEGRADED OK peers=8 direct=1 relay=1…
  up: mesh-home(LOCAL vitals=OK up=ok) · phaedra(yes vitals=OK up=ok)
-- DOCTOR (this node, cached 13m): 2026-09-12T11:33:51Z FAIL=3 WARN=33
  FAIL egress rides tailscale0 (overlay/VPN) — should be LAN
  FAIL exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk
  FAIL smoke-test (real): mesh-claude-deepseek
  WARN mic DEFAULT device broken/busy (use -D plughw:N,M)
-- VPN (observe-only): friends@phaedra DEGRADED; egress now DERP udp=true, Helsinki, 34.3 ms
-- CPU/GPU: load1=11.68/16c; GPU HEALTHY, 9258/12288M, 0% util, 52C
-- organs: all LIVE (none DARK); 24 alarm, 26 stale, 88 quiet
```

The `mesh-doctor --quiet` live run at 11:48:16Z independently emitted the two relevant FAILs
and the microphone WARN, then emitted `WARN untimed peer-SSH — hangs on a dead peer:mesh-load-audit`.
It did not finish a full scan; I interrupted it after it remained hung. Its exit status was 130,
so I do not report a complete current FAIL/WARN total from that run.

```text
2026-09-12T11:48:16Z FAIL egress rides tailscale0 (overlay/VPN) — should be LAN
2026-09-12T11:48:16Z FAIL exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk
2026-09-12T11:48:16Z WARN mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-12T11:48:16Z WARN untimed peer-SSH — hangs on a dead peer:mesh-load-audit
```

The scoped direct probes were:

```text
$ rtk proxy ip route get 1.1.1.1
1.1.1.1 dev tailscale0 table 52 src 100.81.222.19 uid 1000
    cache

$ rtk proxy mesh-lan-presence --nodes
HOST                       IP              MAC                STATE    MESH-NODE
?                          192.168.8.0/24  ?                  UNKNOWN
mesh-lan-presence: router unreachable — UNKNOWN (no local address in 192.168.8.0/24 ; ARP cannot see that segment from here, and no known host answered ICMP)
exit=1

$ rtk proxy mesh-egress-health
<no output>
exit=0

$ cat ~/.mesh/.egress-state
OK
$ cat ~/.mesh/.egress-cause
OK qfunc=PRESERVED anth=405
```

The updated roll-call is `/home/mesh-home/.mesh/chat.log:56113` (2026-09-12T11:50:05Z). It
records the still-current egress-route and LAN visibility gaps, the functioning external egress
round trip, the incomplete doctor scan, and the absence of substrate changes.

## Disposition

The warning remains valid for egress path topology and LAN visibility; its old route proposal is
not actionable and stays retired. The external egress check is currently functional. The doctor
scan did not complete, and the LAN router remains unreachable, so no safe substrate repair is
supported by this evidence. Leave those systems untouched.
