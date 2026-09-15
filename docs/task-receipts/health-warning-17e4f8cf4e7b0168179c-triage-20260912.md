# Health warning triage: `health-warning/17e4f8cf4e7b0168179c`

Checked: 2026-09-12 21:20–21:22 UTC on `mesh-home`  
Task: `health-warning/17e4f8cf4e7b0168179c/triage`  
Owner: `health`

## Finding

The watchdog's 21:19:22Z alarm is consistent with a brief loss of the iMac's
tailnet availability: a read-only `tailscale status --json` sample at 21:20Z
reported `Online=false`, `Active=true`, relay `hel`, and `LastSeen=21:20:00.1Z`
for `imac-rozalia` (`100.121.88.110`). This confirms a recent tailnet observation
followed by an offline status; it does not establish that the iMac itself is
powered off or identify the cause. The live health pane reports zero LAN nodes
and warns that local load makes reachability probes unreliable, so this node
cannot distinguish an iMac outage from a path/probe failure or verify LAN
fallback. Treat the physical state and LAN path as unknown until a reliable
later sample changes that evidence.

No routing, DNS, firewall, VPN, Tailscale, or remote-node configuration was
changed. This triage records the alarm as a current tailnet-availability
failure with LAN reachability as a known visibility gap.

## Evidence

- `mesh-dash --once check` at 21:20:41Z: fleet summary `10 nodes: 2 ssh · 0 lan ·
  8 down`; `LOCAL LOAD HIGH — reachability probe UNRELIABLE`; egress remains on
  `tailscale0` and the displayed doctor result is cached from 20:32:36Z.
- `/home/mesh-home/.mesh/chat.log:58283`: exact watchdog alarm at 21:19:22Z.
- Read-only `tailscale status --json` sample at 21:20Z, filtered to
  `imac-rozalia`: `Online=false`, `Active=true`, `Relay=hel`,
  `LastSeen=2026-09-12T21:20:00.1Z`, `ExitNode=false`.
- Dispatch validation `mesh-task check dispatch health-warning/17e4f8cf4e7b0168179c/triage health`
  exited 0; owner-authored take recorded at
  `/home/mesh-home/.mesh/chat.log:58289`.

## Disposition

Close this alarm's triage as tailnet unavailability observed, root cause and
physical iMac state unknown, and LAN fallback unverified from this node. No
substrate action is safe from the current evidence. Reassess on a later reliable
pane sample or a fresh path/owner observation.
