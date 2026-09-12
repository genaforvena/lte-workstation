# Health warning triage — 2026-09-12

Task: `health-warning/71839be786b31e27711b/triage` (owner `health`).

## Finding

The warning's `2F/34W` count from 2026-09-10 is stale, not evidence that the extra warnings
cleared. The latest health-authored check in `~/.mesh/chat.log` is 2026-09-12T09:57:36Z and
records `2 FAIL/33 WARN`; the two known FAILs are unchanged: node egress uses `tailscale0`
and an exit node is configured (single-exit-node SPOF). It also records LAN presence as
UNKNOWN, egress to `1.1.1.1` through `tailscale0` table 52, and DNS for `api.anthropic.com`
as `160.79.104.10`.

Live checks around 2026-09-12T13:03Z confirm the same health boundary:

- `mesh-card` (live-refreshed 12:51Z) reports `default-egress: tailscale0`, exit-node
  `phaedra`, and exit-node-LAN `SWALLOWED`: `100.76.0.1` resolves via `tailscale0` table 52
  instead of the LAN link. The card explicitly notes outward probes can stay green through
  this fault.
- `mesh-doctor` began a live pass and showed the same two egress FAILs plus the microphone
  default-device WARN (capture works when explicitly selecting `plughw:1,0`). Its full pass
  did not finish within the observation window; this receipt does not claim a fresh total
  warning count.
- `mesh-lan-presence --nodes` reports only `192.168.8.0/24 UNKNOWN` and says the router is
  unreachable with no local address in that segment. This is a known vantage blind spot,
  not evidence that LAN hosts are down.
- `mesh-health` at 13:03Z: `mesh-home` and `phaedra` PASS; six fleet nodes OFFLINE, Redmi 10
  UNKNOWN(timeout), and `imac-rozalia` SSH authentication refused. `mesh-fleet-health`
  likewise shows six OFFLINE, one NO-SSHD, one UNKNOWN, plus `PATH: OK` with 2 direct peers.
- `mesh-reflex-health` reports 36 per-run reflexes fresh, while explicitly marking
  `lan-newdevice` and `wifi-link` organ-blind with state frozen since their last real reads.
  It also reports absent `kbd-activity`/`wifi-rf` organs and several overwrite-only values.
  A fresh reflex heartbeat therefore does not restore those data sources.
- The requested `mesh-dash --once check` returned zero bytes in this invocation; no pane
  rows can be inferred from that empty result.

## Disposition

The egress route/exit-node findings remain known, actionable substrate faults; the LAN
presence result remains UNKNOWN due to an unreachable router/segment, and the listed frozen
sensors remain known blindness. No substrate mutation was authorized by this triage row, so
none was attempted. A route repair needs a separately scoped substrate action under the
health charter's coordination protocol. Nothing here claims the fleet-wide warnings are
resolved.

## Evidence and limits

Observed live with `mesh-card`, `mesh-doctor`, `mesh-lan-presence --nodes`, `mesh-health`,
`mesh-fleet-health`, and `mesh-reflex-health` on 2026-09-12; historical check deltas were
read from `~/.mesh/chat.log`. The health task dispatch check exited 0 and the row was
claimed by `health`. The doctor run was incomplete, and the one-shot dash was empty, so
counts and pane detail beyond the cited prior check remain unverified.
