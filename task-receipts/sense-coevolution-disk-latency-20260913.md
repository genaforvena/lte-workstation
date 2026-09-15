# Disk-latency producer–consumer link — 2026-09-13

Closed the existing `mesh-disk-latency` → `mesh-situation` link. The producer was live but had no
consumer in the base `mesh-situation`; the parked working-tree change consumes its cached artifact
and relates the disk verdict to the live node-stress axis. This adds no producer or novelty/fitness
score.

Verification:

- `scripts/mesh-disk-latency --test` — PASS; classifier 12/12 and real `/proc/diskstats` read over
  two visible block devices.
- Live producer artifact: `~/.mesh/.disk-latency-state`, timestamp `2026-09-13T01:16:41Z`, verdict
  `FAST`, `ndevs=2`, `window=cum+iv`.
- `scripts/mesh-situation --test` — PASS. Its checks assert the fresh disk artifact, the joint
  relation, overlap coverage, and that a missing artifact renders `UNKNOWN` and exits 2.
- Live consumer: `scripts/mesh-situation --json` — exit 0; consumed `disk_latency=FAST` and emitted
  `latency_stress_relation=NODE-STRESS-WITH-FAST-DISK`, `latency_stress_coverage=2/2`.
- The producer's existing cron cadence is present in `~/.mesh/reflexes.cron`; its successful read
  calls the shared `mesh-state-touch` primitive. No new tool file was created.
- No commit was made.

The required doctor gate did not pass. The full run reported hard failures for egress through
`tailscale0` and an exit node set (`n2sbt7yy6t11CNTRL`), plus a warning that the default mic device
is broken/busy. The broad smoke sweep continued spawning checks for 2:42, so it was stopped; this is
not a clean completion and does not establish an orphan-WARN result. No `[sense]` post was made.

Next action: resolve the existing doctor blockers under the substrate's single-writer rules, run
`mesh-doctor --quiet` to a clean completion, and only then post `[sense]` for
`mesh-disk-latency <-> mesh-situation`.
