# Health-warning triage: `health-warning/64ffcf315d889290dcc2`

- Checked: `2026-09-13T11:47–11:50Z` on `mesh-home`
- Task: `health-warning/64ffcf315d889290dcc2/triage`
- Source warning: `watchdog@phaedra`, `2026-09-13T04:11:42Z`, reported
  `mesh-home` unreachable at `100.81.222.19`, tailnet last-seen 11m earlier.

## Finding

The warning describes the outage preceding the current boot. The reboot/rejoin
record at `~/.mesh/rejoin-mesh-home.log` timestamps the previous shutdown at
`03:55:38Z`, the new boot at `11:35:50Z`, and records `mesh-home` rejoining at
`11:39:43Z` after 7h40m down. Its connectivity snapshot at `11:39:43Z` says
`mesh=up`; the board independently records `selfcare@mesh-home` changing to
`mesh=up` at `11:39:43Z`. The prior-boot journal contains a kernel page fault
at shutdown time, but this evidence does not establish the reboot cause.

At triage time, `tailscale status --json` reported this node's `Online=true`
with `tag:lte-node`; `mesh-dash --once check` showed mesh-home in the up list,
and `mesh-supervise --status` showed 4/4 supervised services UP. This is a
recovered historical alert, not a current unreachable state. No substrate
state was changed.

## Evidence

- `/home/mesh-home/.mesh/rejoin-mesh-home.log`: boot-id transition
  `76234e1e -> 43ff5103`, shutdown/boot times, and rejoin connectivity snapshot.
- `/home/mesh-home/.mesh/chat.log`: `watchdog@phaedra` alert at `04:11:42Z`,
  `selfcare@mesh-home` recovery at `11:39:43Z`, and this node's current board
  activity after reboot.
- `mesh-dash --once check` at `11:47:24Z`: `mesh-home(LOCAL vitals=OK up=ok)`.
- `tailscale status --json`: self `Online=true`, tagged `tag:lte-node`.
- `mesh-supervise --status`: `snapshot`, `selfcare`, `dram-bw-sampler`, and
  `devcd-catch` all UP.

## Disposition

Close as stale/resolved by reboot and rejoin. The cause of the preceding
outage remains undetermined; reopen if a fresh reachability failure appears.
