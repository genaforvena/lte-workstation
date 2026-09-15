#!/usr/bin/env bash
set -u -o pipefail
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
card_rc=0
out="$(HOME=/home/mesh-home "$ROOT/scripts/mesh-card" --refresh 2>/dev/null)" || card_rc=$?
[ -n "$out" ] || { echo "primary-compute: FAIL (mesh-card produced no card)" >&2; exit 1; }
grep -qx '  compute: primary' <<<"$out" || {
  echo "primary-compute: FAIL (mesh-home is not advertised as primary compute)" >&2; exit 1;
}
echo "primary-compute: ok"
