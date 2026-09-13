#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd -P)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cd "$tmp"
"$repo/scripts/ux/check-build-manifest"
cp -a "$repo/scripts/ux" "$tmp/ux-copy"
printf 'platform rebuild differs\n' >> "$tmp/ux-copy/bin/uxncli"
"$tmp/ux-copy/check-build-manifest"

test -x "$repo/scripts/tests/uxn/test-lease-gate"
test -L "$repo/scripts/uxn/test-lease-gate"
test -f "$repo/scripts/ux/lease-gate.rom"
cmp "$repo/scripts/ux/lease-gate.rom" "$repo/scripts/uxn/lease-gate.rom"
test -f "$repo/scripts/ux/uxn-build-manifest.tsv"

python3 - "$repo" <<'PY'
import csv
import os
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1])
rows = list(csv.DictReader(
    subprocess.check_output(
        [str(repo / "scripts/mesh-manifest"), "--list"],
        text=True,
        env={**os.environ, "MESH_REPO": str(repo)},
    ).splitlines()[2:],
    delimiter="\t",
    fieldnames=("source_path", "installed_basename", "domain", "kind", "deploy_policy", "cadence_policy", "compatibility_owner"),
))
by_path = {row["source_path"]: row for row in rows}
test_rows = [
    row for path, row in by_path.items()
    if path.startswith("scripts/tests/uxn/") or path == "scripts/ux/chibicc/tests"
]
assert test_rows, "no UXN test/fixture rows in the production manifest"
for row in test_rows:
    assert row["domain"] == "tests" and row["kind"] == "fixture", row
    assert row["deploy_policy"] == "none" and row["installed_basename"] == "", row

ux_rows = [
    row for path, row in by_path.items()
    if path.startswith("scripts/ux/") and row["domain"] == "ux"
]
assert ux_rows, "no UXN source/asset rows in the production manifest"
for row in ux_rows:
    assert row["domain"] == "ux", row
    assert row["deploy_policy"] == "none" and row["installed_basename"] == "", row

parity = subprocess.check_output(
    [str(repo / "scripts/mesh-manifest"), "--parity"],
    text=True,
    env={**os.environ, "MESH_REPO": str(repo)},
).splitlines()[2:]
for line in parity:
    fields = line.split("\t")
    if fields[0].startswith(("scripts/tests/uxn/", "scripts/ux/")):
        assert fields[7] == "na", line

for basename in ("test-lease-gate", "lease-fixtures", "lease-gate.rom", "lease-gate.rom.sym"):
    assert not (Path.home() / ".local/bin" / basename).exists(), f"fixture/asset deployed: {basename}"
PY

"$repo/scripts/tests/uxn/test-lease-gate" >/dev/null
"$repo/scripts/tests/uxn/test-arith32" --test >/dev/null
"$repo/scripts/uxn/test-arith32" --test >/dev/null
echo "uxn layout: classified tests/assets, legacy paths resolve, and build manifest is valid from outside repo"
