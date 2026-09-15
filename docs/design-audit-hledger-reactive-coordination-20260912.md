# Hledger reactive coordination design audit — 2026-09-12

Audited `docs/superpowers/specs/2026-07-24-hledger-reactive-coordination-design.md` against the
current task source, materialized witness journal, dispatch path, accounting tools, witness pane,
and live cadence. Verdict: the proposed hledger-centered reactor architecture was superseded by the
task-only coordination decision. Hledger remains in the mesh as an accounting view and labour meter;
it is not the actionable task lifecycle or production dispatch authority.

## Current contract and live evidence

- `scripts/mesh-task` declares task-state records in `chat.log` authoritative and JSON chain files
  derived. Its dispatch queue is `mesh-task queue --dispatch`; exact-owner filtering and eligibility
  checks are exposed in the CLI.
- `scripts/mesh-task-journal` replays those source records into `~/.mesh/tasks.journal`. The live
  witness frame at 2026-09-12 02:16 UTC reported `task_source=PASS`, 52,923 source and replayed
  events, zero source errors, and 783 task rows (189 unfinished, 109 rejected, 485 done).
- `scripts/mesh-dispatch` remains the production push dispatcher. The live `~/.mesh/reflexes.cron`
  has it at `3-59/5 * * * *` and also invokes it from chat.log fsnotify. The dispatcher's current
  source reads `mesh-task queue --dispatch`. Its status pass at 02:15 UTC found 81 open tasks and
  zero idle workers, so it dispatched nothing on that pass.
- The witness pane composes the task journal and a live rolling-five-hour labour tree from
  `mesh-labor --balance --rolling`. It does not show the proposed `debt:wiring` balance or a
  `board.journal` view.
- `scripts/mesh-promises` explicitly says new coordination work must use `mesh-task`/`tasks.journal`;
  promise/claim/hold journals remain accounting and leak-detection compatibility views. A live
  `mesh-promises --check` at 02:16 UTC passed parity and replay-to-hledger agreement for promises
  (264), claims (145), holds (65), and asks (66). It also reported five promise rows owned by
  non-roster windows under `liabilities:promises:unrouted`; that accounting warning does not change
  task dispatch authority.
- `scripts/accounts.journal` remains the declared accounting chart, but its own comments say the
  declared accounts are not the window census; live windows are unioned at runtime. This differs
  from the spec's proposed chart-as-roster contract.
- No `mesh-board-journal`, `mesh-board-reactor`, or `mesh-reactor-watchdog` source exists under
  `scripts/`, and no corresponding unit/reflex wiring appeared in the inspected cadence file. The
  five-minute dispatcher is still wired, so the spec's prerequisite “see watchdog red before
  removing cron” migration did not occur.

## Component disposition

| 2026-07-24 component | Current disposition |
|---|---|
| Board grammar and `mesh-chat --lint` | Not the current lifecycle authority; structured task-state records and `mesh-task` own task transitions. |
| Chart of accounts as the window roster | Superseded: accounts are accounting declarations; live-window roster is derived separately. |
| `mesh-board-journal` transforming marker posts | Superseded by `mesh-task-journal` replaying structured task-state events to `tasks.journal`; `mesh-promises` materializes separate compatibility accounting. |
| `mesh-board-reactor` as task wake/router | Superseded: `mesh-dispatch` remains cron/fsnotify wired and consumes the canonical `mesh-task` queue. |
| Reactor/watchdog pair replacing mind-call cron | Not implemented; existing dispatch cadence remains present. |
| Wiring-debt PROMISEs for every declaration | Not present in the witness output inspected here; the proposed `debt:wiring` surface is not part of the current task journal contract. |
| Migration removing cron after shadow/red tests | Not reached; current cron and fsnotify dispatch paths remain active. |

The July spec should remain in the repository as design history. Its top now points to this audit and
warns that its unchecked phases are not current requirements. No architecture or substrate change was
made by this audit.

## Verification

- `python3 scripts/mesh-task --test`: PASS.
- `mesh-task-journal --test`: PASS.
- `mesh-dispatch --test`: PASS; summary covered structured task authority, priority/FIFO ordering,
  and dependency-wait exclusion.
- `mesh-promises --check`: PASS for accounting parity and replay agreement across all four families;
  the five unrouted promise rows remain a reported accounting condition.
- `mesh-witness --pane --embed`: rendered the current labour tree and full `tasks.journal` view.
- Read-only source/cadence inspection confirmed the canonical task queue dispatch path and the still-
  wired five-minute cron/fsnotify routes.

The unresolved work is not to resurrect the July reactor design. Any future coordination change must
start from the task-only authority and separately specify a tested replacement for the current
dispatch reflex before removing its cadence.
