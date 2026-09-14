# Confirmatory-v1 scorer validator-binding review — 2026-09-14

Task: `tinyfleet-confirmatory-v1-scorer-binding-fix-20260914/review-validator-bound-scorer`

## Verdict

**PASS.** The pushed scorer bundle binds the imported generation validator to the amended scorer
and the frozen generation registration. The mutation regression rejects a changed registered
validator digest before the scoring path can request embeddings. Scoring remains gated on this
review's PASS.

## Independent evidence

- Reviewed commit `94c19d2a478bb8033419d39028f68528f0867283`. Local `HEAD`, local `origin/master`,
  and remote `origin` `refs/heads/master` all resolve to this commit. Its 11 added paths are scoped
  to the Tiny Fleet confirmatory-v1 plan, receipts, raw generation artifact, scorer amendment, and
  regression tests; `git diff-tree --check` reported no whitespace errors.
- `scripts/drift_score_confirmatory_v1.py::scorer_bundle_digest()` hashes `drift_generate.py`,
  `drift_score.py`, and the amended scorer. Independently recomputed bundle SHA-256:
  `f824ce755e1e7168ba302f961a4519e6878f677b2efd5618357f6abf768dba14`, matching the amendment.
- `verify_amendment()` requires the live `drift_generate.py` digest to equal both the amendment's
  `validator_source_sha256` and `generative-registration.json`'s `runner.source_sha256`, then checks
  the raw-tape, generation-registration, scorer, dependency, and bundle digests before `score_file()`
  parses records or calls `score_pairs()`.
- Confirmed hashes:
  - Frozen generation registration: `157fb3351366e656760ff17bb1a1379607fcc8d14fdc3a83037dbc338c265de7`
  - Raw tape: `b691c04b3a053c0fff8b6aefbc336fd0e61bd01de03453a76415c53e216bab5b`
  - Validator: `adc416a6e5d47b464c82b13d07b1cfffd0cd5e03c6a45a9f7772e51cfe4632c7`
  - Original scorer dependency: `54142ae236a6a55ff4452e360e2c6867e219b356d56f0ff4c589cd6fb8b8e127`
  - Amended scorer: `f5f01e9620c6073f3128b8c15a26a5e87bbebfcd1e08de6de510094f7b9c9114`
  - Scoring amendment: `f92f9acf77c18d629bb2f5b9ebbbfc34c609dd38a6e6bb9b61fdb8796b8e8eb7`
- The mutation test changes the manifest runner's validator digest and expects
  `validator_registration_mismatch`. Adapter-pair tests also check each snapshot's registered LoRA
  digest and allow distinct old/new digests.
- Reproduced both targeted suites from the pushed checkout: amended scorer **5/5 passed**; original
  scorer **7/7 passed**. `py_compile` passed for the amended scorer and its test module.
- The code path is bound to `runs/drift-confirmatory-v1/generative-registration.json` (the recorded
  hash above). The separate output manifest `execution-confirmatory-v1/manifest-v2.json` hashes to
  `77c70b6c381d486a341722d2cddddd2b56fd031a062157a35e5bfca42f68aafc`; it is not interchangeable
  with the frozen generation registration for the scorer's `--manifest` argument.

No scoring pass or embedding request was run. The raw tape was hashed but its generated text was
not inspected. The unrelated dirty files in the Tiny Fleet working tree were preserved.
