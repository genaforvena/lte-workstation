#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
out=$("$root/scripts/mesh-health" --test 2>&1)
printf '%s\n' "$out"
case "$out" in
  *'ok: SSH auth refusal is distinguished from transport failure'*) ;;
  *) echo 'FAIL: mesh-health --test did not verify SSH auth classification' >&2; exit 1 ;;
esac
