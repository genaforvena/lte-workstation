# Pub dev.to comment review — 2026-09-16

Live source: `mesh-devto-comments --list` at 2026-09-16T11:25Z.

The dev.to API is read-only for comments; no comments were posted by this turn. The following
operator-ready replies are grounded in the published artifacts:

- `3ej9o` / @raknaos — The session-jar example separates recovery evidence from elapsed time.
  The current voice case's 300-second quarantine only ages out the marker; compare a health probe
  with an opportunistic retry and record outcomes before choosing the release rule.
- `3ee66` / @topstar_ai — Agree that failure class and confidence are the next refinement:
  explicit engine errors fail over, while uncertain timeouts get one bounded retry. The current
  evidence is the measured 300-second quarantine and proven-delivery release.
- `3ecga` / @alexshev — Persist failure class and confidence to keep noisy telemetry from
  causing unnecessary failover; test explicit-error and uncertain-timeout branches separately.
- `3ecgb` / @alexshev — Accept the proposed fixed mixed-workload evaluation with declared
  weighting and confidence intervals across seeds. The current evidence covers two held-out topic
  sets and does not justify a single deployment score.
- `3ec2k` / @raknaos — Price failed attempts, keep provider charge and tool labour distinct,
  version rates without rewriting historical money rows, and book the watcher's own TURN as
  visible measurement labour.

Do not reply to these unrelated promotional comments: `3ekdf`, `3eoo9`, `3ekc9`, and `3ef25`.

Delegation: `pub-reply-review` performed a read-only cross-check of the live queue and local
evidence. I personally inspected its report and the cited draft/source files before recording
this artifact. No files were edited by the worker and no external side effects occurred.
