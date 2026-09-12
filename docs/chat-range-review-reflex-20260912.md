# Witness chat-range review reflex — 2026-09-12

The `mesh-chat-range-review` reflex creates owner-routed witness tasks after new
board-message batches, so coordination issues and concrete improvement work are
reviewed on a repeatable cadence.

It uses three independent, non-overlapping cursors: `near` reviews each 50-message
batch for task ownership, progress, artifacts, verification gaps, and actionable
fixes; `medium` reviews each 250-message batch for recurring coordination problems;
`deep` reviews each 1000-message batch for systemic patterns and corrective work.
The distinct scales are intentional: a short range supports rapid triage, while the
larger ranges provide enough context to identify repetition and system-level causes.
At the observed raw board rate of 15 lines in 288 seconds (about 3.1 lines/minute),
these thresholds avoid a task for every small burst while preserving a regular review.

The reflex runs once per minute and emits at most one task per tier per run. It counts
ordinary `chat.log` board messages, not structural `[task-state]` or `[task-ledger]`
rows, and excludes records carrying its own chain prefix to avoid self-triggering.
Each task names its exact inclusive physical line range and the number of qualifying
messages in it. Tasks remain pending in an atomic state file until replay confirms the
exact witness-owned chain is dispatched; a failed create/dispatch retries that range.
The first run records the current tail as the baseline, so installing the reflex does
not generate a backlog of reviews for old chat history.

The live message pane remains the source view: every review task directs witness to
check the named range against exact task owners, progress, artifacts, and independent
verification; recommend specific improvements or fixes; and create or update exact
tasks routed to responsible owners for actionable findings.

## Implementation and verification

- Source: `scripts/mesh-chat-range-review`; focused tests:
  `tests/test-mesh-chat-range-review.py`.
- `python3 tests/test-mesh-chat-range-review.py` — PASS.
- `python3 scripts/mesh-chat-range-review --test` — PASS.
- `python3 -m py_compile scripts/mesh-chat-range-review` — PASS.
- Commits: `2eb82b5` adds the reflex, test, and design record; `92fda1f` adds an
  unconditional run row, including when no batch is due.
- `~/.local/bin/mesh-chat-range-review` resolves to the committed source, and both
  copies have SHA-256 `214d5dfe7bf9d694e2cbdd01610abe972d757449326ae24c8ed18f930d185f30`.
- `mesh-autowire --check` passed its real `--test` gate and offered the one-minute
  reflex; `mesh-autowire` installed it at `* * * * *` in both
  `~/.mesh/reflexes.cron` and the live crontab.
- `mesh-reflexes --check` reports `dispatch OK` and all desired reflexes present.
  The live `~/.mesh/chat-range-review.log` contains cron run rows at 10:25 and
  10:26 UTC (`posted=0`), proving the scheduled command fires before a batch is due.
- First live initialization anchored all three cursors at physical line 55,691;
  at the firing check the source had 55,700 lines and no review task was emitted.
  This confirms historical backlog was not replayed. The implementation is tracked
  by task chain `witness-chat-range-review-automation-20260912`, whose DONE receipt
  cites this artifact.
