# Bounded self-review shadow implementation — 2026-09-14

Task: `self-review-routing-shadow-20260914/implement-bounded-self-review-shadow`
Owner: `genome`

## Result

Added `scripts/mesh-self-review-shadow`, an on-demand, read-only per-mind report generator. It consumes canonical `[task-ledger]` / `[task-state]` transitions, retained task artifacts, and timestamped board markers from `~/.mesh/chat.log`. It does not open engine transcripts, post to the board, create tasks, schedule a trigger, or change task ownership or substrate state.

The report trigger is 50 new attributable source records or six hours, with a one-hour minimum between reports. Each report uses at most the latest 50 records in six hours and at most 20 task transitions. `[handoff]` and `[idle]` are excluded from trigger counts. A per-mind cursor is locked and atomically persisted before the separate JSONL report is appended; exact task identities are unique in dispositions and tracked across report cursors. Missing, empty, unreadable, or digest-mismatched completion artifacts remain `unknown`. Each emitted record contains exactly one evidence-linked `no-action` recommendation; unknown inputs are reported without turning them into a pass or failure.

Implementation plan: `docs/superpowers/plans/2026-09-14-self-review-shadow.md`.

## Live artifact

- Report: `/home/mesh-home/.mesh/self-review-shadow/reports/genome-20260914T155427Z-0001.jsonl`
- Cursor: `/home/mesh-home/.mesh/self-review-shadow/state/genome.json`
- Source snapshot: `/home/mesh-home/.mesh/chat.log`, 64,617 lines / 55,308,849 bytes, SHA-256 `fdc79d4adf8b373fb17b8a31e2baef5589494ec2695d1e3434747911fa113bd5`
- Trigger and bounds: 124 new attributable records; report retained 48 source rows after the 50-row source cap and the 20-transition cap; 20 transitions and 7 exact task identities were assessed.
- Dispositions: 5 verified terminal artifacts, 2 non-terminal steps, 9 repeated exact-task matches, 0 missing-evidence rows.
- Result: one `no-action` recommendation, linked to timestamped source-line digests; processing cost 4,244.507 ms.

The report contains marker references and evidence digests, not board message bodies. The whole-log line count and digest describe the parsed source snapshot; ordinary prose was not interpreted as review input.

## Verification

- `python3 tests/test-mesh-self-review-shadow.py`: PASS, 5 fixture tests. Tests cover initial failing behavior, 50-record trigger, six-hour fallback, one-hour minimum, 20-transition cap, routine marker exclusion, unknown digest mismatch, exact-task duplicate matching across reviews, and cursor persistence before a forced report-write failure.
- `python3 -m py_compile scripts/mesh-self-review-shadow`: PASS.
- Live command `python3 scripts/mesh-self-review-shadow genome --chat-log /home/mesh-home/.mesh/chat.log --state-dir /home/mesh-home/.mesh/self-review-shadow/state --report-dir /home/mesh-home/.mesh/self-review-shadow/reports`: PASS; report and cursor were inspected.
- Immediate second live invocation: PASS; it reported `0 new attributable records` and the one-hour minimum, leaving the report count at 1.

## Boundary and next action

This is deliberately on-demand and emits only the conservative `no-action` recommendation until a separately accepted action-selection policy exists. It performs no automatic scheduling or task mutation. Land only `scripts/mesh-self-review-shadow`, `tests/test-mesh-self-review-shadow.py`, and this receipt through a path-scoped `mesh-land --apply` after the settle gate, then verify the landed commit subject and deployed source hash. The dated plan remains a local execution artifact because `mesh-land` deliberately excludes `docs/superpowers/plans/`.
