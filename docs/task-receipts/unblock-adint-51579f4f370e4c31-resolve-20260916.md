# adint unblock recovery — genome lifecycle drain — 2026-09-16

Task: `unblock/adint/51579f4f370e4c31/resolve`
Parent: `unblock/health/97b723e65eaf0f9e/resolve`

## Live evidence

- `mesh-tell --peek genome` showed the stuck `/clearclear` input before recovery.
- `mesh-mind-state genome` reported `WEDGED-INPUT`.
- Genome's handoff reported 227 dirty files parked at `refs/wip/genome` and the
  exact lifecycle retry edge.
- `mesh-clear genome` returned exit 0 and wrote a fresh handoff; subsequent
  `mesh-mind-state genome` reported `IDLE` and the pane showed an empty prompt.
- Required retry `MESH_WEDGE_RECOVER=1 mesh-tell --ack genome '/clearclear'`
  returned exit 3: `REFUSED — genome has a pending turn handoff/reset`.
- `mesh-codex-lifecycle --ready genome` returned exit 3. The only nonterminal
  genome lifecycle receipt is `pending`, with error `clear sent but fresh empty
  composer not observed`.
- A bounded `mesh-codex-lifecycle --drain` attempt timed out at 30 seconds while
  waiting on the serialized lifecycle lock; the pane-consumer/background retry
  is still holding or waiting for that lock.

## Disposition

**BLOCKED — dependency.** No genome worktree or WIP was mutated beyond the
authorized `mesh-clear` lifecycle operation; no task ownership or substrate
state was changed outside this resolver.

Exact retry edge:

```text
after the pending genome lifecycle receipt is cleared and the lifecycle lock
drains, run MESH_WEDGE_RECOVER=1 mesh-tell --ack genome '/clearclear', then
verify mesh-tell --peek genome and mesh-mind-state genome; only then resume the
health parent.
```
