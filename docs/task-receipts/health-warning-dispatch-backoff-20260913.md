# Health warning dispatch backoff — 2026-09-13

Live evidence showed `health-warning/4ffcd9cbfa5307a1234e/triage` failing board
dispatch every roughly 20 seconds. Each retry took the global `mesh-task` lock while
the task ledger was replayed/appended, delaying unrelated Health reconciliation and
other owners' transitions.

`mesh-health-warning-task` now persists a retry record per exact chain. A failed
dispatch backs off from five minutes with bounded exponential growth to one hour;
the next watcher pass records and honors the deadline rather than repeatedly taking
the ledger lock. A successful or terminal disposition clears that retry record.
The source cursor stays before the unresolved warning, so no incident is dropped.

Verification:

- `python3 tests/test-mesh-health-warning-task.py` covers a future persisted retry
  deadline (no dispatch) followed by an eligible deadline (one dispatch).
- `python3 scripts/mesh-health-warning-task --test`
- `git diff --check`

This change is pending with the witness autonomy branch and is not yet active in
the installed watcher. After landing, observe the live retry tape/state for the
exact `4ffcd9...` chain and verify unrelated ledger operations remain responsive.
