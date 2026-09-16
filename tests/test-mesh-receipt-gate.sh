#!/usr/bin/env bash
# test-mesh-receipt-gate: the receipt gate passes working artifacts,
# holds proof-of-work-only files, and skips non-receipt paths.
set -uo pipefail
cd "$(dirname "$(readlink -f "$0")")/.." || exit 1
fail=0
scripts/mesh-receipt-gate --test || fail=1
# Live corpus probes: a known stale triage must HOLD, a durable-evidence receipt must PASS.
out="$(scripts/mesh-receipt-gate task-receipts/health-warning-f400f1983d2a35a7d257-triage-20260915.md 2>&1)" \
  && { echo "FAIL: stale triage passed the gate: $out"; fail=1; }
out="$(scripts/mesh-receipt-gate docs/task-receipts/06-durable-evidence-receipt-20260908.md 2>&1)" \
  || { echo "FAIL: durable-evidence receipt held: $out"; fail=1; }
[ "$fail" = 0 ] && echo 'test-mesh-receipt-gate: PASS (gate --test green; stale triage HOLDs; evidence receipt PASSes)'
exit "$fail"
