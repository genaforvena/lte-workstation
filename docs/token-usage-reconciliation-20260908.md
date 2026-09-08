# Token usage reconciliation (2026-09-08)

Task: `token-usage-accounting-implementation-20260908/token-reconciliation`

Implemented `scripts/mesh-token-usage-reconcile`, a read-only verifier for normalized recorder
rows. It compares provider `total` with `input + output`; `cached_input` is checked as a subset of
input and `reasoning` as a detail of output, so neither is added again. Missing required values are
reported as `missing`, arithmetic or non-additive violations as `mismatch`, and valid rows as
`pass`. The JSON report is deterministic, making identical replay input byte-identical.

The verifier is informational only: it has no budget, threshold, alert, routing, scoring, stopping,
or callback integration.

Verification:

```text
tests/test-mesh-token-usage-reconciliation.sh
=> token-reconciliation-test: ok (match, non-additive, missing, mismatch, replay)
python3 -m py_compile scripts/mesh-token-usage-reconcile
=> exit 0
```
