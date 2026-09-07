# Drift/close methodology and weekly extension

## Close rule

The pilot closes as `blocked` when any acceptance-critical control fails, a required arm is
unavailable, or the corpus boundary cannot support the stated estimand. A report may publish the
negative result only with the failed control, affected claims, raw artifact, and next experiment
visible. `not_run`, `blocked`, and `fail` are distinct states.

The headline table is generated from the evaluator JSON, not hand-entered prose. The claim matrix
is the reconciliation gate: no prose claim is publishable unless it names an artifact and a field or
check. Structural and lexical values remain separate from behavioral and model-update values.

## Weekly extension

The existing weekly structural series may continue independently using immutable snapshot IDs and
the same canonical file filter. Each weekly row must carry protocol digest, snapshot commit, raw
manifest digest, excluded-file counts, and a repeatability result. Weekly rows are descriptive
observations until the corpus lock, leakage controls, repository-stratified uncertainty, and held-out
behavioral evaluation pass. A weekly lexical movement must never be relabeled architectural drift.

## Close-to-next-run procedure

1. Resolve immutable commits and license evidence for at least one additional repository, then
   regenerate the corpus lock without network ambiguity.
2. Explain/remove the six duplicate blobs and rerun the leakage, near-duplicate, and split controls.
3. Add live prompt-only/shuffled/base controls plus behavioral, abstention, and calibration rows.
4. Install and preflight the pinned LoRA/QLoRA stack; if unavailable, retain a dated blocked receipt.
5. Recompute the report and matrix from raw rows, obtain an independent witness rerun, then refresh
   checksums.
