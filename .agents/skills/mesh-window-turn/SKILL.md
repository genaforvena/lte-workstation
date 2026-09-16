---
name: mesh-window-turn
description: Execute a mesh window turn from its current charter, pane, task queue, and handoff, including verification and durable continuation. Use on mesh window wake or task dispatch.
---

Resolve the real window from `TMUX_PANE` or the explicit session identity; never adopt
another lane's identity to make a command pass. Read its node-local charter, falling
back to `charter/<window>.md` through `mesh-handoff --charter <window>`. The charter
defines this window's role; do not copy a roster or another window's duties here.

This skill is a living procedure, not set in stone. Adapt and improve it for demonstrated
needs within your authorized scope. Record the reason, update the shared instructions,
test the changed behavior, and hand off the result. Preserve authorization, charter
boundaries, privacy, single-writer coordination, and verification; skill edits do not
waive those constraints. Ordinary in-scope improvements need no new approval ritual.

Read the prior handoff and the live data pane. Check current ledger state before
resuming: a restored completion is history, not new work. Read the complete
`mesh-task queue --dispatch --owner <window>` and choose eligible work that advances
the window's goal, including runnable prerequisites. A query failure means unknown,
not an empty queue. Use `mesh-task check dispatch <chain>/<step> <window>` before take.

For `tg` and `tg-roz`, an inbound message or eligible owned task is the wake reason.
Dashboard drift, outgoing reply display, periodic health reads, and context restoration
alone are not new work. Keep these lanes quiet until an event; retry only pending work.

Claim and advance independent work within the configured capacity. Prefer subagent
workflows by default: delegate each independently verifiable audit or fix, fan out
non-overlapping work, and use isolated worktrees for edits. Keep tiny single-file or
tightly coupled work local when delegation costs more coordination than it saves.
Keep ownership changes, board voice, substrate writes, landing, and final artifact
verification in this window. Inspect returned artifacts yourself and record which
delegation produced them and how you verified them; an agent report is not evidence.

Every actionable finding from an audit or review must result in an exact-owner corrective
task before the audit settles. First search for an existing active task that covers the
finding and cite it; otherwise create a corrective task naming the owner, acceptance
condition, retry edge, and durable artifact path. A finding recorded only in a receipt is
incomplete. Canonical task plans use `owner<TAB>step-slug<TAB>description` (or the
four-column form with priority); verify the created ledger row and dispatch eligibility.
Mark every task that performs an audit, review, reconciliation, or other work promising
downstream task creation with the plan header `#tags=audit-followthrough`. Its completion
artifact must have an adjacent `<artifact>.findings.json` file with `version: 1` and a
nonempty `findings` array. Each unique finding is either `actionable: true` with exact
`task` (`chain/step`) and `owner`, or `actionable: false` with a nonempty `reason`.
`mesh-task done` verifies these mappings against canonical replay; tagged work cannot use
`reject` to bypass disposition, so block it with an exact retry edge or complete it with a
reasoned non-actionable disposition. This tag is explicit metadata, never inferred from a
task name or prose.

Use `mesh-operator-followthrough` for operator work that needs durable follow-through;
use `mesh-task-recovery` for apparently stranded work. Follow the charter's concrete
tools and acceptance criteria: a delivery lane owes a receipt, a code lane owes verified
behavior, a sensor lane owes a fresh real reading. A different lane's success is not yours.

Before the turn ends, settle through `mesh-task done`/`reject`, or persist progress or
a typed block with the exact next action and retry edge. Write
`mesh-handoff <window> "<result> + <next command or event> + <artifact paths>"`.
Let the native completion callback own normal resets; do not clear during tool work.
