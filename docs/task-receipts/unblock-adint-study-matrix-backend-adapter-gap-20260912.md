# Study matrix backend and adapter dependency — 2026-09-12

This receipt applies to these adint-owned duplicate resolver rows:

- `unblock/bash/1a5d03de7dabf729/resolve` → `unblock/adint/b9a8802e931a7d30/resolve`
- `unblock/bash/224502755f9ff98e/resolve` → `unblock/adint/8b36c020c067fc00/resolve`
- `unblock/bash/420d6fa1ca0bcecb/resolve` → `unblock/adint/d5876cdfd3252dcb/resolve`
- `unblock/bash/45d63044c1071f5c/resolve` → `unblock/adint/ff68ff618cb983ea/resolve`
- `unblock/bash/4cee1a0e4c0d4b80/resolve` → `unblock/adint/d03bfaa2c5b97636/resolve`
- `unblock/bash/52c35560a08431b3/resolve` → `unblock/adint/2efe508c50b2779b/resolve`
- `unblock/bash/adb855c43ed83294/resolve` → `unblock/adint/b419a3832411efd6/resolve`

## Fresh finding

The old descriptions say the matrix runner/backend is absent. Current Tiny Fleet source has the
runner CLI and default `TransformersBackend` path. On 2026-09-12, its focused suite passed all 10
tests, including missing-adapter refusal without fallback; `--plan-only` emitted the registered 15
arm/seed rows. These checks verify the runner surface, not real model inference or training.

All five required adapters are still absent: `study-pooled`, `study-toy_passage_ppl`,
`study-executable_code`, `study-rated_style`, and `study-adversarial_safety`. The 2026-09-12T05:02Z
preflight saw an RTX 3060 with 4,481 MiB free and 1.2 GiB swap free. The run matrix was not
started; there are no artifacts to load, and resource suitability must be checked again after the
adapters are produced. All seven referenced adint parent rows still report `blocked`.

## Exact next action

The S06 owner must create the five registered adapter artifacts from the frozen study inputs and
record their training configurations, seeds, input hashes, output hashes, and resource/time data.
After that, perform a fresh non-destructive preflight and run the registered 15-row matrix. The
existing runner summary's `training_executed` field must also be corrected or explicitly resolved
before interpreting it: ordinary execution loads existing adapters and does not train them.
Until these conditions hold, keep the study work blocked and do not substitute the verification-only
fake backend for a scientific result.

No shared Tiny Fleet source, adapter, run root, or workload was changed. The shared worktree already
has uncommitted runner/S06 files.
