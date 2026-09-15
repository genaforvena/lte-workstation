# Wake pane charter check — 2026-09-14

The `wake` arm is present and renders the distillation lane. A current one-shot frame names
the finnegans-fake repository, `condent.py`, `paired.py`, `run-seed-spread.sh`, the scored
rungs, trained adapters, and whether a lane process is in flight. It includes the
`SCORED RUNGS` block and the val-loss anti-selector warning required by the charter.

## Verification

- `timeout 30 mesh-dash --test-fast` — exit 0 in 21.0s. The fast core passed, including
  the wake-pane smoke gate; witness viewport checks also passed.
- `timeout 60 mesh-dash --test` — exit 124 at the imposed 60s bound. The forage timeout
  gate and both witness-pane checks reported PASS before termination. This is an incomplete
  full-suite run, not a wake-pane failure; `scripts/mesh-dash` documents the deep full-suite
  runtime as 68–90s and separates it from the fast core.
- `mesh-dash --once wake` — exit 0; captured live frame at `2026-09-14T18:28:08Z`.
  It shows the lane path, harness/gate/replicate tools, no lane run in flight, scored rungs,
  trained adapters, and the val-loss warning. Capture SHA-256:
  `24fe7cb2ddbd3ba1b9239bd21e27b8b8e36a768711542629e692eea0aac44646`.

The score-refresh follow-up is tracked separately and capability-blocked because only
2625 MiB of the RTX 3060's 12288 MiB was free while three other live processes held the
remaining allocations; see `~/finnegans-fake/docs/runtime-score-live-validation-2026-09-14.md`.
