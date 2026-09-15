#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SWAP="$ROOT/scripts/mesh-model-swap"

[[ -x "$SWAP" ]] || {
  echo "FAIL: mesh-model-swap implementation is missing or not executable"
  exit 1
}

out="$(bash "$SWAP" --test 2>&1)" || {
  echo "$out"
  echo "FAIL: mesh-model-swap --test rejected its real temp-copy refusal/restore gate"
  exit 1
}

grep -qF 'red refusal rc=' <<<"$out" || {
  echo "$out"
  echo "FAIL: --test did not prove a bad model is refused"
  exit 1
}
grep -qF 'restored=yes' <<<"$out" || {
  echo "$out"
  echo "FAIL: --test did not prove the marked line was restored"
  exit 1
}
grep -qF 'smoke-test: ok' <<<"$out" || {
  echo "$out"
  echo "FAIL: --test did not finish green"
  exit 1
}

printf '%s\n' "$out"
