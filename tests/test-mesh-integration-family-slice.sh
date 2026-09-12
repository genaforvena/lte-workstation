#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
shim="$repo/scripts/mesh-body-motion"
implementation="$repo/scripts/integrations/mesh-body-motion"
tmp=$(mktemp -d -t mesh-integration-family.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$implementation" ] || {
  echo 'integration family: body-motion implementation is not in integrations/' >&2
  exit 1
}
[ -x "$shim" ] || {
  echo 'integration family: compatibility entrypoint is not executable' >&2
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
implementation = by_path["scripts/integrations/mesh-body-motion"]
shim = by_path["scripts/mesh-body-motion"]
assert implementation["domain"] == "integrations", implementation
assert implementation["kind"] == "tool" and implementation["deploy_policy"] == "none", implementation
assert shim["domain"] == "integrations" and shim["installed_basename"] == "mesh-body-motion", shim
assert shim["deploy_policy"] == "install" and shim["compatibility_owner"] == "scripts:mesh-body-motion", shim
PY

# A source-tree shim must resolve the nested implementation without phone access.
mkdir -p "$tmp/home/.mesh"
printf '73|[body-still]|0||42|1\n' > "$tmp/home/.mesh/.body-motion-state"
source_out=$(HOME="$tmp/home" MESH_REPO="$repo" "$shim" --status)
[ "$source_out" = '73|[body-still]|0||42|1' ] || {
  echo "integration family: source shim returned unexpected status: $source_out" >&2
  exit 1
}

# mesh-land deploys a regular copy, so its fallback must still reach the same source.
mkdir -p "$tmp/home/.local/bin"
cp "$shim" "$tmp/home/.local/bin/mesh-body-motion"
deployed_out=$(HOME="$tmp/home" MESH_REPO="$repo" "$tmp/home/.local/bin/mesh-body-motion" --status)
[ "$deployed_out" = "$source_out" ] || {
  echo "integration family: regular-copy shim returned unexpected status: $deployed_out" >&2
  exit 1
}

echo 'integration family: body-motion manifest and source/deployed shims pass'
