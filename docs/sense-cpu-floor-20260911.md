# New sense: ACPI CPPC minimum performance floor

Implemented `scripts/mesh-cpu-floor` as an on-demand, honest hardware sense. It reads the
per-core `/sys/devices/system/cpu/cpu*/acpi_cppc/lowest_freq` values, publishes the minimum,
sum, and number of cores, and exits `2` when no readable source exists. It has an executable
source header with `orphan-ok`; it is deliberately not cron-wired.

Evidence:

- `scripts/mesh-cpu-floor --test` — PASS; fixture parser and real-read gate passed:
  `550 8800 16`.
- `scripts/mesh-cpu-floor --json` — real artifact:
  `{"min_khz":550,"sum_khz":8800,"cpus":16,"source":"acpi_cppc/lowest_freq"}`.
- `mesh-autowire --check` — no `mesh-cpu-floor` orphan warning; existing candidates only.
- `git diff --check` — PASS.
- `mesh-doctor` — NOT CLEAN: pre-existing egress FAILs (`tailscale0` route and exit-node SPOF)
  and existing WARNs (default mic, untimed peer SSH, local-mind failover). No new orphan WARN
  was emitted for this sense.

No `[sense]` board post was made because the mint contract requires a clean `mesh-doctor` first.
No commit was made.
