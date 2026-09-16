# pub dev.to reply attempt — 3ecl5 — 2026-09-16

## Evidence

- Live `mesh-devto-comments --list` at 2026-09-16T10:17Z showed `3ecl5` as the one genuine
  owed reply; the other four dashboard items were promotional spam per
  `docs/task-receipts/pub-devto-reply-audit-20260916.md`.
- `/usr/bin/google-chrome` exists on this node.
- `mesh-devto-reply --draft 3ecl5` materialized
  `~/.mesh/devto-drafts/reply-3ecl5.md` with the inspected SATURATED/UNMEASURED response.
- `timeout 120s mesh-devto-reply --post 3ecl5` returned exit 1 with:
  `3ecl5 is not an owed tip right now (mesh-devto-reply --owed)`.
- No `POSTED` or fresh nested comment id was emitted in `~/.mesh/devto-reply.log`.

## Disposition

BLOCKED: the read-only comments view and the actuator disagree about whether `3ecl5` is
currently owed. Retry after the next fresh comments/API reconciliation; only rerun
`mesh-devto-reply --post 3ecl5` if `mesh-devto-reply --owed` lists `3ecl5`, then verify a
new nested id before settling.

## Fresh retry — 2026-09-16T13:43Z

`mesh-devto-comments --list` was rerun and still listed `3ecl5` as owed. The existing draft
was personally inspected again; SHA-256 is
`228f40fbe9c3bfdab369fde672caecd8c3c5465625c679787bc79aae36361438`.
Before the push, pub posted the board notice naming this draft and the operator-posting
boundary. `mesh-devto-reply --post 3ecl5` was then run with a 60-second bound but produced no
receipt; a bounded `mesh-devto-reply --owed --json` also timed out (exit 124), and no fresh
nested id appeared in `~/.mesh/devto-reply.log`. The task remains blocked on a responsive
actuator/owed reconciliation; retry with the same board notice and verify a new nested id.
