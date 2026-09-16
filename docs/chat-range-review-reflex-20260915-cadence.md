# Witness chat-range review cadence adjustment — 2026-09-15

The live review producer was firing every minute while `~/.mesh/chat-range-review.log`
showed 89 open review chains and repeated held rows. That cadence was unnecessary
once the backlog gate was engaged and made the reflex itself noisy.

Adjustment:

- `scripts/mesh-chat-range-review` now declares a 15-minute reflex cadence.
- Its default pending-review cap is 3 instead of 10; the existing environment override
  remains available for deliberate tuning.
- The live cron entry in `~/.mesh/reflexes.cron` was changed to `*/15 * * * *`.

No cursor or existing task was changed. When the backlog falls below the cap, reviews
resume from the saved cursors; delayed ranges remain pending rather than skipped.

Verification: `python3 tests/test-mesh-chat-range-review.py` and
`python3 scripts/mesh-chat-range-review --test` pass; the live cron entry and source
header agree on the 15-minute cadence. At change time the state cursors were near
62625, medium 66879, deep 66879, with no pending cursor transaction.
