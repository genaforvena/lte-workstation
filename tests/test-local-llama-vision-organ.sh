#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
organ="$repo/scripts/mesh-llama-vision"

[[ -x "$organ" ]] || { echo "test-local-llama-vision-organ: FAIL (organ is not executable)" >&2; exit 1; }
bash -n "$organ"
help="$($organ --help)"
grep -q -- '--test' <<<"$help"
grep -q -- 'LLAMA_SERVER_URL' <<<"$help"
printf '%s\n' 'test-local-llama-vision-organ: PASS (entrypoint and documented test contract)' 
