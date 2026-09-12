#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
shim="$repo/scripts/mesh-camera"
implementation="$repo/scripts/integrations/mesh-camera"
tmp=$(mktemp -d -t mesh-camera-integration.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$implementation" ] || {
  echo 'camera integration: implementation is not in integrations/' >&2
  exit 1
}
[ -x "$shim" ] || {
  echo 'camera integration: compatibility entrypoint is not executable' >&2
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
implementation = by_path["scripts/integrations/mesh-camera"]
shim = by_path["scripts/mesh-camera"]
assert implementation["domain"] == "integrations", implementation
assert implementation["kind"] == "tool" and implementation["deploy_policy"] == "none", implementation
assert shim["domain"] == "integrations" and shim["installed_basename"] == "mesh-camera", shim
assert shim["deploy_policy"] == "install" and shim["compatibility_owner"] == "scripts:mesh-camera", shim
PY

# --test must capture and validate one real frame (or report a held, usable device as BUSY).
mkdir -p "$tmp/home"
set +e
test_out=$(HOME="$tmp/home" MESH_REPO="$repo" "$shim" --test 2>&1)
test_rc=$?
set -e
[ "$test_rc" -eq 0 ] || {
  echo "camera integration: real capture test failed with rc=$test_rc: $test_out" >&2
  exit 1
}
printf '%s\n' "$test_out" | grep -qE 'smoke-test: ok \(real one-frame capture -> |smoke-test: ok \(camera present but BUSY' || {
  echo "camera integration: test omitted a validated frame or explicit busy result: $test_out" >&2
  exit 1
}

echo 'camera integration: manifest, compatibility shim, and real capture artifact pass'
