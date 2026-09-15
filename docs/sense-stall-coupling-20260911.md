# New sense: CPU × memory stall coupling — 2026-09-11

Added `scripts/mesh-stall-coupling`, an on-demand relation over the live kernel files
`/proc/pressure/cpu` and `/proc/pressure/memory`. `COUPLED` is emitted only when both
`some.avg10` axes exceed their thresholds; one-sided pressure remains `CPU_ONLY` or
`MEMORY_ONLY`, and missing/malformed input exits 2 as `UNKNOWN`.

The source is executable and declares `orphan-ok` because it has no scheduled consumer.
The standard local command link is installed at `~/.local/bin/mesh-stall-coupling`.
No state file is written, so no change-gated liveness touch is applicable.

## Verification

- `bash tests/test-mesh-stall-coupling.sh` — PASS: joint relation, one-sided distinction,
  missing input rc=2, and malformed input rc=2.
- `scripts/mesh-stall-coupling --test` — PASS; includes a real CPU+memory PSI read.
- `scripts/mesh-stall-coupling --json` at `2026-09-11T06:20:56Z` — live artifact:
  `{"relation":"CALM","cpu_some_avg10":2.26,"memory_some_avg10":0.00,...}`.
- `bash -n scripts/mesh-stall-coupling` — PASS.
- `mesh-autowire --test` — PASS. `mesh-autowire --check` names the source as untracked at
  `HEAD`, so it does not install a cron line; this is consistent with the on-demand
  `orphan-ok` declaration and the explicit no-commit instruction.
- `mesh-doctor --test` — PASS.
- `mesh-doctor --quiet` — NOT CLEAN / timed out rc=124 after reporting pre-existing
  `egress rides tailscale0`, `exit-node set`, and the existing busy-default-mic warning.
  No new orphan warning for `mesh-stall-coupling` appeared.
- `git diff --check` — PASS.

No `[sense]` board post was made because the active contract forbids birth while live
`mesh-doctor` is not clean. No commit was made.
