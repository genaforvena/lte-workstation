#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
chmod +x "$ROOT/scripts/mesh-jev"
test -x "$ROOT/scripts/mesh-jev"

output="$($ROOT/scripts/mesh-jev --test)"
test "$output" = "PASS: mesh-jev offline validation"

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
if TYPESAFE_API_KEY= "$ROOT/scripts/mesh-jev" --evaluate </dev/null >"$tmp" 2>&1; then
  echo "expected missing-key failure" >&2
  exit 1
fi
grep -q 'TYPESAFE_API_KEY is not configured' "$tmp"
! grep -q 'Bearer' "$tmp"

echo "PASS: mesh-jev adapter"
