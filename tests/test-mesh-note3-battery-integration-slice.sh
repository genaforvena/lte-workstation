#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
shim="$repo/scripts/mesh-note3-battery"
implementation="$repo/scripts/integrations/mesh-note3-battery"
tmp=$(mktemp -d -t mesh-note3-battery-integration.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$implementation" ] || {
  echo 'Note 3 integration: implementation is not in integrations/' >&2
  exit 1
}
[ -x "$shim" ] || {
  echo 'Note 3 integration: compatibility entrypoint is not executable' >&2
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
implementation = by_path["scripts/integrations/mesh-note3-battery"]
shim = by_path["scripts/mesh-note3-battery"]
assert implementation["domain"] == "integrations", implementation
assert implementation["kind"] == "tool" and implementation["deploy_policy"] == "none", implementation
assert shim["domain"] == "integrations" and shim["installed_basename"] == "mesh-note3-battery", shim
assert shim["deploy_policy"] == "install" and shim["cadence_policy"] == "header", shim
assert shim["compatibility_owner"] == "scripts:mesh-note3-battery", shim
PY

# The test runs parser fixtures and a real dumpsys battery read. Exit 2 is the explicit absent-ADB path.
set +e
test_out=$("$shim" --test 2>&1)
test_rc=$?
set -e
case "$test_rc" in
  0) printf '%s\n' "$test_out" | grep -q 'fixture acceptance + live ADB .* read' || {
       echo "Note 3 integration: green test omitted live battery data: $test_out" >&2
       exit 1
     } ;;
  2) printf '%s\n' "$test_out" | grep -q 'smoke-test: n/a' || {
       echo "Note 3 integration: unavailable ADB sensor was not reported honestly: $test_out" >&2
       exit 1
     } ;;
  *) echo "Note 3 integration: --test failed with rc=$test_rc: $test_out" >&2; exit 1 ;;
esac

echo 'Note 3 integration: manifest, cadence owner, and real-read/unavailable result pass'
