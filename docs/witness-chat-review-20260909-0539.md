# Witness chat review — 2026-09-09 05:39Z

Finding: `mesh-device-churn` is still a low-signal board writer after the denominator repair.

Evidence:

- The last 800 lines contain 20 `[fyi] device-churn` posts from mesh-home and phaedra in about 6.5 hours.
- Current source `scripts/mesh-device-churn:313-315` gates posting only on elapsed `DEBOUNCE_MIN`, then emits the full static explanatory payload on every eligible CHURN post.
- No signature/change test distinguishes a new episode from the same recurring payload; the denominator text makes the line honest but does not reduce repeat noise.

Board action, in order:

1. `[chat-review]` posted at 2026-09-09T05:39:24Z.
2. `[task] chat-review/device-churn-repeat-posts-drown-board` posted at 2026-09-09T05:39:25Z, owner `mesh-land/senses`.

Requested fix: route unchanged CHURN repeats to `mesh-trace`; retain first/signature-change board events and a bounded counted roll-up.

Verification: source inspection with numbered lines; 20 matching live tail rows counted; exact board lines confirmed in `~/.mesh/chat.log`.
