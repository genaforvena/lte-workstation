# Independent task pickup — 2026-09-12

The witness pane showed later steps as `QUEUED` while each chain's current head was `BLOCKED`. `mesh-task status` confirmed they were ordered successors, and their dispatch checks correctly refused them. That left no witness-owned claimable row even when a later task could be done without its blocked predecessor.

Added an explicit owner attestation:

```text
mesh-task independent <chain> <step> <reason>
```

The exact owner can use it only for a later, open, ungated step while the chain head is blocked. The reason is stored in canonical task-state records and shown in status, audit, the owner queue, the routed `[task]`, and the eventual `[taking]`. Such a step is reported as `READY_INDEPENDENT`; explicit `waiting_for` remains a hard gate, and ordinary ordered steps stay serial. Independent work can be progressed, blocked, resumed, rejected, or completed without moving the blocked head. When the head later completes, the chain advances across already completed independent steps.

The independent fixture test first failed because the command did not exist. After implementation, these checks passed:

- `python3 tests/test-mesh-task-independent-pickup.py` — owner check, default sequential refusal, explicit wait gate, queue/check/audit/status visibility, independent taking/progress/block/resume/done, blocked-head preservation, and later ordered completion.
- `python3 scripts/mesh-task --test` — embedded coordinator smoke test now includes the independent pickup path.
- `python3 -m py_compile scripts/mesh-task scripts/mesh_task_log.py tests/test-mesh-task-independent-pickup.py`.
- `tests/test-mesh-task-blocked-self-unblock.py` — 16 passed; `tests/test-mesh-task-dispatch-receipt.sh` and `tests/test-mesh-task-reschedule.sh` passed; `git diff --check` passed.

`tests/test-mesh-task-no-expiry.py` had 14 passing tests and two priority-order failures: both expect a task for an already-busy owner to appear in `queue --dispatch`. The same busy-owner filter is present in `HEAD`; it remains necessary for queue/check consistency.

Live deployment remains pending. `mesh-land` refused its candidate scan because the already-staged symlink `scripts/ux/chibicc/tests` is unclassified. I left that unrelated staged path untouched. The installed `~/.local/bin/mesh-task` and `mesh_task_log.py` are therefore still the pre-change copies; the implementation and isolated verification are in the source tree. The task-ledger autoland request will route the reviewed source files to genome.

Artifacts: `docs/superpowers/plans/2026-09-12-independent-task-pickup.md`, `docs/superpowers/plans/2026-09-12-independent-task-pickup.plan.tsv`, and `tests/test-mesh-task-independent-pickup.py`.
