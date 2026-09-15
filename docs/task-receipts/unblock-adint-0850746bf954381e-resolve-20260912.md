# Resolver receipt: `unblock/bash/0850746bf954381e/resolve`

- Checked: 2026-09-12T05:02Z UTC
- Actor: `adint`
- Parent: `unblock/adint/5afe0d59ca2decdf/resolve`
- Disposition: the dispatch description is stale about the missing CLI/backend; current code and focused tests are present, but the real study remains blocked on five trained adapter artifacts.

## Fresh verification

In `/home/mesh-home/tiny-fleet`, `rtk proxy .venv/bin/python scripts/test_run_study_matrix.py`
passed all 10 tests, including the explicit refusal when a real adapter artifact is missing and
the bounded fake-backend smoke. `rtk proxy .venv/bin/python scripts/run_study_matrix.py
--registration runs/fleet-study-v1/registration.json --run-root runs/fleet-study-v1 --plan-only`
emitted the full 15-row registered plan (five arms × seeds 17, 29, 43). The runner's source
contains the default `TransformersBackend` path and calls `require_adapters` before model
execution.

All five required adapter directories are absent: `study-pooled`, `study-toy_passage_ppl`,
`study-executable_code`, `study-rated_style`, and `study-adversarial_safety`. At 05:02Z the RTX
3060 had 4,481 MiB free of 12,288 MiB; swap had 1.2 GiB free. No real matrix or training was run.
The default execution path has not been demonstrated with real adapters. The shared Tiny Fleet
worktree already contains uncommitted runner and S06 files, so this resolver made no source edits.

## Exact next action

The S06 owner must produce the five registered adapter artifacts from the frozen study inputs and
record their training provenance and hashes. Then perform a fresh non-destructive resource preflight
and run:

```bash
cd /home/mesh-home/tiny-fleet
rtk proxy .venv/bin/python scripts/run_study_matrix.py \
  --registration runs/fleet-study-v1/registration.json \
  --run-root runs/fleet-study-v1
```

Before accepting its output as a study result, correct or explicitly resolve the current runner
summary field that sets `training_executed` true on ordinary inference even though this path loads
existing adapters rather than training them. The resolver task's parent remains blocked; the
10-test pass and plan-only output are implementation/preflight evidence, not study results.

## Verification

- `rtk mesh-task check dispatch unblock/bash/0850746bf954381e/resolve adint` exited 0 before take.
- Focused tests: 10/10 passed.
- Plan-only: 15 registered rows emitted.
- Adapter directory presence check: all five missing.
- Fresh GPU/RAM/swap observation recorded above; no model, training, or matrix execution started.
