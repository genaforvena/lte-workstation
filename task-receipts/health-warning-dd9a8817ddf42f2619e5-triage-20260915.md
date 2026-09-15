# Health-warning triage: `mesh-capcheck-881539.scope`

- Checked: `2026-09-15 UTC`
- Owner: `health / mesh-home`
- Task: `health-warning/dd9a8817ddf42f2619e5/triage`
- Source: `journal-watch@phaedra`, `2026-09-15T06:15:19Z`

## Verdict

The warning is an expected artifact of the cgroup-capability probe, not a
host-memory incident or a broken systemd target. The source tape names the
128 MiB `mesh-capcheck` probe and its transient scope. Read-only inspection of
phaedra's current-boot journal in the surrounding window shows the same probe
starting successfully and then being killed by the kernel at the deliberate
32 MiB cgroup ceiling; the adjacent 256 MiB `mesh-caphog` probe is likewise
killed at its deliberate 64 MiB ceiling. The journal also shows ordinary
`mesh-heavy-*` scopes continuing to start around these events.

The original `Failed to start` wording is therefore a lossy health-watch
classification of the transient scope's non-zero/`oom-kill` result. It does
not establish a systemd start-path failure. No routing, DNS, firewall, VPN,
Tailscale, systemd, or probe configuration was changed.

## Evidence

- `/home/mesh-home/.mesh/chat.log:68128-68130` records the warning, dispatch,
  and exact task instructions; `:68137-68138` records the owner-authored take.
- `/home/mesh-home/.mesh/journal-watch.log` on phaedra records the source at
  `2026-09-15T06:15:02Z` as `new=yes`, with the exact 128 MiB probe command.
- Read-only `ssh phaedra-direct` journal capture for
  `2026-09-15T06:10:00Z`–`06:20:00Z` shows repeated successful starts of
  `mesh-capcheck-*.scope`, followed by `memory: usage 32768kB, limit
  32768kB`, `Memory cgroup out of memory`, victim `mesh-capcheck`, and
  `Failed with result 'oom-kill'`; the same window shows `mesh-caphog` at a
  65536kB limit and normal `mesh-heavy-*` starts.
- `mesh-hw-health` at `2026-09-15T21:03Z`: disk SMART PASSED, wear 2%,
  critical warning 0x00, spare 100%; this is not a complete fleet-health
  verdict, but provides current local hardware evidence.
- Local `journalctl -b 0 -p err --grep='Failed to start mesh-capcheck'`
  returned `-- No entries --`; the current boot's local capcheck OOM lines
  are the expected probe family.

## Disposition

Close as an expected synthetic cgroup-limit result. Keep the health-watch
classification limitation explicit: `oom-kill` after a successful transient
scope start is not equivalent to `Failed to start`. Reopen if a capcheck scope
fails before starting, if the cap probe stops proving the intended ceiling, or
if unrelated OOM victims appear outside the named probe commands.

## Verification

- `mesh-dash --once check` — one-shot live pane consumed.
- `mesh-task check dispatch health-warning/dd9a8817ddf42f2619e5/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/dd9a8817ddf42f2619e5 triage`
  — exact owner claim recorded.
