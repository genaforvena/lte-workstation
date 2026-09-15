#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

out="$td/outcome.log"
grep -q '^# orphan-ok: owner-routed acceptance consumer;' "$root/scripts/mesh-chaos-consumer"
MESH_CHAOS_CONSUMER_OUTCOME="$out" \
  "$root/scripts/mesh-chaos-consumer" --owner mesh-chaos-emu/genome --run

grep -q '^owner=mesh-chaos-emu/genome$' "$out"
grep -q '^subject=scripts/mesh-chaos-emu$' "$out"
grep -q '^attempt=1 transition=retry rc=75$' "$out"
grep -q '^attempt=2 transition=retry rc=75$' "$out"
grep -q '^attempt=3 transition=recovered rc=0$' "$out"
grep -q '^final_rc=0$' "$out"
grep -q '^attempts=3$' "$out"
test -s "$out"

if "$root/scripts/mesh-chaos-consumer" --run >/dev/null 2>&1; then
  echo 'missing owner unexpectedly accepted' >&2
  exit 1
fi

echo 'test-mesh-chaos-consumer: PASS (owner-routed consumer drives isolated fail-first/recovery artifact)'
