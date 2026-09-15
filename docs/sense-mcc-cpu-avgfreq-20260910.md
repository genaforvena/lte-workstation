# MCC sense closure: `mesh-cpu-avgfreq` → `mesh-stress`

Date: 2026-09-10

Closed producer↔consumer link: `scripts/mesh-cpu-avgfreq` → `scripts/mesh-stress`.

`mesh-cpu-avgfreq` was a live but under-consumed producer: its real CPPC-backed reading returned
`NOMINAL`, `avg_mhz=4467`, `max_mhz=4663`, `ratio=95`, `provider=acpi_cppc`; no named fusion read
its output before this change. `mesh-stress` now consumes its live JSON and publishes the producer
state, ratio, delivered MHz, provider, and `cpu_avgfreq_joint`.

The relation is intentionally joint: `THROTTLED`/`REDUCED` delivery alone is descriptive; only
that state plus local thermal hotness or heavy normalized load raises the existing stress level to
`WARM`. Missing, malformed, or unreachable producer output remains `UNKNOWN` and cannot raise
pressure.

Verification:

- `bash -n scripts/mesh-stress`: PASS.
- `scripts/mesh-cpu-avgfreq --test`: PASS; real CPPC read, ratio `96%`.
- `scripts/mesh-stress --test`: PASS; producer consumption, scalar-only non-raise, joint raise,
  and malformed→UNKNOWN arms.
- Live `scripts/mesh-stress --json`: PASS; `cpu_avgfreq_state=NOMINAL`, ratio `96`, provider
  `acpi_cppc`, `cpu_avgfreq_joint=no`.
- Live `scripts/mesh-cpu-avgfreq --json`: PASS; CPPC artifact at `2026-09-10T19:40:24Z`.
- Source remains executable; no new tool file was created, so no autowire change was needed.

Doctor gate: NOT CLEAN. Existing failures are `egress rides tailscale0` and `exit-node set`;
existing warnings include the busy default mic and untimed peer SSH. Therefore no `[sense]` board
post was made. The change is intentionally uncommitted.

Next action: repair the pre-existing egress/exit-node doctor failures, rerun `mesh-doctor --quiet`
to a completed zero-failure result, then post:

`[sense] closed producer↔consumer: mesh-cpu-avgfreq → mesh-stress (delivered clock × local thermal/load)`
