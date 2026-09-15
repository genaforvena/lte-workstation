#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

log="$tmp/render-verdicts.tsv"
mesh="$tmp/mesh"
mkdir -p "$mesh"

record() {
  MESH_DIR="$mesh" SR_VERIFY_LOG="$log" "$repo/scripts/mesh-sound-reflex" \
    --verify-outcome "$1" "$2" "$3" "$4" "$5"
}

# A verdict is durable even when the mutable records corpus is absent.
record abc123 drop pass "amc l 120 nofill" "verified=pass"
record def456 drop reject "amc l 130 nofill" "verified=reject reason=dead-gaps"
record ghi789 ext unverified "amc l 140 nofill" "verified=unverified"

[ "$(wc -l < "$log")" -eq 3 ]
grep -F $'abc123\tdrop\tpass\tamc l 120 nofill\tverified=pass' "$log" >/dev/null
grep -F $'def456\tdrop\treject\tamc l 130 nofill\tverified=reject reason=dead-gaps' "$log" >/dev/null
grep -F $'ghi789\text\tunverified\tamc l 140 nofill\tverified=unverified' "$log" >/dev/null

# Missing tape rows remain unknown; they are never silently promoted to shipped/pass.
if grep -qF $'\tmissing\t' "$log"; then
  echo "FAIL: a missing verdict row was treated as shipped" >&2
  exit 1
fi

echo "ok: append-only verify tape preserves pass/reject/unverified and leaves missing unknown"
