#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd -P)
for tool in mesh-cleaner-scan mesh-cleaner-settle mesh-cleaner-docs mesh-cleaner-receipt mesh-cleaner-dash; do
  "$root/scripts/cleaner/$tool" --test
done
test -f "$root/charter/cleaner.md"
echo 'test-mesh-cleaner: PASS'
