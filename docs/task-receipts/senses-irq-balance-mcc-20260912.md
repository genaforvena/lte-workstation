# Senses MCC closure: IRQ balance × local load

Date: 2026-09-12

## Change

`scripts/mesh-stress` now consumes the live artifact written by `mesh-irq-balance` at
`~/.mesh/.irq-balance-state`. It publishes the state, share, and joint relation in `--json` and
the human reason line. Only `CONCENTRATED` IRQs plus normalized CPU load above `1.0` can add a
WARM-capped precursor. Missing, malformed, stale, or timestamp-inconsistent artifacts remain
UNKNOWN; `--json` and `--check` exit 2 when the producer cannot be read.

The producer artifact is fresh and is written from `/proc/interrupts`; it has no reader among the
five listed fusion consumers before this change. No new tool file was created.

## Verification

- `mesh-irq-balance --test`: PASS; includes fixture balance/concentration, unreachable exit 2, and
  a real `/proc/interrupts` read.
- New `mesh-stress --test` relation assertions were reached and passed: the producer artifact is
  parsed; concentration alone leaves CALM unchanged; concentration plus heavy load yields WARM;
  a balanced sample stays descriptive; a stale sample becomes UNKNOWN.
- Live producer and consumer were exercised end to end. `mesh-stress --json` read the fresh
  `BALANCED` artifact at 59.28% and published `irq_balance_state=\"BALANCED\"`,
  `irq_balance_share=\"59.28\"`, `irq_balance_joint=\"no\"`. With the artifact path absent and
  the other required inputs supplied, it published `irq_balance_state=\"?\"` and exited 2.
- `bash -n scripts/mesh-stress`: PASS.
- Full `mesh-stress --test`: FAIL in its later live-dependent memory assertion (`IDLE swap must not
  raise level`); during this run the host was under load and the live stress JSON showed other
  active pressure relations. The new isolated IRQ-balance assertions had already passed.
- `mesh-doctor`: NOT CLEAN / INCOMPLETE. It reported egress integrity FAILs (`tailscale0` egress and
  a configured exit node), plus existing warnings for default-mic contention, untimed peer SSH,
  sole-path bypasses, and absence rendered as a negative. Its smoke-test stage remained in
  `mesh-udev-stream --test` beyond its 20-second timeout. The invocation was stopped with exit 143
  after confirming the hang; no final clean result was produced.

## Gate and next action

No `[sense]` line was posted, as required by the clean-doctor gate. No commit was made.

Next: once the egress integrity failures are resolved by the substrate owner and `mesh-doctor`
completes cleanly with no new orphan warning, rerun `mesh-stress --test`, then post
`[sense] mesh-irq-balance -> mesh-stress: fresh /proc/interrupts balance × normalized CPU load`.
