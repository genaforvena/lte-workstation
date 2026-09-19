#!/usr/bin/env bash
set -euo pipefail

out_senses="$(mktemp)"
trap 'rm -f "$out_senses"' EXIT
if ! timeout 10s mesh-dash --once senses >"$out_senses" 2>&1; then
  echo "FAIL: mesh-dash --once senses did not complete within 10s"
  exit 1
fi
grep -q '^-- sense-reflex liveness' "$out_senses" \
  || { echo "FAIL: senses frame missing reflex-liveness section"; exit 1; }

echo "PASS: mesh-dash --once senses completes and renders the full sense frame"
