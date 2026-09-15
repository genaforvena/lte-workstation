# Independent review: confirmatory-v1 scorer amendment

Reviewed: 2026-09-14T11:48:06Z  
Task: `tinyfleet-confirmatory-v1-scorer-compat-20260914/independently-review-scorer-amendment`  
Verdict: **FAIL — scoring gate remains closed.**

## Scope and live state

The review task was open, dispatched to `witness`, and then taken at 11:44:04Z. Its implementation prerequisite is recorded DONE with artifact `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-confirmatory-v1-scorer-amendment-20260914.md`. The comparison task's execution step was still queued with `waiting_for=tinyfleet-confirmatory-v1-scorer-compat-20260914/independently-review-scorer-amendment` during this review.

I did not edit the tiny-fleet scorer, tests, registration, raw tape, or amendment. I did not invoke embeddings or score records, and no score output exists in the execution directory. The tape was parsed in memory for schema/provenance validation; generated output text was not printed or reviewed.

## Evidence checked

- Current generation-registration SHA-256 is `157fb3351366e656760ff17bb1a1379607fcc8d14fdc3a83037dbc338c265de7`, matching the amendment.
- Current raw 162-record tape SHA-256 is `b691c04b3a053c0fff8b6aefbc336fd0e61bd01de03453a76415c53e216bab5b`, matching the amendment.
- Current original scorer SHA-256 is `54142ae236a6a55ff4452e360e2c6867e219b356d56f0ff4c589cd6fb8b8e127`, matching both the registration and amendment.
- Current amended scorer SHA-256 is `32758b98d34583d5ed9bc11cece02d2d68e761197085cccd7bdf99b780d369f8`; amendment SHA-256 is `61562c634e2667925f6c3f1d29ddc1aef4198d7d7b716a03b1dd1c6afd180ed4`.
- The registered runner source SHA matches the current `scripts/drift_generate.py` SHA (`adc416a6e5d47b464c82b13d07b1cfffd0cd5e03c6a45a9f7772e51cfe4632c7`). Calling the amended pairing validator on the actual tape validated all 162 records into 81 pairs, including 27 LoRA pairs whose registered old/new adapter digests differ.
- The amendment tests passed (4 tests), the legacy scorer tests passed (7 tests), and `py_compile` passed for the amended scorer and test module.
- The amendment correctly labels cosine as embedding similarity rather than semantic ground truth and states that objective labels are not behavioral or semantic truth. The frozen registration still has `comparison_authorized: false`; this review does not change that scope boundary.

## Reasons the gate fails

1. `scripts/drift_score_confirmatory_v1.py:11` imports `validate_v2_records` from `scripts/drift_generate.py`, and that validator determines whether raw records match the registration. But `scorer_bundle_digest()` at lines 29–33 hashes only the amended scorer and `drift_score.py`. `verify_amendment()` does not verify the imported validator against `manifest.runner.source_sha256`. The current validator happens to match the registered hash, but after it changes, amendment verification and the scorer bundle digest can still pass while scoring uses different record-validation logic. Bind and verify this dependency (or an equivalent immutable validator), and add a regression that refuses a changed validator digest before scoring.
2. The amended scorer, its tests, the scoring-amendment JSON, and its implementation receipt are still untracked in `/home/mesh-home/tiny-fleet` (`git status` reports `??` for each). The implementation is therefore not landed or pushed as required by the repository's Tiny Fleet update rule, and its “frozen” state currently rests only on mutable local files and hashes.

## Required retry

Keep `tinyfleet-confirmatory-v1-comparison-20260914/execute-confirmatory-v1-generative-matrix` queued/typed-blocked. Haunt should bind the generation validator into the scorer's verified code identity, add the mutation regression, and commit and push the scoped implementation artifacts. Witness should then re-check current hashes and tests and publish a fresh PASS before any scoring starts. The exact raw tape and registration remain unchanged in this review.
