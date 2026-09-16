# senses — CPU-steal consumer closure — 2026-09-16

## Result

Implemented one coevolutionary producer→consumer closure without adding a producer:

`mesh-cpu-steal` → `mesh-operator-state`

The producer is a live `/proc/stat` counter-delta read. The consumer now reads its fresh
`.cpu-steal-state` artifact, preserves stale/missing/malformed input as `UNKNOWN`, exposes the
state in text and JSON, and emits the joint relation `DESK-CPU-STEAL` only for
`AT-DESK + STOLEN`. The relation cannot be reached by either axis alone.

## Evidence

- `timeout 8 mesh-cpu-steal`: rc=0; `[cpu-steal] CLEAR`; refreshed
  `/home/mesh-home/.mesh/.cpu-steal-state` from the real `/proc/stat` field.
- `bash -n scripts/mesh-operator-state`: pass.
- `scripts/mesh-operator-state --test`: pass; includes fresh fixture consumption, stale fixture
  → `UNKNOWN`, and `AT-DESK + STOLEN` → `DESK-CPU-STEAL`.
- Live `mesh-operator-state --json` completed rc=0 and reported the existing consumer fields
  (`state=UNKNOWN`, `cross_sense=UNREACHABLE`) while the producer artifact was fresh; the JSON
  now includes `cpu_steal_state`.
- Controller recheck at `2026-09-16T03:03:12Z`: `scripts/mesh-cpu-steal --test` passed with a
  real `/proc/stat` read (`cpu steal=0`), then `timeout 8 scripts/mesh-cpu-steal` emitted
  `[cpu-steal] CLEAR`, and `/home/mesh-home/.mesh/.cpu-steal-state` was fresh, non-empty
  (76 bytes), and contained `CLEAR|steal_jiffies=0|delta_jiffies=0|window_ms=250`.
- `mesh-card --test` passed; the node card declares configuration-backed organs, while this
  derived capability is registered by its producer/consumer receipt and live state artifact.
- `mesh-doctor --quiet`: rc=0 but explicitly **skipped** because an automated doctor holds the
  shared lock; `mesh-doctor --test` was bounded at 25s and returned 124 under the existing node
  load. The completed doctor output observed before the lock contention had no new orphan warning,
  but the required clean doctor pass is not yet evidenced.

## Gate

No `[sense]` board post was made. The remaining next action is to rerun `mesh-doctor` to a real
completion after the existing `/home/mesh-home/.mesh/.doctor.lock` holder clears, confirm no new
orphan warning, then post the producer↔consumer closure and settle the task.
