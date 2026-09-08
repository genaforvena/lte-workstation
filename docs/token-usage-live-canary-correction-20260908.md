# Token usage live canary correction (2026-09-08)

Task: `token-usage-accounting-implementation-20260908/token-live-canary`

The rejected canary identified that a timestamp-free event was normalized with a fresh current
time on every replay. The recorder now preserves `observed_at: null` when both source timestamps
are absent, so the normalized row is deterministic and replay remains idempotent. The parser
version is `token-usage-recorder-20260908.v2`.

Regression fixture: `tests/test-mesh-token-usage-recorder.sh` records and replays an event with no
`observed_at` or `received_at`, asserts `duplicate` on the second submission, asserts one stored
row, and asserts `observed_at` is JSON `null`.

Verification:

```text
tests/test-mesh-token-usage-recorder.sh
token-recorder-test: ok (record, privacy, permissions, duplicate, conflict, replay, quarantine)

tests/test-mesh-token-usage-reconciliation.sh
token-reconciliation-test: ok (match, non-additive, missing, mismatch, replay)

tests/test-mesh-token-usage-report.sh
token-report-test: ok (grouped coverage and missing fields)

python3 -m py_compile scripts/mesh-token-usage-recorder
SHA-256 scripts/mesh-token-usage-recorder = 3a3666c8fb859327f1ae4412fb6bba7f56a2d8954a88b2433714c19929e874c5
SHA-256 ~/.local/bin/mesh-token-usage-recorder = 3a3666c8fb859327f1ae4412fb6bba7f56a2d8954a88b2433714c19929e874c5
```

Verdict: corrected; timestamp-free replay is accepted as a duplicate rather than a conflict.
