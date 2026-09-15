# MCC closed link: `mesh-pty-count` → `mesh-situation` — 2026-09-11

Applied the mutual minimal criterion using option (b): `mesh-pty-count` was a live but
under-consumed sense, and `mesh-situation` now consumes it. The producer reads the kernel's
`/proc/sys/kernel/pty/nr` allocation counter; the fusion publishes `pty_count` and `pty_status`
without changing posture semantics. Missing, malformed, or unreachable producer output renders
`"pty_count":"UNKNOWN"` and forces consumer machine/edge modes to exit 2.

Verification:

- `mesh-pty-count --json`: live `{"status":"LIVE","pty_count":37,...}` at
  `2026-09-11T04:04:39Z`, exit 0.
- `mesh-situation --test`: PASS; fixture producer is consumed as `pty_count=23`, and an
  unreachable fixture produces valid JSON with `pty_count=UNKNOWN` and consumer exit 2.
- `mesh-situation --json`: live output carried `"pty_count":37,"pty_status":"LIVE"`; overall
  exit 2 was honest for other unavailable axes.
- `rg -l 'mesh-pty-count' scripts/*`: exactly the producer and `scripts/mesh-situation`, proving
  the new consumer link is present.
- `mesh-doctor --test`: PASS. Full `mesh-doctor --quiet` was not clean: it reported pre-existing
  `egress rides tailscale0` and `exit-node set` failures, then timed out before completion. No
  `[sense]` post was made because the contract requires a clean full doctor first.

No commit was made.
