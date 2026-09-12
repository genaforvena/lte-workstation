# Resolve paired-project DNA dependency — 2026-09-12

The exact blocker is satisfied: `tinyfleet-expansion-20260912/behavior-controls-and-lora-preflight`
reached owner-authored `DONE` at 2026-09-12T09:09:01Z. Its artifact is
`docs/tiny-fleet-artifacts-20260912/behavior-controls/README.md` (SHA-256
`5bf2f4e23bce1da015ab0d19d612fea384d54cfc61fbef29c9fca9c60fb615cf`). The LoRA/QLoRA arm remains
explicitly BLOCKED because `torch`, `transformers`, and `peft` are unavailable; the prerequisite was
step completion, not successful adapter training.

After that completion, the task ledger released
`tinyfleet-operator-ideas-20260912/paired-project-dna-snapshots` back to dispatch. Both of its stated
prerequisites are satisfied: the exact BbyWVY-360M baseline was reproduced at revision
`154a243ffa13d3259a824c40a23d709d3ea42fa7`, and the expansion preflight step is DONE. The paired
study must preserve the blocked genuine-update arm; it may run only the pinned base and retrieval
controls until real weight-update dependencies and artifacts exist.

Current structural inputs have at least two immutable local commits: the corpus lock's
`e8f47364e5a0f224c1bd03331df592272a187df5` (2026-09-07) and current `HEAD`
`5686c478ee3a496a6c87e54791bb026128fa9e2b` (2026-09-12). They are distinct commits. The downstream
step must retain both identifiers and raw outputs, and must not treat the single-snapshot-per-repo
corpus lock as a paired temporal result.

Resolution: resume the original task for a bounded two-snapshot control run, carrying the genuine
update arm as BLOCKED. No external corpus was fetched and no model/package configuration was
changed.
