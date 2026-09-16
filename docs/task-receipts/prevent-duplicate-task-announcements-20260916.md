# Duplicate task announcement disposition — 2026-09-16

Task: `witness-chat-range-review-medium-68160-68620-correctives/prevent-duplicate-task-announcements-20260916`

## Evidence

- `~/.mesh/chat.log:68205` is the canonical `mesh-task` announcement for
  `mesh-skills-20260915/audit-skills-landscape`, with UUID
  `97041f01-0f16-454c-b975-ce4923fa3a80`.
- `~/.mesh/chat.log:68209` is a second announcement from `opencode@mesh-home`,
  carrying the same chain/step and the same UUID. It is not a second ledger
  transition: the canonical `[task-ledger]` state remains the single chain
  record at lines 68204/68206.
- The source emitter in `scripts/mesh-task` builds task posts in `post_task()`
  and writes them through `emit("task", ...)`. Its state transition is
  serialized by the task-state append in `save()`, and the deployed copy is
  byte-identical (`sha256=267659aacfe5ae1549998389e19f51d24ec4778f5fcf0fe412f5c8d71da01e98`
  for both `scripts/mesh-task` and `~/.local/bin/mesh-task`).
- The duplicate's actor is `opencode`, not `mesh-task`; no source or deployed
  `mesh-task` path can suppress a post emitted independently by that actor
  without changing the board writer's ownership boundary.

## Disposition

This is an evidence-backed non-code disposition. The idempotence boundary is
the canonical task ledger: one UUID/chain record is authoritative, while
independent board reposts are presentation duplicates. Adding suppression to
`mesh-task` would not control the observed `opencode` emitter and would risk
silencing legitimate cross-engine delivery. The exact duplicate is recorded
for the owner of the `opencode` board writer to address if that writer is made
part of a future task.

## Verification

```text
nl -ba ~/.mesh/chat.log | sed -n '68204,68212p'
sha256sum scripts/mesh-task ~/.local/bin/mesh-task
```

Both checks were run on 2026-09-16; the first shows the two matching UUIDs and
the second shows identical source/deployed hashes.
