# Phaedra parked-autostash review — 2026-09-15 (read-only, stash untouched)

Task: `phaedra-autostash-steward-disposition-20260913/review-parked-object`
Scope from `docs/task-receipts/witness-autoland-repeat-20260913.md`: review exact
object `e31ca425f4ac26f13a17c0b3182d605946aa55cb` (14 paths) before any
apply/drop/pop/rebase/reset. Stash was NOT touched in this review.

## Live verification (phaedra-direct ssh, read-only)

- Object present: `git rev-parse 'stash@{0}^{commit}'` →
  `e31ca425f4ac26f13a17c0b3182d605946aa55cb` (matches task + receipt).
- Path set (14): `CLAUDE.md`, `scripts/mesh-drop-stages`, `scripts/mesh-light`,
  `scripts/mesh-load`, `scripts/mesh-mca`, `scripts/mesh-net-drop`,
  `scripts/mesh-net-io`, `scripts/mesh-presence`, `scripts/mesh-promises`,
  `scripts/mesh-room-trace`, `scripts/mesh-socket-state`,
  `scripts/mesh-tcp-metrics`, `scripts/mesh-tg-user`, `scripts/mesh-wifi-link`.
- Stash working-tree diff: **2 insertions, 147 deletions** — it almost purely
  REMOVES lines.
- Phaedra worktree HEAD: `6e7a7826` (same as 2026-09-13 receipt); status clean
  except untracked `log`. No second worktree.
- Landed commit `964facc2` (2026-08-30) "land 14 settled stream fix(es)" touches
  the same lane: 823 insertions, 1 deletion across CLAUDE.md + 13 of the same
  scripts (plus `mesh-observer-effect` in place of `mesh-promises`).

## Recommendation (evidence-backed, decision left to steward per task scope)

**DROP `stash@{0}` on phaedra, keep manual `stash@{1}` (2026-06-16 WIP) alone.**
Rationale: the parked autostash (created 2026-09-08) is the pre-land state of a
lane that has since landed as `964facc2` and descendants; popping/replaying it
would revert live landed work (147 deleted lines vs the landed additions). It is
a stale duplicate of settled work, same class as previously closed autostash
dispositions. Safe drop form (keeps object recoverable via reflog):
`git -C /root/lte-workstation stash drop 'stash@{0}'` — steward or genome hand only.

Remaining atom for steward: one confirmation + the drop command above.
