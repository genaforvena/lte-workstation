# Witness autoland stale-stash disposition — 2026-09-16

Task: `witness-chat-range-review-near-61067-61133-correctives/resolve-parked-autostash`

## Evidence

- Source witness: `~/.mesh/chat.log:71742` (the current log line corresponding to the
  cited Phaedra incident) reports `autoland REFUSED to rebase`, `stash@{0}`, age
  `636299s`, and 14 paths: `CLAUDE.md`, `scripts/mesh-drop-stages`,
  `scripts/mesh-light`, `scripts/mesh-load`, and `scripts/mesh-mca` (the strand's
  abbreviated path listing).
- This turn ran in `/home/mesh-home/lte-workstation` on the genome node. The target
  Phaedra checkout is not mounted or otherwise available here.

## Commands and results

| Command | Exit | Result |
| --- | ---: | --- |
| `git status --short` | 0 | Genome checkout has pre-existing unrelated dirty paths; no stash mutation was attempted. |
| `git stash list --date=iso --format='%gd %H %ci %s'` | 0 | No local stash entries printed. |
| `git for-each-ref refs/stash refs/wip/phaedra-autostash --format='%(refname) %(objectname) %(creatordate:iso8601) %(subject)'` | 0 | No matching local refs printed. |

## Decision

**BLOCKED — preserve the Phaedra stash untouched.** The evidence identifies a stale
Phaedra autostash, but this node cannot inspect its object or safely apply/drop it. No
destructive stash action was performed. The task must retry after the next Phaedra
autoland pass observes the same parked stash and a Phaedra-capable steward can inspect
the live ref; then record an explicit keep/apply/drop decision before rerunning the
affected autoland verification.

## Live retry — 2026-09-16T06:43Z

Phaedra became reachable at `phaedra` (`100.94.116.17`). Read-only inspection of
`/root/lte-workstation` found the same parked `stash@{0}` with identity
`e31ca425f4ac26f13a17c0b3182d605946aa55cb`, created 2026-09-08T20:03:06Z, and
14 changed paths. The patch is 147 deletions and 2 insertions: it removes stale
`observer-probe` annotations from 12 scripts, removes 110 lines implementing
`send-file`, `create-channel`, and `set-public` from `scripts/mesh-tg-user`, and
changes one usage line. Current Phaedra `HEAD` (`6e7a7826`) and `origin/main`
(`57ac5b71`) both retain those capabilities, so replaying this old revert would
discard current behavior. The checkout also has an unrelated untracked `log`.

**Decision: DROP `stash@{0}`.** This preserves the current tracked behavior and
removes the stale parked revert; the untracked `log` is not touched. Decision
recorded before the remote mutation. Next command: run Phaedra `mesh-land
--autoland` and capture its exit/result; if it still refuses, preserve the exact
new blocker and retry edge.

## Verification after disposition — 2026-09-16T06:45Z

On Phaedra, `/root/.local/bin/mesh-land --autoland` was rerun after the drop.
The stale-stash gate was passed, but autoland found local `main` at
`6e7a7826`, diverged from `origin/main` at `57ac5b71`, and its automatic
rebase-reconcile hit:
`CONFLICT (modify/delete): scripts/mesh-observer-effect deleted in 6e7a7826
and modified in HEAD`. The live checkout remained `main...origin/main [ahead 1,
behind 1476]`, with only the pre-existing untracked `log`; no rebase markers
remain and origin was untouched. The command's own `mesh_land_rc=0` is retained
as an honest tool result even though the board strand is emitted and manual
reconciliation is required.

The exact retry edge is now: a Phaedra-capable steward must manually reconcile
the modify/delete conflict and the remaining divergence, then rerun
`/root/.local/bin/mesh-land --autoland` and verify origin/working-tree state.
