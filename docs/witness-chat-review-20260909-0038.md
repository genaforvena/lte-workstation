# Witness chat review — 2026-09-09 00:38 UTC

## Finding

The existing `chat-review/mesh-path-watch-relay-crossing-no-episode-cooldown` task is
still live. In the reviewed 800-line board window, `path-watch@mesh-home` posted the same
`imac-rozalia` direct-to-DERP warning 20 times at roughly 20-minute intervals.

## Code check

Source and deployed `scripts/mesh-path-watch` have identical SHA-256
`71253ae7a5b7cf51d35ee6c99d55eb7e3e004868b5112622fa7083a0312ddd59`.
Lines 114–115 reset the relay streak after a direct recovery; lines 129–155 emit a new
board post whenever the streak reaches `DEBOUNCE`, with no per-peer alert epoch or episode
cooldown. The live `.path-watch-modes` file has no alert-epoch field. This matches the
observed repeated flap episodes and is not inferred from historical scrollback alone.

## Stale check and routing

No later `[done]` for the exact slug was found in `chat.log`; the task remains the existing
canonical slug, so no replacement slug was created. Fresh `[chat-review]` and `[task]` lines
were posted at 00:38:29–00:38:30 UTC to `mesh-path-watch/genome`.

## Verification

- Read `~/.mesh/tasks.journal`, the last 800 lines of `~/.mesh/chat.log`, and `mesh-task audit`.
- Compared source and deployed hashes.
- Inspected the live modes/tape state and the relevant source lines.
- Confirmed the new board pair is present in `chat.log`.
