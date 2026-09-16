#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd -P)
for tool in mesh-cleaner-scan mesh-cleaner-docs mesh-cleaner-receipt; do
  "$root/scripts/cleaner/$tool" --test
done
dash_out="$($root/scripts/cleaner/mesh-cleaner-dash --test)"
grep -q 'actionable=' <<<"$dash_out"
settle_out="$($root/scripts/cleaner/mesh-cleaner-settle --test)"
grep -q 'quarantine=' <<<"$settle_out"
test -f "$root/charter/cleaner.md"
echo 'test-mesh-cleaner: PASS'
