# Autopoiesis origin-envelope implementation verification

Date: 2026-09-08
Chain: `autopoiesis-task-ledger-20260908`
Step: `implement-origin-envelope`

Integrated reviewed commits `d747a3a4` and `216e5f24` onto the readable `[task-ledger]` writer.

The active plan's explicit priorities were persisted through the canonical `reprioritize` command,
not by editing a cache: `100, 95, 90, 100, 95` in plan order. The same transition is owner-safe or
coordinator-safe (`MESH_TASK_COORDINATOR`, default `witness`) and appends a fresh readable snapshot.
The plan's `tags=design,autopoiesis` and `design_artifact=/home/mesh-home/lte-workstation/docs/design-autopoiesis-promise-ledger-20260908.md`
were then persisted on every existing step through the canonical `annotate` transition.

Implementation:

- `mesh-task create` accepts exactly `origin.kind`, `origin.source`, `origin.hypothesis`,
  `origin.question`, `origin.acceptance`, and `origin.feedback` plan headers.
- Replay validates the exact six non-empty string fields.
- `origin.source` is refused when already present in either an open or settled chain; the append
  path rechecks the canonical ledger under the writer lock so concurrent creators cannot both land.
- Plans without an origin envelope remain valid, and historical readable/legacy records replay.
- New plan headers `#tags=` and `#design_artifact=` are copied to every step. Existing chains use
  `annotate <chain> <step> <tags> <design_artifact>`, with the same owner/coordinator guard.
- `status`, dispatch queue rows, task receipts, and readable snapshots expose the tag and design
  artifact metadata.

Fresh verification:

```text
python3 -m unittest tests/test-mesh-task-log.py tests/test-mesh-task-no-expiry.py tests/test-mesh-promises-task-state.py
.....................
Ran 21 tests in 5.298s
OK
python3 tests/test-mesh-task-origin-envelope.py
PASS: origin envelope, refusal, duplicate status, legacy replay, and cache rebuild
bash tests/test-mesh-task-source-coverage.sh
test-mesh-task-source-coverage: PASS (all chat.log records replayed and hashed)
bash tests/test-mesh-task-autoland-task.sh
test-mesh-task-autoland-task: PASS
```

The focused origin test also passed the canonical new-chain header path and existing-chain annotation
path, including readable replay assertions and status/queue metadata assertions. Live replay confirms:

```text
implement-origin-envelope 100 design,autopoiesis
verify-origin-continuity 95 design,autopoiesis
run-literature-canary 90 design,autopoiesis
wire-autopoietic-producers 100 design,autopoiesis
verify-closed-loop 95 design,autopoiesis
```

`scripts/mesh-task` and `scripts/mesh_task_log.py` are deployed through `~/.local/bin` and have
matching SHA-256 values after `mesh-sync-tools --apply`:

```text
mesh-task       578e1682156fe4f765f9d7d4009b1e59e3fb9becf37756d977edf9940169b65f
mesh_task_log.py 4c47f31e69090b65dcd693526608441a1e55d39dfe026d9b7caeb9103e18f839
```

Landing commits: `bf2ca74d` and `ed9ee6a9`; `main` was pushed and matched `origin/main`.
