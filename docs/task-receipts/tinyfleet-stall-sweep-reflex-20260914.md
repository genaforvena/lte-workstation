# Tiny Fleet witness stall-sweep landing — 2026-09-14

Task: `tinyfleet-stall-sweep-reflex-20260914/land-stall-sweep`  
Owner: `genome`

## Change

Landed `scripts/mesh-witness-stall-sweep` and its disposable-ledger regression test. The sweep clears
only provably dead waits and nudges the exact owner when a blocked task's named prerequisite is DONE;
the integration fixture verifies both actions and retry throttling without touching the live mesh.

## Verification and landing

- `rtk python3 scripts/mesh-witness-stall-sweep --test` — exit 0 (predicate checks, no subprocess or
  mesh access).
- `rtk python3 tests/test-mesh-witness-stall-sweep.py` — exit 0 (1 end-to-end test, temporary ledger).
- `rtk /home/mesh-home/.local/bin/mesh-witness-stall-sweep --test` — exit 0.
- `rtk git diff --check HEAD~2..HEAD -- scripts/mesh-witness-stall-sweep tests/test-mesh-witness-stall-sweep.py`
  — exit 0.
- MeshLand landed the source as `21d5dfb9` (`mesh-land: add dead-park cleanup and satisfied-retry
  nudges to the stall sweep`) and the test as `0918808e` (`mesh-land: add temporary-ledger regression
  coverage for stalled-task recovery`). At verification, local `HEAD` and `origin/main` both resolved
  to `0918808e6c7d961ec672f773b6279b6f2d28a323`.
- Source and deployed script SHA-256 both equal
  `58575c4f465dad96ae94dd0a8750729544faec0579f3632b0babc2d23fb70c6a`.
- The pre-landing crontab had no stall-sweep entry. `rtk mesh-autowire` completed with exit 0; the
  resulting crontab contains line 363:
  `*/15 * * * * $HOME/.local/bin/mesh-witness-stall-sweep --run >> $HOME/.mesh/witness-stall-sweep.log 2>&1   # autowired 2026-09-14`.
- MeshLand reported 661 unrelated staged paths and left them staged; its path-limited commits contain
  only the named source and test.
