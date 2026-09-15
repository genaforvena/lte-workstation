# Tracked tool link parity repair — 2026-09-12

Task: `repo-sync-followups-20260912/repair-tracked-tool-link-parity` (owner `genome`).

Repaired only these eight deployed entries under `/home/mesh-home/.local/bin/` as absolute
symlinks to their committed sources in `/home/mesh-home/lte-workstation/scripts/`:
`mesh-body-motion`, `mesh-device-churn`, `mesh-health`, `mesh-land`, `mesh-mind-recycle`,
`mesh-promises`, `mesh-stress`, and `mesh-travels`. Before replacement, for every name,
the deployed regular-file hash matched both the worktree source and `git show HEAD:<source>`.
After replacement, each `readlink` target was checked for exact equality with the absolute
source path, and SHA-256 through the source, deployed symlink, and committed blob matched.

`mesh-sync-tools --test` passed. The report-only `mesh-sync-tools` invocation returned 1, as
expected while other drift remains. Its fresh `~/.mesh/sync-tools.log` drift row no longer
contains any of the eight repaired names; it still reports unrelated drift including
`mesh-gpu-fan`, which is untracked and deliberately remains undeployed. The root checkout
also remains dirty (the sync log reports 917 uncommitted files). Global `--apply` was not run.

Resource decision: this was a local filesystem/link operation and needed no GPU or heavy-job
slot. I used the active `mesh-home` shell. Live `free -h` reported 17 GiB available RAM and
`df -h /home/mesh-home` reported 641 GiB available disk, so local CPU/filesystem capacity was
available; no remote execution was warranted. The online compute peer `phaedra` was visible
in the live Tailscale listing, but cross-node execution adds no value for this local deployment.

The requested `mesh-dash --once genome` invocation returned no stdout. No source files changed.
