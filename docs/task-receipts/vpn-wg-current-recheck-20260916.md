# VPN WG current recheck — 2026-09-16

## Scope

Read-only recheck of the fresh dashboard observation at 2026-09-16T05:13:10Z. No routing,
firewall, DNS, WireGuard, or service mutation was performed. This task was kept local because
the VPN charter makes diagnosis read-only and substrate single-writer; no independent mutation
was safe to delegate.

## Evidence

- `mesh-dash --once vpn` at `2026-09-16T05:13:10Z`: this node has no consumer tunnel by design;
  four Tailscale machines are online, including mesh-home and phaedra; end-to-end port 8444
  PASS; phaedra reports `SS:up trojan:up wg:up`, 16 WG peers, newest handshake age 1461752s,
  12 stale and 4 never; cached SS state is stale/UNKNOWN.
- `mesh-vpn-health --edge` at `2026-09-16T05:18:36Z`: `SS:up trojan:up wg:up`, newest WG
  handshake age `1462258s`, `0 active / 0 idle / 12 stale / 4 never`.
- `tailscale status --json` at `2026-09-16T05:18:36Z`: mesh-home `Online:true`; phaedra
  `Online:true`; phaedra's Tailscale last handshake `2026-09-16T05:17:00.234293016Z`.
- Bounded `ssh -o BatchMode=yes -o ConnectTimeout=5 phaedra` at `2026-09-16T05:18:45Z`
  exited 0. `wg0` read succeeded and returned 16 peers: 4 latest-handshake values were 0;
  the nonzero values were dated 2026-06-19 through 2026-08-30, all older than the observation.
  `systemctl is-active wg-quick@wg0` returned `active`; the remote running-service listing
  included `ss-op.service` and `trojan.service`.

## Verdict

The moved layer is **WireGuard peer activity**, not the server tunnel or Tailscale reachability:
wg0 and the proxy services are up, phaedra is Tailscale-online, and the end-to-end tunnel passes,
but no provisioned WG client has a fresh handshake. Classify client use as **IDLE / UNPROVEN**;
do not claim client outage or restart a working service. SS remains **UNKNOWN/stale** from its
cached consumer state.

## Verification

Commands and exit results are recorded above: dashboard one-shot succeeded; edge health returned
the degraded reading; Tailscale JSON parsed; bounded SSH/WG/service read exited `0`. Artifact is
the acceptance receipt for `vpn-wg-current-recheck-20260916/classify-current-wg-staleness`.
