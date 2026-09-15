# Witness live unattended follow-up: owner-correction disposition

Measured 2026-09-08 on `phaedra` through `ssh phaedra-direct`.

## Task-routing result

The corrected task is recorded as owner `mesh-land/genome`, but `mesh-task` normalizes
`MESH_TASK_ACTOR=mesh-land/genome` to `genome`. Therefore the requested take is refused:

```text
mesh-task: exact owner required: task owner=mesh-land/genome actor=genome
```

`mesh-task check dispatch ... mesh-land/genome` returns exit 3. No task ledger mutation was
made to bypass this mismatch.

## Live phaedra disposition

- `git stash list` contains only the unrelated manual WIP stash from 2026-06-16.
- The two stale autostash entries are no longer in `refs/stash`.
- The documented object IDs remain valid commits on phaedra:
  `3262dc16f80380caef360720361013c8b396830c` and
  `2f7b55ef448d679aea271a356c1b39eaf5adfd6f`.
- The previously documented `refs/wip/phaedra-autostash-*` names are absent from the current
  ref listing, so the commits are recoverable by object ID but do not currently have those
  durable names. No drop, apply, reset, or worktree edit was performed in this pass.
- Pre-existing phaedra work remains untouched: `CLAUDE.md` and the listed mesh scripts are
  modified, plus the untracked `log`; the manual WIP stash remains.

## Autoland refusal-routing verification

`scripts/mesh-land --test` completed with `rc=0` and `smoke-test: ok`. Its treatment fixture
creates a genuinely diverged repository with a two-day-old autostash and verifies all of the
following: `reconcile_divergence` prints `REFUSING to rebase`, names the parked files, leaves
`HEAD` unchanged, and posts a `[strand]` board alarm. The control fixture also verifies that a
fresh autostash is not refused and that the normal rebase proceeds.

The live source path is `scripts/mesh-land:301-347`; it refuses only autostashes older than
`SETTLE`, emits the incident strand, and returns before `git pull --rebase --autostash`.
