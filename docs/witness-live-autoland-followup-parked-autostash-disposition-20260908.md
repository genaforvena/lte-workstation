# Witness live autoland follow-up: parked autostash disposition

Measured 2026-09-08 on `phaedra` through `ssh phaedra-direct`.

## Before

`/root/lte-workstation` had two stale Git autostashes:

| age | object | files | subject |
|---|---|---:|---|
| 2026-08-27 20:18:25 UTC | `3262dc16f80380caef360720361013c8b396830c` | 1129 | `autostash` |
| 2026-08-27 17:48:28 UTC | `2f7b55ef448d679aea271a356c1b39eaf5adfd6f` | 1128 | `autostash` |

The same worktree had unrelated staged modifications and an untracked `log`; those were
not applied, reset, committed, or otherwise changed. A third, manual WIP stash from
2026-06-16 was not part of this repair.

## Durable disposition

Each autostash commit was first anchored outside `refs/stash`:

```text
refs/wip/phaedra-autostash-20260827-201825 -> 3262dc16f80380caef360720361013c8b396830c
refs/wip/phaedra-autostash-20260827-174828 -> 2f7b55ef448d679aea271a356c1b39eaf5adfd6f
```

Only after both anchors were verified as commits were the two `autostash` stash entries
dropped. The manual 2026-06-16 WIP stash remains in `refs/stash`; both anchored commits
remain addressable and therefore recoverable for a later, explicit review.

## Verification

- `git cat-file -e <each anchored object>^{commit}` passed on phaedra.
- `git stash list` on phaedra contains no `autostash` entries and still contains the
  2026-06-16 manual WIP entry.
- The phaedra worktree still reports its pre-existing modifications; no replay or reset
  was performed.
- `/root/lte-workstation/scripts/mesh-land` and `/root/.local/bin/mesh-land` have the
  same SHA-256: `7f133405e0ba716225963ebb90b1ecc22a81ea6347b380c879189af5f443308a`.
- Live cron wiring remains present:
  `3-59/15 * * * * $HOME/.local/bin/mesh-land --autoland >> $HOME/.mesh/land.log 2>&1`.
- A complete remote `mesh-land --test` was started twice but produced no completion output
  within the 30-second SSH command window; this is recorded as unresolved test evidence,
  not as a pass. The direct live stash/ref checks above did complete.

The stale autostash refusal path is therefore no longer needed for these two parked refs,
while the contents remain durably retained under `refs/wip`.
