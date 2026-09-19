#!/usr/bin/env bash
set -euo pipefail

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
log="$td/light-attempts.log"

set +e
MESH_LIGHT_ATTEMPT_LOG="$log" timeout 45s mesh-light --edge >/dev/null 2>&1
rc=$?
set -e
[ "$rc" -eq 0 ] || [ "$rc" -eq 2 ] || {
  echo "mesh-light --edge returned unexpected rc=$rc" >&2
  exit 1
}
[ -s "$log" ] || {
  echo "mesh-light --edge did not emit one per-run attempt record" >&2
  exit 1
}
[ "$(wc -l < "$log" | tr -d ' ')" -eq 1 ] || {
  echo "expected exactly one attempt row" >&2
  exit 1
}
grep -Eq '^ts=[^ ]+ source=(phone|beacon|webcam|offline) rc=(0|2)$' "$log" || {
  echo "attempt row lacks honest source/exit fields: $(cat "$log")" >&2
  exit 1
}
echo "test-mesh-light-attempt-tape: PASS"
