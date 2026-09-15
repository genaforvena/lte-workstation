# Board tag and hledger coordination audit — 2026-09-12

Task: `design-audit-task-sweep-20260907/design-board-tags` (exact-owner `tg`, dispatch check exit 0).
Sources: `docs/design-board-tag-schema-2026-07-24.md` and `docs/design-hledger-coordination-2026-07-24.md`.

## Direction 1: board tags and query surface

| Design requirement | Current evidence | Disposition |
|---|---|---|
| Parse the trailing ` ; key:value` metadata tail on board lines. | `scripts/mesh-board-query` splits the body at ` ; ` and exposes the tags as fields. `scripts/mesh-board` routes `query` to that reader. Live query and focused reader tests passed (below). | **Implemented as a generic read-only board query.** |
| Make the promise/claim/hold replay prefer explicit `task`, `owner`, `prio`, and `status` tags, retaining prose derivation for legacy lines. | `scripts/mesh-promises` still documents prose-based address/owner matching and calls the explicit-tail reader path a future migration; it does not claim the specified exact task-tag pairing. `scripts/mesh-chat --help` has no `--task`/metadata-tail emission option. | **Not implemented in the hledger projection.** This is no longer a task-lifecycle requirement: the 2026-09-08 task-only decision makes structured task-state events the lifecycle authority. Do not add a second writable lifecycle to promises. Generic board tags remain useful to readers. |
| Provide the proposed `mesh-board` hledger query catalog (`open`, `owes`, `task`, `incidents`, `cost`, `leaks`, `count`). | `mesh-board` has compatibility views for open/count/owes/task/incidents and the generic `query` command. `mesh-promises` and `mesh-labor` remain direct accounting/report tools; this is not one complete wrapper over all three journals. | **Partly implemented as a compatibility/accounting surface; full catalog is not a current requirement.** |
| Replace dispatch's raw `[task]` count with the netted promise count. | `scripts/mesh-dispatch` reads `mesh-task queue --dispatch`; `~/.mesh/reflexes.cron` still wires its five-minute and chat.log-fsnotify invocations. `docs/task-only-coordination-20260908.md` defines tasks as actionable lifecycle and promises as accounting. | **Superseded by canonical task dispatch.** The dispatch backlog is the task queue, not `mesh-board count`. |

The schema's exact-match verification case (tagged open/done pair nets to zero without fuzzy matching) is **not evidenced and must not be represented as passing**. The generic reader tests prove metadata parsing/query behavior only. Legacy promise matching remains in use for compatibility accounting.

## Remaining directions in the July 24 coordination note

| Direction | Reconciliation |
|---|---|
| 2 — correlate labour with board activity to distinguish reflex from cron work | Reconciled by `docs/design-audit-labour-trigger-cron-20260912.md`: the old 25/30 one-window observation is not a fleet rate, board proximity is incomplete, and the proposed retrospective idle detector is declined as unidentifiable. The actionable low-yield wake issue has separate corrective artifacts and passing focused checks. No new task is warranted from the July correlation proposal. |
| 3 — merge `minds` into `witness`, then verify dispatch | Current `~/.mesh/restore.env` retires `minds` and `chat`; a live `tmux list-windows -a` likewise has neither window. The mind roster has since expanded beyond the original ten-window set. Current dispatch consumes the canonical task queue and remains wired by cron plus chat.log fsnotify; `mesh-dispatch --test` passed. The original 10-window roster is historical, not a constraint on today's expanded roster. |
| 4 — make `mesh-rns-sh` survive a link drop | `scripts/reticulum/mesh-rns-sh.sh` now contains bounded reconnect/backoff and serves interactive sessions under persistent tmux; `docs/reticulum-remote-shell.md` documents the delivered tool and local E2E `--test`. The July requirement to verify a real peer link drop is **not evidenced in this audit**; do not claim that acceptance from source inspection or the local round-trip test. |
| Tentative fourth “values” accounting axis | It was explicitly tentative and unscoped in the source. **Parked; no implementation or task is implied.** |

## Verification performed

- `python3 scripts/mesh-board-query --test`: PASS (metadata tags, envelope fields, boolean/contains/not-equal queries, count and no-match behavior). Its expected invalid-predicate diagnostic appeared inside the self-test.
- `bash tests/test-mesh-board-query-reader.sh`: PASS.
- `python3 scripts/mesh-task --test`: PASS (canonical task state, exact owner, lease/progress, typed block/resume, artifact hash, idempotent done).
- `bash scripts/mesh-dispatch --test`: PASS (structured task queue, priority/FIFO, dependency waits excluded).
- Read current dispatch source and `~/.mesh/reflexes.cron`: queue consumer plus five-minute cron and chat.log fsnotify wiring are present.
- Live generic board query returned 178 `owner=tg`, 2450 `marker=task`, and 40 `status=open` records at audit time. These are parser counts, not open-liability or task-queue counts.

No code or substrate configuration was changed by this audit. The open real-peer link-drop evidence remains separate from this completed reconciliation and must be checked before claiming that specific acceptance criterion.
