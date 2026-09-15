# Health warning triage: `health-warning/504c0323782bea4f8b13`

- Checked: `2026-09-12T21:28–21:30Z` on `mesh-home`
- Task: `health-warning/504c0323782bea4f8b13/triage`
- Owner: `health`
- Source alarm: watchdog on `phaedra`, `2026-09-12T21:21:48Z`, reporting
  `imac-rozalia` (`100.121.88.110`) unreachable, last-seen about 1 minute ago,
  `active=False`, and no LAN fallback.

## Finding

The task was still open and dispatch-eligible; the owner-authored take succeeded.
The offline classification remains supported, but the alarm's `active=False`
detail is not current. A fresh local Tailscale status sample reports
`Online=false`, `Active=true`, `Relay=hel`, and last seen at `21:17:13Z`; a
read-only `tailscale ping` timed out. The health pane reports zero LAN nodes and
warns that local load makes reachability probes unreliable. Local
`MESH_LAN_FALLBACK` contains no `imac-rozalia` entry, so this node has no
configured LAN candidate to test. The evidence supports tailnet unavailability
from this node, but does not establish the iMac's physical power state or
exclude a path/probe failure.

The current code agrees with that boundary: `scripts/mesh-health` checks only
configured LAN fallback candidates and renders `OFFLINE` if none answers
(lines 59–65, 207–229). `scripts/mesh-session-watchdog` describes this
`mesh-health` OFFLINE class as tailscaled unavailable plus no LAN fallback
(lines 599–604). The task is therefore correctly scoped as triage; no safe
network or remote-node change follows from this evidence.

No routing, DNS, firewall, VPN, Tailscale, or remote-node configuration was
changed.

## Evidence

- `mesh-task check dispatch health-warning/504c0323782bea4f8b13/triage health`
  exited 0; `MESH_TASK_ACTOR=health mesh-task take
  health-warning/504c0323782bea4f8b13 triage` recorded the owner-authored claim.
- `mesh-dash --once check` at `21:28:25Z`: 10-node summary includes
  `imac-rozalia` among down peers, zero LAN nodes, and the local-load probe
  warning.
- `tailscale status --json` filtered to `imac-rozalia`: `Online=false`,
  `Active=true`, `Relay=hel`, `LastSeen=2026-09-12T21:17:13.1Z`,
  `InEngine=true`.
- `tailscale ping --c 1 --timeout 5s imac-rozalia`: `no reply` / timed out.
- `/home/mesh-home/.mesh/nodes` configures LAN fallbacks only for
  `GL-MT3000` and `router`; no iMac fallback is configured here.
- Prior adjacent triage at
  `docs/task-receipts/health-warning-17e4f8cf4e7b0168179c-triage-20260912.md`
  also records the same visibility gap and the earlier `21:20Z` offline sample.

## Disposition

## Update: 2026-09-12T23:22Z

The later sample changes the classification from sustained unavailability to
intermittent reachability with relay fallback, while leaving the latest state
disputed. Witness reported a `mesh-home` Tailscale sample with
`Online=true`, `Relay=hel`. The path-watch tape records recovery from offline
to relay at `23:04:01Z`; Phaedra reported relay again at `23:14Z`. The same
tape records a transition back to offline at `23:19:01Z`. Its latest UDP
measurement is `udp=true` at `22:49:01Z`, which predates both transitions and
does not establish UDP health at the time of recovery.

A fresh read from `mesh-home` at `23:22Z` reports `Online=false`,
`Relay=hel`, and `LastSeen=2026-09-12T23:20:00.1Z`. This conflicts with the
witness's `Online=true` report, so the peer's present online state is not
settled. The evidence does show relay-path recovery between offline periods;
it still does not establish the iMac's physical state or the cause of the
flapping. No network state was changed. Keep this triage active for a fresh
repeat status sample and an updated path/UDP reading before assigning a stable
current-state verdict.

## Original disposition (superseded)

The initial 21:28–21:30Z sample supported tailnet unavailability from this
node, with physical iMac state and alternate-path availability unknown. That
single-sample conclusion was superseded by the 23:04Z relay recovery and
23:19Z offline transition above.

## Repeat sample: 2026-09-12T23:33–23:34Z

The fresh `mesh-home` Tailscale view still reports `imac-rozalia` as
`Online=false`, `Active=true`, `Relay=hel`, `InEngine=true`, with
`LastSeen=23:18:30.1Z` and no handshake. `tailscale ping --c 1 --timeout 5s`
timed out. The local path-watch snapshot at `23:29:01Z` classifies it
`offline`; its fleet count is `direct=1 relay=0 offline=7`. The latest tape
transition remains `23:19:01Z path ... mode=offline was=relay`, so there is no
new peer-path recovery in the tape.

At `23:33:49Z`, local `tailscale netcheck` reports `UDP=true`, public IPv4
available, and Helsinki as nearest DERP. This establishes that local UDP is
available now, but not that the iMac is reachable or that its offline state is
caused by this node's UDP path. The new local status and ping agree on current
unreachability; the earlier witness report still conflicts with them. Physical
power state and the reason for the intermittent peer reports remain unknown.
No network state was changed; keep the triage active pending the next peer
status/path sample.

- Repeat evidence: `tailscale status --json` filtered to the peer;
  `tailscale ping --c 1 --timeout 5s imac-rozalia`; `tailscale netcheck`;
  `mesh-path-watch --status`; and the tail of `~/.mesh/path-watch.log`.

## Follow-up sample: 2026-09-12T23:48Z

The repeat check after the next path-watch pass still shows `imac-rozalia`
offline from `mesh-home`. At `23:48Z`, `tailscale status --json` reports
`Online=false`, `Active=false`, `Relay=hel`, `InEngine=true`,
`LastSeen=23:18:30.1Z`, and no handshake; `tailscale ping` timed out. The
`23:44:01Z` path-watch snapshot reports `imac-rozalia=offline` (fleet count
`direct=1 relay=0 offline=7`). At `23:48:42Z`, local `tailscale netcheck`
still reports `UDP=true`, public IPv4, and Helsinki as nearest DERP. The
path-watch tape has no newer transition than the `23:19:01Z` offline record.

This confirms local UDP availability alongside a continued offline peer view;
it does not establish the iMac's physical state or the cause of the missing
peer path. Keep the triage active and repeat status/path/UDP after the next
path-watch pass, around `23:59Z`; no network state was changed.

## Final disposition: 2026-09-12T23:48Z

The requested repeat after the 23:34Z sample is complete. The 23:44Z
path-watch snapshot still classifies the peer offline, and the 23:48Z local
status and ping agree; local UDP is available. The alarm is therefore
confirmed as `UNREACHABLE from mesh-home` at this sample. The remaining
blindness is the iMac's physical/power state and the cause of its intermittent
tailnet reports; this node has no configured LAN fallback for that peer. No
safe network or remote-node change follows from this evidence. Triage is
complete with that limitation recorded; no network state was changed.
