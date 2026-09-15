# Idle-turn cost follow-through correction verification — 2026-09-11

## Verdict

PASS. The corrected landed and deployed path suppresses no-candidate idle churn without suppressing
new exact-owner work or genuinely unpredicted pane/task changes.

## Behavioral verification

- `bash tests/test-mesh-pane-consume-task-aware-idle-gate.sh` — PASS. Its live-loop transition seam
  covers an expired expectation plus a changed fully-predicted frame (`HOLD:no-eligible`), the same
  expired state plus an unpredicted line (wake), empty→eligible (wake), eligible→empty (hold), and
  exact-owner candidate/wake-message validation with owner-authored `mesh-task take` instructions.
- `bash scripts/mesh-pane-consume --test` — PASS.
- `bash -n scripts/mesh-pane-consume tests/test-mesh-pane-consume-task-aware-idle-gate.sh` — PASS.
- The daemon loop calls `task_aware_transition_decision` whenever pane or candidate signatures
  change, persists `prev_candidate`, and advances pane/task baselines on both hold verdicts. This is
  the same seam exercised by the changed-frame regression, not the earlier unreachable same-frame
  helper branch.

## Wiring and landed artifacts

- Source and deployed executable SHA-256 both equal
  `44a44dd490c31a44dda3bed0ca681d61be638f26a222b063a33778647dd20c3a`.
- `41e9da17` contains corrected `scripts/mesh-pane-consume`.
- `025ef766` contains `tests/test-mesh-pane-consume-task-aware-idle-gate.sh`; no runtime copy exists
  in `~/.local/bin`.
- `9e512c6c` contains the correction implementation receipt and `83644e60` contains the independent
  prelanding review. All four commits are ancestors of both local `HEAD` and `origin/main`.
- The four correction paths are clean in `git status`.
- Canonical board history contains owner-authored `[taking]` transitions for the genome correction
  step; dispatch alone was not treated as start evidence.

The accidental unrelated landing encountered during closure was separately recovered and verified
by completed chain `idle-turn-cost-followthrough-mislanding-20260911`; its resolver-test content is
preserved as dirty mode-644 work for its real owner.

