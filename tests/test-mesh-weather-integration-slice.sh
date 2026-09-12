#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
shim="$repo/scripts/mesh-weather"
implementation="$repo/scripts/integrations/mesh-weather"
tmp=$(mktemp -d -t mesh-weather-integration.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$implementation" ] || {
  echo 'weather integration: implementation is not in integrations/' >&2
  exit 1
}
[ -x "$shim" ] || {
  echo 'weather integration: compatibility entrypoint is not executable' >&2
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
implementation = by_path["scripts/integrations/mesh-weather"]
shim = by_path["scripts/mesh-weather"]
assert implementation["domain"] == "integrations", implementation
assert implementation["kind"] == "tool" and implementation["deploy_policy"] == "none", implementation
assert shim["domain"] == "integrations" and shim["installed_basename"] == "mesh-weather", shim
assert shim["deploy_policy"] == "install" and shim["cadence_policy"] == "header", shim
assert shim["compatibility_owner"] == "scripts:mesh-weather", shim
PY

# This adapter's test uses the operator-seeded city-level coordinates and must parse a live response.
set +e
test_out=$("$shim" --test 2>&1)
test_rc=$?
set -e
[ "$test_rc" -eq 0 ] && printf '%s\n' "$test_out" | grep -q 'live open-meteo fetch parsed for seeded coords' || {
  echo "weather integration: live test failed with rc=$test_rc: $test_out" >&2
  exit 1
}

echo 'weather integration: manifest, compatibility shim, seeded live fetch, and parse artifact pass'
