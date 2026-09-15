# New sense: NVMe internal thermal gradient — 2026-09-11

Added `scripts/mesh-nvme-internal-gradient`, a minimal relation over the live NVMe hwmon channels
`Sensor 1` and `Sensor 2` on one controller. It reports `INTERNAL-GRADIENT` when their absolute
difference is at least 10°C, otherwise `INTERNAL-COUPLED`. Either channel missing or malformed is
UNKNOWN (`rc=2`); there is no zero/default fallback. Every successful run stamps the state with
`mesh-state-touch`.

Evidence:

- `scripts/mesh-nvme-internal-gradient --test` — PASS; fixture relation, missing-sysfs `rc=2`, and
  real pair-read gate all passed.
- `scripts/mesh-nvme-internal-gradient --json` — LIVE: `Sensor 1=68850mC`, `Sensor 2=56850mC`,
  `delta=-12000mC`, `verdict=INTERNAL-GRADIENT`, observed `2026-09-11T17:36:58Z`.
- `bash -n scripts/mesh-nvme-internal-gradient` and `git diff --check` — PASS.
- Source is executable and deployed at `~/.local/bin/mesh-nvme-internal-gradient`.
- `mesh-autowire --check` — correctly refused wiring because the source is not tracked at `HEAD`;
  it named the exact source and did not add a cron line. No commit was made, per task instruction.
- `mesh-doctor --quiet` — NOT CLEAN due pre-existing substrate failures: `egress rides tailscale0`,
  `exit-node set`, and `mic DEFAULT device broken/busy`.
- `mesh-doctor --test` — FAIL on a pre-existing twice-red-tool fixture assertion (`got 'na'`).

No `[sense]` board post was made: the required clean live doctor gate was not met. The tool remains
uncommitted and ready for the next action: resolve the independent doctor blockers, then land the
source and rerun `mesh-autowire` so its tracked-source gate can wire it.
