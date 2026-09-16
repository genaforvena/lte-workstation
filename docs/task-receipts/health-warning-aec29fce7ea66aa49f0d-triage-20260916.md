# Health warning triage — 2026-09-16

Task: `health-warning/aec29fce7ea66aa49f0d/triage`

Warning under review: the 2026-09-15 roll-call reported `route:no`, no active
proposal, a b6 health triage already in progress, and gaps around iMac SSH
authentication and stale peers.

## Evidence

- `mesh-dash --once check` at `2026-09-16T00:09:50Z` reports the local node
  healthy but under high load (`load1=38.78/16c`), with reachability probes
  explicitly marked unreliable; egress is currently OK and all local organs
  are live.
- `mesh-fleet-health` at `2026-09-16T00:10:54Z` confirms `mesh-home` LOCAL,
  `imac-rozalia` reachable via its card, and `phaedra` reachable; it marks
  `ilya`, `imozerov-Default-string`, `imozerov-IdeaPad-3-15IIL05`, and `rip`
  as `UNKNOWN(load)`, not confirmed down. The path summary is `OK`, with
  `peers=8 direct=2 relay=0 offline=6`.
- The preceding health receipt
  `docs/task-receipts/health-warning-5f75bbdf7b01f3e69285-triage-20260916.md`
  records live iMac SSH and Tailscale/LAN verification; its four stale/offline
  peers remain without an alternate path.

## Disposition

The iMac SSH gap is already cleared by live evidence. Current high load makes
new reachability probes unreliable, and no safe substrate change is justified.
The stale/offline peers remain a known blind spot; recheck them when load
normalizes or an alternate path becomes available. `route:no` remains
consistent with the retired/no-proposal state rather than a demonstrated live
route fault.
