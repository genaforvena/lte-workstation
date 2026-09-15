#!/usr/bin/env bash
# Regression for the bounded genetic schedule search in the vendored Uxn compiler.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
uxn="$root/scripts/uxn"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

"$uxn/build.sh" --chibicc >/dev/null
cc -I "$uxn/chibicc" -I "$uxn/chibicc/lib" -P -E -x c \
  "$uxn/chibicc-eval/lease-gate.c" -o "$tmp/lease-gate.i"

"$uxn/bin/chibicc" -O1 "$tmp/lease-gate.i" > "$tmp/o1.tal"
"$uxn/bin/chibicc" -O2 "$tmp/lease-gate.i" > "$tmp/o2-a.tal"
"$uxn/bin/chibicc" -O2 "$tmp/lease-gate.i" > "$tmp/o2-b.tal"

cmp -s "$tmp/o2-a.tal" "$tmp/o2-b.tal" \
  || { echo 'genetic superoptimizer is not deterministic' >&2; exit 1; }

o1_tokens="$(wc -w < "$tmp/o1.tal")"
o2_tokens="$(wc -w < "$tmp/o2-a.tal")"
[ "$o2_tokens" -le "$o1_tokens" ] \
  || { echo "genetic superoptimizer regressed token count: O1=$o1_tokens O2=$o2_tokens" >&2; exit 1; }

echo "test-uxn-genetic-superoptimizer: PASS (deterministic, O1 tokens=$o1_tokens, O2 tokens=$o2_tokens)"
