# Ledger-driven task dispatch plan audit — 2026-09-12

## Verdict

The 2026-09-06 plan's hledger-first dispatch architecture is superseded by the tasks-only
coordination decision recorded in `docs/task-only-coordination-20260908.md`: every actionable item
has one task identity and lifecycle in append-only `chat.log`; promise balances are an accounting
view, not a second dispatch queue. This is confirmed by current production code. The plan is now
marked superseded at its top so its unchecked implementation steps are not mistaken for current
requirements.

`mesh-promises` is not wholly removed: it still materializes accounting views and `mesh-board`
supports legacy open promise rows. Dispatch eligibility itself comes from structured task state.

## Integration checked

- `scripts/mesh-task` declares task-state records authoritative and exposes
  `queue --dispatch [--owner <mind>]`; it selects the current open step, preserves ordering and
  dependencies, and supports exact-owner filtering.
- `scripts/mesh-dispatch` production flow reads `mesh-task queue --dispatch` and refuses when that
  query is unavailable. Its smoke test calls the task authority self-test and validates queue rows.
- `scripts/mesh-board open --dispatch` remains an hledger/accounting compatibility surface that
  merges legacy open balances with current canonical task steps. It is not the production dispatch
  source.
- `docs/task-only-coordination-20260908.md` explicitly states that promises are not independently
  dispatchable and that task records are the lifecycle authority.

## Residual compatibility gap

`tests/test-mesh-dispatch-hledger-gate.sh` fails because it still expects a synthetic
`mesh-promises` feed failure to block the dispatcher. That assertion targets the superseded
hledger-first architecture. The live dispatcher no longer invokes that feed; its current guard is
the canonical `mesh-task` queue. Keep the old test visible as stale compatibility coverage until it
is retired or rewritten to exercise task-queue failure. No dispatch implementation change is
recommended by this audit.

Tags recorded on the task: `superseded-by-tasks-only,stale-hledger-gate`.

## Verification

- `python3 scripts/mesh-task --test`: PASS.
- `mesh-task queue --dispatch --owner tg`: PASS; exact-owner query returned the current eligible
  `spec-uxn-predicate` step after this audit task was claimed.
- `mesh-dispatch --test`: PASS (structured task authority, priority/FIFO order, dependency waits
  excluded).
- `tests/test-mesh-board-query-reader.sh`: PASS.
- `tests/test-mesh-board-id-markdown.sh`: PASS.
- `tests/test-mesh-dispatch-hledger-gate.sh`: FAIL, as expected for the stale hledger-feed contract.
- `mesh-promises --check`: accounting parity and replay agreement passed during the run; roster
  reporting listed 21 unrouted legacy promise rows. This does not alter the task-state dispatch
  verdict.
- The plan's documented `bash scripts/mesh-board --test` and `bash scripts/mesh-task --test`
  commands are invalid for these Python entry points; the actual task self-test is
  `python3 scripts/mesh-task --test`. `mesh-board` currently has no `--test` entry point.

No runtime task/dispatch defect was found in the tasks-only path. Remaining work is to update or
retire the stale hledger-feed test and keep the historical plan's status visible.
