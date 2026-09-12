# Health-warning triage: `health-warning/915a3ef9522ed7288174`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/915a3ef9522ed7288174/triage`  
Priority: 50

## Claim verification

The exact queue head was checked and claimed as owner `health`:

```text
mesh-task check dispatch health-warning/915a3ef9522ed7288174/triage health
exit=0
mesh-task take health-warning/915a3ef9522ed7288174 triage
status=active
```

## Warning and path-tape evidence

The warning was emitted by `path-watch@mesh-home` for the 2026-09-11T19:04:01Z
pass: one peer, `imac-rozalia`, fell from direct to DERP relay. The source names
the conditional root cause correctly: if local UDP had gone false, the
`path-udp-blocked` observation would explain it.

The retained `/home/mesh-home/.mesh/path-watch.log` shows this is not a persistent
loss of reachability. Around the warning, `imac-rozalia` alternated between
direct and relay, while the periodic network-weather samples remained
`udp=true` (for example 19:54Z, DERP Helsinki, 37.2 ms). The tape then recorded
`imac-rozalia mode=direct was=relay` at 20:14:01Z.

## Current independent path evidence

Fresh reads at 2026-09-11T20:15Z:

```text
mesh-path-watch
QUIET (peers=8 direct=2 relay=0 offline=6 ... imac-rozalia=direct ... phaedra=direct)

tailscale netcheck
UDP: true
IPv4: yes, 5.227.42.156:60832
Nearest DERP: Helsinki; hel latency 33 ms

tailscale ping --c 3 100.121.88.110
pong from imac-rozalia (100.121.88.110) via 5.227.25.156:55351 in 7ms

tailscale status
imac-rozalia ... active; direct 5.227.25.156:55351
```

The local Tailscale daemon is running, the peer is online, and the current path
is direct. No routing, DNS, firewall, WireGuard, or Tailscale mutation was made.

## Disposition

Settled as a recovered transient direct→relay observation, not a current outage.
The remaining direct↔relay churn is consistent with the documented LTE/carrier
NAT path instability and is a known limitation rather than evidence for a local
repair. The path-watch alarm is therefore closed with current path evidence;
leave the lower-priority delivery rows for the next queue turns.
