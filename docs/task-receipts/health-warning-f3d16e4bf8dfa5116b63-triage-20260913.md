# Health-warning triage: `health-warning/f3d16e4bf8dfa5116b63`

- Checked: `2026-09-13T11:41–11:43Z` on `mesh-home`
- Task: `health-warning/f3d16e4bf8dfa5116b63/triage`
- Source: `watchdog@phaedra`, `2026-09-13T07:21:52Z`; chronic signature
  `35f22fafd26a`, gap `159012s`, recurrence window `351600s` (`n=21`), with
  3 suppressed identical cycles since the preceding board line.

## Finding

The exact task was open in the task ledger and became active under `health`;
it is not an already-closed duplicate. A prior receipt for the same signature
at `01:18Z` documented the earlier offline episode, so this roll-up is a later
recurrence and its suppression count remains meaningful.

The current check pane and a fresh Tailscale status agree that
`imac-rozalia` is offline from `mesh-home`: the pane reports it among 8 down
peers and `PATH: ... offline=7`; Tailscale reports `Online=false`,
`Active=false`, last seen `2026-09-13T11:23:25Z`. A fresh batch SSH attempt to
`100.121.88.110` timed out on port 22. This supports the warning's present
reachability verdict. It does not establish the Mac's physical/power state or
why its tailnet path disappeared.

Current `scripts/mesh-health` uses configured LAN fallback candidates if the
tailnet path is unavailable. `/home/mesh-home/.mesh/nodes` configures candidates
for `GL-MT3000` and `router`, but none for `imac-rozalia`; consequently there
is no alternate LAN observation from this node. The classifier and its
visibility limit match the current configuration. No routing, DNS, firewall,
VPN, Tailscale, or remote-node configuration was changed.

## Evidence

- `mesh-chat --history f3d16e4bf8dfa5116b63 30`: ledger reports the exact
  chain open at `11:40:17Z`; subsequent ledger rows show dispatch failures,
  and `mesh-task status` reports the step active under `health`.
- `mesh-dash --once check` at `11:41:43Z`: 10 nodes, 2 SSH, 8 down; path
  `direct=1 relay=0 offline=7`; `imac-rozalia(OFF)`.
- `tailscale status --json` filtered to the peer: `Online=false`,
  `Active=false`, `LastSeen=2026-09-13T11:23:25.1Z`.
- `timeout 6 ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`:
  timed out connecting to port 22 (exit 255).
- `scripts/mesh-health` documents host-keyed `MESH_LAN_FALLBACK` candidates;
  `/home/mesh-home/.mesh/nodes` has no iMac candidate.
- Earlier episode: `docs/task-receipts/health-warning-1b5cd081c6b28386a347-triage-20260913.md`.

## Disposition

Close as a confirmed recurring SSH/tailnet reachability failure from
`mesh-home`; physical state and root cause remain unknown. The alarm is not
cleared, and no safe corrective action is available from this node without a
reachable peer or configured LAN path. Reassess from the health pane on the
next wake; if the peer returns, test SSH separately before recording recovery.
