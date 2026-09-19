#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh/knowledge"
: > "$td/.mesh/study.log"
: > "$td/.mesh/ideas-queue"
: > "$td/.mesh/chat.log"

for n in $(seq 1 381); do
  printf 'capability fixture %03d\n' "$n" >"$td/.mesh/knowledge/capability-old-2026-08-$(printf '%02d' "$(( (n % 28) + 1 ))")-${n}.md"
done
printf 'newest\n' >"$td/.mesh/knowledge/capability-new-20260919.md"
printf 'middle\n' >"$td/.mesh/knowledge/capability-mid-2026-09-18.md"

out="$td/out"
if ! timeout 10s env HOME="$td" MESH_DIR="$td/.mesh" MESH_DASH_FAST=1 \
    bash "$ROOT/scripts/mesh-dash" --once discover >"$out" 2>&1; then
  echo "FAIL: discover one-shot exceeded 10s or exited non-zero"
  exit 1
fi
grep -q '^mission: ' "$out" || { echo "FAIL: discover frame missing mission"; exit 1; }
grep -q '^-- FRONTIER: recent capability finds (apply targets) --' "$out" \
  || { echo "FAIL: discover frame missing FRONTIER"; exit 1; }
mapfile -t rows < <(sed -n '/^-- FRONTIER: recent capability finds/,${/^  capability-/p;}' "$out")
[ "${#rows[@]}" -eq 2 ] || { echo "FAIL: expected two frontier rows, got ${#rows[@]}"; exit 1; }
case "${rows[0]}" in
  *capability-new-20260919.md) : ;;
  *) echo "FAIL: newest filename-date was not first: ${rows[0]}"; exit 1 ;;
esac
case "${rows[1]}" in
  *capability-mid-2026-09-18.md) : ;;
  *) echo "FAIL: second filename-date was not next: ${rows[1]}"; exit 1 ;;
esac
echo "PASS: discover one-shot handles 383 capability fixtures within 10s and preserves filename-date ordering"
