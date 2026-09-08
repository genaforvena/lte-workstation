# Token usage reporting (2026-09-08)

Task: `token-usage-accounting-implementation-20260908/token-reporting`

Added `scripts/mesh-token-usage-report`, a read-only report grouped by window and model. It emits
row counts and aggregate missing-field counts for the five normalized usage fields. It has no
budgets, thresholds, alerts, routing, scoring, or enforcement.

Verification: `tests/test-mesh-token-usage-report.sh` → `token-report-test: ok (grouped coverage and missing fields)`;
`python3 -m py_compile scripts/mesh-token-usage-report` → exit 0.
