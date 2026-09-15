# Health-warning triage: `health-warning/255bc20b04fcab5de704`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/255bc20b04fcab5de704/triage`  

## Claim verification

The exact owner-scoped dispatch row was checked and claimed:

```text
mesh-task check dispatch health-warning/255bc20b04fcab5de704/triage health
exit=0
MESH_TASK_ACTOR=health mesh-task take health-warning/255bc20b04fcab5de704 triage
claimed health-warning/255bc20b04fcab5de704/triage
```

## Warning and retained tape

The warning reported one `imac-rozalia` direct→DERP transition. The retained
`~/.mesh/path-watch.log` shows repeated direct/relay crossings through the
observation period, not loss of the peer. At 22:24Z it recorded
`imac-rozalia mode=direct was=relay`; the same tape records `netweather udp=true`
at 21:54Z with DERP Helsinki latency 36.8 ms.

## Fresh independent read

At 2026-09-11T22:30:10Z:

```text
mesh-path-watch: QUIET (peers=8 direct=2 relay=0 offline=6 ... imac-rozalia=direct ...)
UDP: true; IPv4: yes; Nearest DERP: Helsinki; hel: 34.6ms
pong from imac-rozalia (100.121.88.110) via 5.227.25.156:55351 in 4ms
tailscale status: imac-rozalia active; direct 5.227.25.156:55351
```

No routing, DNS, firewall, WireGuard, or Tailscale mutation was made. The
current path is direct and UDP is healthy; this warning is a recovered transient
relay crossing. The remaining fleet offline count (6 peers) is separate evidence,
not caused by this row.

## Disposition

Closed as recovered transient direct↔relay churn. LTE/carrier NAT variability is
the known limitation; a local substrate repair is not justified by this evidence.
