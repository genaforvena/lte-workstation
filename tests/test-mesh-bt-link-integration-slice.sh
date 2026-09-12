#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
shim="$repo/scripts/mesh-bt-link"
implementation="$repo/scripts/integrations/mesh-bt-link"
tmp=$(mktemp -d -t mesh-bt-integration.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$implementation" ] || {
  echo 'BT integration: implementation is not in integrations/' >&2
  exit 1
}
[ -x "$shim" ] || {
  echo 'BT integration: compatibility entrypoint is not executable' >&2
  exit 1
}

manifest="$tmp/manifest.tsv"
"$repo/scripts/mesh-manifest" --list > "$manifest"
python3 - "$manifest" <<'PY'
import csv
import sys

with open(sys.argv[1], newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader((line for line in stream if not line.startswith("#")), delimiter="\t"))

by_path = {row["source_path"]: row for row in rows}
implementation = by_path["scripts/integrations/mesh-bt-link"]
shim = by_path["scripts/mesh-bt-link"]
assert implementation["domain"] == "integrations", implementation
assert implementation["kind"] == "tool" and implementation["deploy_policy"] == "none", implementation
assert shim["domain"] == "integrations" and shim["installed_basename"] == "mesh-bt-link", shim
assert shim["deploy_policy"] == "install" and shim["compatibility_owner"] == "scripts:mesh-bt-link", shim
PY

# Exercise the top-level compatibility entrypoint with an isolated state directory. The real
# --test may return 2 when this node has no usable Bluetooth controller; that is an honest outcome.
mkdir -p "$tmp/home"
set +e
test_out=$(HOME="$tmp/home" MESH_REPO="$repo" "$shim" --test 2>&1)
test_rc=$?
set -e
case "$test_rc" in
  0) printf '%s\n' "$test_out" | grep -q 'smoke-test: ok' || {
       echo "BT integration: green live test omitted its artifact: $test_out" >&2
       exit 1
     } ;;
  2) printf '%s\n' "$test_out" | grep -q 'smoke-test: n/a' || {
       echo "BT integration: unavailable sensor was not reported honestly: $test_out" >&2
       exit 1
     } ;;
  *) echo "BT integration: --test failed with rc=$test_rc: $test_out" >&2; exit 1 ;;
esac

echo 'BT integration: manifest, shim resolution, and real-read/unavailable test result pass'
