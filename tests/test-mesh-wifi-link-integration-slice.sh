#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
shim="$repo/scripts/mesh-wifi-link"
implementation="$repo/scripts/integrations/mesh-wifi-link"
tmp=$(mktemp -d -t mesh-wifi-link-integration.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$implementation" ] || {
  echo 'Wi-Fi integration: implementation is not in integrations/' >&2
  exit 1
}
[ -x "$shim" ] || {
  echo 'Wi-Fi integration: compatibility entrypoint is not executable' >&2
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
implementation = by_path["scripts/integrations/mesh-wifi-link"]
shim = by_path["scripts/mesh-wifi-link"]
assert implementation["domain"] == "integrations", implementation
assert implementation["kind"] == "tool" and implementation["deploy_policy"] == "none", implementation
assert shim["domain"] == "integrations" and shim["installed_basename"] == "mesh-wifi-link", shim
assert shim["deploy_policy"] == "install" and shim["cadence_policy"] == "header", shim
assert shim["compatibility_owner"] == "scripts:mesh-wifi-link", shim
PY

# This test performs the adapter's live Termux Wi-Fi read. Exit 2 is expected when the phone is
# unavailable; that result must remain visibly n/a instead of becoming a fabricated all-clear.
set +e
test_out=$("$shim" --test 2>&1)
test_rc=$?
set -e
case "$test_rc" in
  0) printf '%s\n' "$test_out" | grep -q 'live read produced real fields' || {
       echo "Wi-Fi integration: green test omitted a real sample: $test_out" >&2
       exit 1
     } ;;
  2) printf '%s\n' "$test_out" | grep -q 'smoke-test: n/a' || {
       echo "Wi-Fi integration: unavailable sensor was not reported honestly: $test_out" >&2
       exit 1
     } ;;
  *) echo "Wi-Fi integration: --test failed with rc=$test_rc: $test_out" >&2; exit 1 ;;
esac

echo 'Wi-Fi integration: manifest, cadence owner, and real-read/unavailable result pass'
