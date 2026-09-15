# Health-warning triage: `health-warning/1b5cd081c6b28386a347`

- Checked: `2026-09-13T01:18–01:20Z` on `mesh-home`
- Owner: `health`
- Task: `health-warning/1b5cd081c6b28386a347/triage`
- Source: watchdog roll-up at `2026-09-13T01:16:42Z`, chronic signature
  `35f22fafd26a`, same text `100.121.88.110 — SSH unreachable`; measured
  recurrence window `652162s` (`n=18`), gap `136540s`, and 3 suppressed
  identical cycles since the preceding board line.

## Finding

The task was still open and dispatch-eligible when checked; it was claimed by
`health`. This is not already resolved: the newest check pane lists
`imac-rozalia` unreachable, and fresh checks confirm the peer is currently
unreachable from `mesh-home`. Tailscale status reports it offline (last seen
about one minute earlier, relay metadata `hel`); two Tailscale pings timed out;
batch SSH to `100.121.88.110` timed out connecting to port 22; and the latest
`mesh-path-watch --once` classifies it offline. The older
`health-warning/504c0323782bea4f8b13/triage` receipt documents the preceding
episode and a later relay recovery, so the recurrence is intermittent, not a
new local substrate fault or evidence that this episode cleared.

The classifier boundary matches the current node configuration: `mesh-health`
uses host-keyed `MESH_LAN_FALLBACK` entries when tailnet reachability fails
(`scripts/mesh-health:207-229`); the current config names only `GL-MT3000` and
`router`, not this Mac (`~/.mesh/nodes:127`). There is no alternate LAN
candidate for this host. The evidence supports “unreachable from mesh-home”;
it cannot establish the Mac's physical power state or why its tailnet path
disappeared. That physical state and root cause are the known blindness. No
route, DNS, firewall, VPN, Tailscale, or remote-node configuration was changed.

## Evidence

- `mesh-task check dispatch health-warning/1b5cd081c6b28386a347/triage health`
  returned eligible; `mesh-task take health-warning/1b5cd081c6b28386a347
  triage` claimed the open task.
- `mesh-dash --once check` at `01:18Z`: fleet includes `imac-rozalia` as
  unreachable/down; local egress is reported OK.
- `tailscale status`: `imac-rozalia` is offline, last seen about 1m ago,
  relay metadata `hel`.
- `tailscale ping --c 2 --timeout 5s imac-rozalia`: both probes timed out;
  no reply.
- `timeout 6 ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`:
  port 22 connection timed out.
- `mesh-path-watch --once`: `peers=8 direct=1 relay=0 offline=7`, with
  `imac-rozalia=offline`.
- Current `/home/mesh-home/.mesh/nodes` has no iMac `MESH_LAN_FALLBACK`;
  the current classifier reads these entries in `scripts/mesh-health`.
- Prior episode: `docs/task-receipts/health-warning-504c0323782bea4f8b13-triage-20260912.md`.

## Disposition

Close this triage as a confirmed, recurring reachability fault with the
physical state and cause explicitly unknown. No safe corrective action is
available from this node while the Mac is unreachable and has no configured
LAN path. Recheck from the health pane on the next wake; if the peer returns,
test SSH separately before treating recovery as complete.
