#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
tool="$root/scripts/mesh-rules"
out="$($tool --check "$root/MESH.md")"
grep -Fq 'mesh-rules: PASS' <<<"$out"
if "$tool" --check <(printf '%s\n' '- `mesh:1` — one' '- `mesh:1` — duplicate') >/dev/null 2>&1; then
  echo 'FAIL: duplicate rule IDs accepted' >&2
  exit 1
fi
echo 'test-mesh-rules-cli: PASS'
