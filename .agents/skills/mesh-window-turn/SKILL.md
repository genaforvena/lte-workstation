---
name: mesh-window-turn
description: Execute a mesh window turn from its current charter, pane, task queue, and handoff, and finish with a real artifact. Use on mesh window wake or task dispatch.
---

Resolve the real window from `TMUX_PANE` or the explicit session identity; never adopt
another lane's identity to make a command pass. Read its node-local charter, falling
back to `charter/<window>.md` through `mesh-handoff --charter <window>`. The charter
defines this window's role; do not copy a roster or another window's duties here.

Read the prior handoff and the live data pane. Check current ledger state before
resuming: a restored completion is history, not new work. Read the complete
`mesh-task queue --dispatch --owner <window>` and choose eligible work that advances
the window's goal, including runnable prerequisites. A query failure means unknown,
not an empty queue. Use `mesh-task check dispatch <chain>/<step> <window>` before take.

For `tg` and `tg-roz`, an inbound message or eligible owned task is the wake reason.
Dashboard drift, outgoing reply display, periodic health reads, and context restoration
alone are not new work. Keep these lanes quiet until an event; retry only pending work.

Do the work, then prove it done. Definition of done for a turn — BOTH halves,
never one without the other:

- CODE: the behavior changed in an executable (script, test, config a live caller
  reads), or a plan naming the executables expected when implemented. A paragraph
  about the work is a receipt, not the artifact — receipts never settle
  implementation. (`mesh-task done` refuses prose for implementation steps;
  receipt-only steps must declare it with the exact tag.)
- OBSERVED CHANGE: the new state renders on a top pane and the owning mind
  observes it there — the result names the pane/role (`pane:<mesh-dash role>`).
  Deterministic gates wire into `mesh-doctor` so `.doctor-fails` carries them to
  the health pane; pane presence itself is asserted over the live panes, never by
  re-probing a render. An artifact no pane observes is waste.

Per lane, that conjunction means: delivery lane owes the receipt with destination
+ transport proof AND its effect visible where the lane is watched; code lane owes
verified behavior (`--test` green, red-then-green where the gate matters); sensor
lane owes a fresh real reading, not a cached or classified one. Every lane also
owes a settled ledger row (`mesh-task done`/`reject` with artifact) and a written
handoff — settlement without the two halves above is paperwork, not done.
- Observability: the change renders on a top pane and the owning mind observes it
  there — name the pane/role in the receipt. A verdict visible only in chat.log was
  never rendered. Deterministic gates wire into `mesh-doctor` so `.doctor-fails`
  carries them to the health pane; pane presence itself is asserted over the live
  panes, never by re-probing a render.

A turn with no artifact and no settled row is not done; it is started. If the work
cannot finish, persist a typed block with the exact next action and retry edge —
that is the honest incomplete state, not a done one.

Use `mesh-operator-followthrough` for operator work needing durable follow-through,
`mesh-task-recovery` for apparently stranded work, and `mesh-audit` for any audit,
review, or reconciliation that promises downstream task creation. Keep ownership
changes, board voice, substrate writes, landing, and final artifact verification in
this window; delegate only what is independently verifiable and record what you
personally inspected.
