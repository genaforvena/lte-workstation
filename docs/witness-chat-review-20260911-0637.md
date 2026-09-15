# Witness chat review — 2026-09-11

## Result

No new review task. The supplied 800-line digest contains approximately 558 substantive
lines, 240 idle/room-moved lines, and 2 mind-churn lines. The remaining repetition is
already covered by existing review work and current source gates.

## Checks

- `mesh-device-churn` currently routes unchanged CHURN repeats to `mesh-trace` and emits
  only a counted roll-up (`scripts/mesh-device-churn:360-363`); its regression test requires
  the repeat to be traced and the roll-up to preserve the suppressed count
  (`scripts/mesh-device-churn:555-570`). Existing slug:
  `chat-review/device-churn-repeat-posts-drown-board`.
- `mesh-udev-stream` keeps EVENTS and GAP on separate debounce markers and routes
  floor-level GAP readings to trace (`scripts/mesh-udev-stream:128-147,625-653`); its test
  asserts that GAP cannot evict EVENTS (`scripts/mesh-udev-stream:1198-1267`). Existing
  slug: `chat-review/udev-stream-gap-and-events-share-one-debounce-slot`.
- `mesh-chat-review` requires both elapsed time and new-board-line input before injection
  (`scripts/mesh-chat-review:15-18`) and records skipped runs with the gate reading
  (`scripts/mesh-chat-review:544-551`), so the repeated witness reviews are not evidence of
  a newly broken trigger.
- The recurring overdue coordination/health rows were rechecked against `tasks.journal`
  and `mesh-task audit`; they are exact existing chains, not new defects to duplicate.

## Verification

Read `~/.mesh/tasks.journal`, the last 800 lines of `~/.mesh/chat.log`, and ran
`mesh-task audit`. No source errors or new malformed task-state records were found.
