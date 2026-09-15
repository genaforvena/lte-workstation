# Witness task priority ordering verification — 2026-09-08

## Contract

The dispatch queue orders claimable current tasks by the shared `mesh-task`
ordering key: `priority:incident` first, then numeric priority descending, then
the dispatch/queue creation timestamp oldest first, with the task id as the
stable tie-breaker. The witness task pane is materialized from `mesh-task audit`
and must preserve that order for queue-eligible unfinished rows.

## Live evidence

At 2026-09-08T10:55Z:

- `mesh-task queue --dispatch` emitted 18 claimable rows.
- `~/.mesh/tasks.journal` contained 168 unfinished rows.
- Filtering the pane rows to the 18 claimable task ids produced the exact same
  sequence as the dispatch queue; the comparison exited 0.
- The first five ids in both sequences were:
  `recreated-rejected-20260908-08/plans-sound-collage`,
  `recreated-rejected-20260908-09/spec-sound-pane-records`,
  `recreated-rejected-20260908-12/freeze-independent-repository-sample`,
  `recreated-rejected-20260908-13/dispatch-corpus-contract`, and
  `recreated-rejected-20260908-14/standalone-drift-extraction`.
- The new landing chain
  `autoland-human-readable-task-ledger-20260908/land-define-readable-ledger`
  is priority `0`, dispatched to `genome`, and appears after older priority-0
  work, satisfying same-priority oldest-first ordering.

## Verification commands

```text
python3 tests/test-mesh-task-no-expiry.py                         -> 7 tests OK
bash tests/test-mesh-witness-task-queue-fit.sh                    -> PASS
python3 scripts/mesh-task --test                                 -> PASS
bash scripts/mesh-task-journal --test                             -> PASS
live queue/pane sequence comparison                              -> PASS
```

The source and installed `mesh-task` hashes differ because the installed copy
lacks the newer origin-envelope parser; the priority/audit/dispatch ordering
code paths are identical. `mesh-task-journal` source and installed hashes
match. This deployment drift remains an independent wiring obligation.
