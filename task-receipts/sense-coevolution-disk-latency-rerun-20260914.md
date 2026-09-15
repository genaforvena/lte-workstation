# Disk-latency producer–consumer live recheck — 2026-09-14

The `mesh-disk-latency` → `mesh-situation` relation was already present in the working tree, so
this turn made no source edits and no commit. It revalidated the extant link against fresh artifacts.

- `scripts/mesh-disk-latency --test` passed: classifier 12/12 plus live `/proc/diskstats` reads
  across two devices and two windows.
- `scripts/mesh-disk-latency` returned `FAST` from two devices. The real state artifact
  `~/.mesh/.disk-latency-state` was refreshed at `2026-09-14 04:47:12 UTC`.
- `scripts/mesh-situation --test` passed its suite, including the existing overlap and missing-input
  assertions.
- `scripts/mesh-situation --json` exited 0 and consumed the real state: `disk_latency=FAST`,
  `latency_stress_relation=NODE-STRESS-WITH-FAST-DISK`, `latency_stress_coverage=2/2`; the live
  internal axis was `WATCH`.
- `rg -l '\.disk-latency-state|mesh-disk-latency' scripts` shows the consumer `mesh-situation`
  (plus the storage-health/system-vitality readers), so this is not under-consumed.

The required `mesh-doctor --quiet` gate did not pass. It immediately reported hard failures for
egress through `tailscale0` and an exit node set (`n2sbt7yy6t11CNTRL`), plus the existing default
microphone warning. It also reported the untimed peer-SSH, six song-verification funnel bypasses,
and five absence-as-negative warnings. No orphan warning appeared in the findings emitted before
the run stalled. After five minutes without a summary, this invocation was interrupted with exit
130 to stop its broad test sweep. A complete doctor pass and final orphan-clean result are NOT
established. No `[sense]` post was made because the required doctor-clean gate remains unmet.

Next action: the designated substrate writer resolves the live egress/exit-node blockers; then run
`mesh-doctor --quiet` to completion and confirm PASS with no new orphan WARN. If clean, post
`[sense] mesh-disk-latency <-> mesh-situation` with the live `2/2` overlap artifact.
