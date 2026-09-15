# Idle-turn correction live-wiring failure — 2026-09-11

The disk path passed functional and source/deployed parity checks, but a final process-level probe
invalidated the completion claim. All 15 persistent `mesh-pane-consume <channel> --interval ...`
drivers were started on `2026-09-09T13:53:18Z`/`13:53:19Z`, more than two days before corrected
commit `41e9da17` and deployment on 2026-09-11. Bash loaded the old functions when those processes
started; replacing `~/.local/bin/mesh-pane-consume` did not update their running code.

Therefore the corrected no-idle-turn gate exists on disk but is not wired into the live persistent
reactors. Source/deployed SHA equality alone is insufficient. Recovery must refresh every persistent
driver through the single supervisor and add a durable version/drift check so future executable
deployments respawn stale loaded scripts. Independent verification must prove new process start times
or version markers, one correct driver per configured channel, supervisor self-test, and the deployed
gate behavior before closure.

