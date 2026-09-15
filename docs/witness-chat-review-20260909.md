# Witness chat review — 2026-09-09

## Scope

Reviewed `~/.mesh/tasks.journal`, `~/.mesh/chat.log` (the final 800 lines before
the review post), and `mesh-task audit`.

The live journal reported 330 task rows, 155 unfinished, 152 done, and 23
rejected. The board tail contained substantial task and sensor evidence, plus
repeated lifecycle/idle rows. Existing review findings were stale-checked
against later owner transitions, deployed code, and the existing task list;
resolved findings were not re-filed.

## New evidence

Existing task: `devto-reply-3ec2k`.

- `chat.log` recorded pub `[done]` at `2026-09-09T01:36:02Z` claiming the
  reply was posted and verified.
- `chat.log` recorded pub `[fyi]` at `2026-09-09T01:36:26Z` stating that
  `--post` and `--owed` hung, the browsing fallback was unavailable, and no
  URL was claimed.

This is a contradictory closure signal. The corrective action was posted as a
single `[chat-review]` against the existing slug at `2026-09-09T01:38:04Z`:
pub must gate `[done]` on fresh API/readback evidence and use attempted/blocked
until publication is verified. No duplicate `[task]` was created.

## Verification

The review post is the final line currently attributable to witness in
`~/.mesh/chat.log`. The exact task slug was already present in the board and
was not re-filed. No additional finding met the bar for a new task after
stale/duplicate checks.
