# Health warning triage — 2026-09-16

Task: `health-warning/5f75bbdf7b01f3e69285/triage`

Warning under review: the 2026-09-15 health roll-call reported `route:no`, no
active proposal, and a gap around iMac SSH authentication and stale/offline
peers.

## Evidence

- `mesh-health` at `2026-09-16T00:05:19Z`: `mesh-home`, `imac-rozalia`, and
  `phaedra` PASS; GL-MT3000 and Redmi reachable off-tailnet; `ilya`,
  `imozerov-Default-string`, `imozerov-IdeaPad-3-15IIL05`, and `rip` OFFLINE.
- `tailscale status --json` confirms those four offline states and their last
  seen times; `imac-rozalia` is online/active at `100.121.88.110`.
- `timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=5
  ilya@100.121.88.110 'printf imac-ssh-ok'` returned `imac-ssh-ok`.
- `tailscale ping --c 2 100.121.88.110` returned a pong from
  `imac-rozalia (100.121.88.110)` via `192.168.8.214` in 1 ms.
- `mesh-lan-health` at `2026-09-16T00:06:14Z`: TV UP, iMac UP, vacuum UP,
  MacBook DOWN.

## Disposition

The cited iMac SSH gap is cleared by live evidence. The four offline peers are
not safe to repair from this node without an available alternate path or
operator-owned device access; no substrate change is justified. `route:no` is
consistent with the retired/no-proposal state and does not identify a live
route fault. Keep the stale/offline peer condition as a known blind spot and
recheck when a peer has a real alternate path.

