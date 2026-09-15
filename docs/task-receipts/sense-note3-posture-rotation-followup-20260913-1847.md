# Note 3 posture × rotation sense — 2026-09-13 follow-up

The existing uncommitted on-demand reader at `scripts/mesh-note3-posture-rotation` measures one
fresh, aligned pair of Note 3 HAL orientation and gyroscope events. This is joint evidence: posture
and rotation through that posture are not inferable from either axis alone. No verdict or cached state
is written.

## Refreshed live evidence

- `bash tests/test-mesh-note3-posture-rotation.sh` — PASS; fixtures plus a real Note 3 HAL pair,
  `coverage=1/1 paired sample`, `pair_skew_ms=0.0`, `pair_age_ms=14.592`.
- A separate `scripts/mesh-note3-posture-rotation --json` read exited 0 with a fresh pair,
  `pair_skew_ms=0.0`, `pair_age_ms=33.507`.
- Source mode is `775`; the source declares `# orphan-ok:`. It is stateless, so no state-touch rule
  applies.

## Doctor gate — withheld

`mesh-doctor --quiet` reported hard failures for the default egress riding `tailscale0` and a selected
Tailscale exit node. It also reported a broken/busy default mic, an untimed peer-SSH probe, six
declared-funnel bypasses, and five sites that render missing evidence as a negative reading. After
nearly six minutes with no further output, this run was stopped by terminating only its own process
group (exit 143). It did not complete, did not pass, and did not establish a complete orphan census.
No `[sense]` post was made.

The egress failures are substrate state owned by routing; this senses task did not alter it. The
reader and its test remain existing uncommitted work. The `[sense]` obligation stays open until a
complete `mesh-doctor` run exits 0 and establishes no new orphan WARN.

## Exact next action

After the routing owner resolves or explicitly dispositions the egress FAILs and the stalled doctor
probes can complete, run `mesh-doctor --quiet` to completion. If it exits 0 with no new orphan WARN,
refresh `scripts/mesh-note3-posture-rotation --json` and post that live artifact as `[sense]`.
