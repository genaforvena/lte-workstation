# Autoland parked-autostash disposition — 2026-09-08

Task: `witness-live-unattended-followup-20260908-generic-20260908/repair-parked-autostash-generic`

## Disposition

Inspected on `phaedra` through `ssh phaedra-direct` at 2026-09-08. The two stale
Git autostashes from 2026-08-27 are no longer parked in `refs/stash`; both were
already preserved as durable refs by the earlier repair:

| ref | object | created |
|---|---|---|
| `refs/wip/phaedra-autostash-20260827-201825` | `3262dc16f80380caef360720361013c8b396830c` | 2026-08-27 20:18:25 UTC |
| `refs/wip/phaedra-autostash-20260827-174828` | `2f7b55ef448d679aea271a356c1b39eaf5adfd6f` | 2026-08-27 17:48:28 UTC |

The only remaining `refs/stash` entry is the unrelated manual WIP stash from
2026-06-16 (`e82ca16393c884db1a3ea89acedb3ba34b6b59f5`). It was retained.
The pre-existing phaedra worktree changes (12 modified scripts plus untracked
`log`) were unchanged; no stash was applied, dropped, reset, committed, or
otherwise replayed by this repair.

During live verification, `mesh-land --autoland` created a transient fresh
autostash while attempting to reconcile phaedra's dirty, diverged worktree and
then hit a modify/delete conflict. The rebase-abort path returned the worktree
to its prior state and did not leave that fresh autostash parked. This is a
separate current blocker: phaedra is `ahead 1, behind 465` relative to origin.

## Refusal-routing verification

- `/root/lte-workstation/scripts/mesh-land` and `/root/.local/bin/mesh-land` on
  phaedra both hash to
  `7f133405e0ba716225963ebb90b1ecc22a81ea6347b380c879189af5f443308a`.
- Live cron wiring remains present:
  `3-59/15 * * * * $HOME/.local/bin/mesh-land --autoland >> $HOME/.mesh/land.log 2>&1`.
- `scripts/mesh-land --test` completed locally against that exact implementation
  with `smoke-test: ok`. Its isolated treatment fixture proved that a stale
  autostash is named, refuses rebase, leaves `HEAD` unmoved, and posts the
  `[strand]` refusal; the control fixture proved a fresh autostash proceeds.
- The live phaedra invocation emitted the expected non-silent refusal for the
  currently observed divergence/conflict and did not land or push anything.

Conclusion: the original parked-autostash strand is resolved and its contents
remain recoverable under `refs/wip`. Autoland refusal routing is wired and
verified. The next action is a separately authorized/manual reconcile of
phaedra's current divergence; it must not replay either preserved WIP ref or
touch the unrelated dirty worktree without an explicit content decision.
