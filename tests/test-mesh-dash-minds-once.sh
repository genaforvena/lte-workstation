#!/usr/bin/env bash
set -euo pipefail

out="$(mktemp)"
trap 'rm -f "$out"' EXIT
if ! timeout 12s mesh-dash --once minds >"$out" 2>&1; then
  echo "FAIL: mesh-dash --once minds exceeded 12s"
  exit 1
fi
grep -q '^-- allocation: idle hands & unclaimed work' "$out" \
  || { echo "FAIL: minds frame missing allocation section"; exit 1; }
grep -q '^-- spend: where compute goes' "$out" \
  || { echo "FAIL: minds frame missing spend section"; exit 1; }
grep -q '^  gate: dispatch ' "$out" \
  || { echo "FAIL: minds frame missing explicit dispatch gate"; exit 1; }
echo "PASS: mesh-dash --once minds is bounded and renders allocation/spend state"
