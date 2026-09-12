#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
shim="$repo/scripts/mesh-imac-cam"
implementation="$repo/scripts/integrations/mesh-imac-cam"
helper="$repo/scripts/integrations/mesh-imac-cam.m"
tmp=$(mktemp -d -t mesh-imac-cam-integration.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$implementation" ] || {
  echo 'iMac camera integration: implementation is not in integrations/' >&2
  exit 1
}
[ -f "$helper" ] || {
  echo 'iMac camera integration: Objective-C helper is not paired with implementation' >&2
  exit 1
}
[ -x "$shim" ] || {
  echo 'iMac camera integration: compatibility entrypoint is not executable' >&2
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
implementation = by_path["scripts/integrations/mesh-imac-cam"]
helper = by_path["scripts/integrations/mesh-imac-cam.m"]
shim = by_path["scripts/mesh-imac-cam"]
assert implementation["domain"] == "integrations", implementation
assert implementation["kind"] == "tool" and implementation["deploy_policy"] == "none", implementation
assert helper["domain"] == "integrations" and helper["deploy_policy"] == "none", helper
assert shim["domain"] == "integrations" and shim["installed_basename"] == "mesh-imac-cam", shim
assert shim["deploy_policy"] == "install" and shim["compatibility_owner"] == "scripts:mesh-imac-cam", shim
assert shim["cadence_policy"] == "none", shim
PY

# Exercise the public compatibility path. The offline settle-core gate must pass; exit 2 is honest
# only when the actual iMac is unreachable, while a reachable iMac must produce a real JPEG.
set +e
test_out=$("$shim" --test 2>&1)
test_rc=$?
set -e
printf '%s\n' "$test_out" | grep -q 'settle-core: ok' || {
  echo "iMac camera integration: offline settle gate did not pass: $test_out" >&2
  exit 1
}
case "$test_rc" in
  0) printf '%s\n' "$test_out" | grep -q 'REAL capture .* JPEG' || {
       echo "iMac camera integration: green test omitted a real JPEG: $test_out" >&2
       exit 1
     } ;;
  2) printf '%s\n' "$test_out" | grep -q 'smoke-test: n/a (iMac unreachable:' || {
       echo "iMac camera integration: unavailable iMac was not reported honestly: $test_out" >&2
       exit 1
     } ;;
  *) echo "iMac camera integration: --test failed with rc=$test_rc: $test_out" >&2; exit 1 ;;
esac

echo 'iMac camera integration: paired source, manifest ownership, and real-read/unavailable gate pass'
