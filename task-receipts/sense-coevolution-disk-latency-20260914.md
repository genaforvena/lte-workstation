# Disk-latency producer–consumer link — 2026-09-14

Validated the existing `mesh-disk-latency` → `mesh-situation` relation from the parked worktree
change. No source file was created or edited during this turn, and no commit was made.

The producer candidate was live but under-consumed: a script scan excluding the new consumer found
no fusion reader for `.disk-latency-state`. The producer is an existing five-minute reflex and has
its cadence header. Its `--test` passed (12/12 classifier cases plus the real two-device,
two-window `/proc/diskstats` check). A live read wrote:

```text
FAST|verdict=FAST|dev=nvme0n1|side=none|read_ms=3.67|write_ms=20.37|window=cum+iv|won=iv|ndevs=2|2026-09-14T00:47:05Z|raw=1789346825;...
```

The artifact mtime was `2026-09-14 00:47:05 UTC`. `scripts/mesh-situation --test` passed; its
fixture verifies the joint relation, overlap coverage, and missing-artifact `UNKNOWN`/exit-2 path.
The live `scripts/mesh-situation --json` exited 0 and consumed the real artifact, reporting
`disk_latency=FAST`, `latency_stress_relation=NODE-STRESS-WITH-FAST-DISK`, and
`latency_stress_coverage=2/2`. The joint label combines disk latency with the live internal-stress
axis and carries overlap coverage.

The required `scripts/mesh-doctor --quiet` gate did not pass. Its preliminary audit reported hard
failures: egress uses `tailscale0`, and exit node `n2sbt7yy6t11CNTRL` is set; it also reported the
existing default microphone warning, untimed peer-SSH warning, six `mesh-song-verify` funnel
bypasses, and five absence-as-negative sites. The broad test sweep had not reached a summary and was
interrupted with exit 130 after the hard failures were established. No orphan warning appeared in
the emitted findings before interruption, but a complete doctor-clean/no-new-orphan result is NOT
established. The `[sense]` post is therefore withheld as required by the mint gate.

Next action: the designated substrate writer resolves the egress/exit-node blockers; then run
`scripts/mesh-doctor --quiet` to completion and confirm PASS with no new orphan WARN. If clean, post
`[sense] mesh-disk-latency <-> mesh-situation` with the live relation and `2/2` overlap artifact.
