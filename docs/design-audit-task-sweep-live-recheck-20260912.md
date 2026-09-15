# Design/audit sweep — post-closure live recheck, 2026-09-12

This is an addendum to the completed matrix at
`docs/design-audit-task-sweep-final-20260912.md`. It preserves the live ledger state observed after
the final task row closed; the matrix file itself remains unchanged as the task's completion
artifact.

## Task and ledger state

- `mesh-task status design-audit-task-sweep-20260907` reported the chain `complete (18/18)` and
  the final row DONE with the matrix artifact. A fresh `mesh-task audit` also classified that row
  DONE with the same artifact. The wider audit snapshot had 596 DONE, 111 REJECTED, 59 BLOCKED,
  51 QUEUED, 24 OPEN_UNOWNED, 2 RUNNING, 4 HELD_EXPIRED, 3 HELD_REJECTED, and 1 OVERDUE.
- A post-closure `mesh-promises --feed` exited 0. The immediately following
  `mesh-promises --check` exited 1: parity passed, promises agreed at 229/229 and claims at
  147/147, but holds disagreed at replay 60 versus journal balance 0. At that moment
  `~/.mesh/promises/promises.journal` was empty (0 bytes), and multiple `mesh-promises --check`
  processes were visible. A concurrent materialization race is plausible, but the evidence does
  not establish a cause.
- With no other feed/check process active, a serial `mesh-promises --feed` retry exited 0
  (`open=232`, `claim_open=147`, `hold_open=61`, `ask_open=66`). Its subsequent
  `mesh-promises --check` exited 0: parity passed, and all four replay balances agreed—promises
  232/232, claims 147/147, holds 61/61, asks 66/66. The roster still reports 5 unrouted promises,
  141 unrouted claims, and 5 unrouted holds. The successful retry restores this snapshot; it does
  not explain the preceding empty-journal interval.

## Other turn artifacts

- The requested fleet roll-call digest was posted to the board at 2026-09-12T05:09:27Z. It
  included 14/17 expected responders and named `tg`, `phaedra:genome`, and `phaedra:chat` silent
  after the 120-second grace. The final board re-scan preceded posting; no foreign-host roll-call
  lines were present.
- `mesh-wake-expect tg` was written at 2026-09-12T05:05:30Z with a 300-second TTL for the
  recurring witness/VPN roll-call FYI line shape (expired at 05:10:30Z). Task-ledger events and
  other lines were outside that pattern.

## Outstanding work

The sweep chain is complete. Remaining evidence to follow up is the time-sensitive
`test-mesh-promises-identity-integrity.sh` fixture documented in the matrix: its 2026-09-08 task
line is now beyond the 24-hour leak threshold, causing `mesh-promises --json` to exit 1 before the
fixture assertions. The global task audit backlog and unrouted promise liabilities above are also
still live; they are not claims of sweep-chain incompleteness.
