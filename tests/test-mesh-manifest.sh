#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
manifest="$root/scripts/mesh-manifest"

tmp=$(mktemp -d -t mesh-manifest-test.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

repo="$tmp/repo"
mkdir -p "$repo/scripts/reticulum" "$repo/scripts/tests" "$repo/scripts/__pycache__" "$repo/job" "$repo/outside"
printf '#!/usr/bin/env bash\necho top\n' > "$repo/scripts/mesh-fixture-tool"
printf '#!/usr/bin/env bash\necho nested\n' > "$repo/scripts/reticulum/mesh-fixture-nested"
printf '[Unit]\n' > "$repo/scripts/demo.service"
printf 'fixture\n' > "$repo/scripts/tests/sample.fixture"
printf 'cache\n' > "$repo/scripts/__pycache__/sample.cpython-312.pyc"
printf '#!/usr/bin/env bash\necho job\n' > "$repo/job/mesh-fixture-job"
chmod +x "$repo/scripts/mesh-fixture-tool" "$repo/scripts/reticulum/mesh-fixture-nested" "$repo/job/mesh-fixture-job"
printf 'outside\n' > "$repo/outside/not-a-source"

live=$tmp/live.tsv
MESH_REPO="$repo" "$manifest" --check >/dev/null
MESH_REPO="$repo" "$manifest" --list > "$live"
grep -q $'^scripts/mesh-fixture-tool\tmesh-fixture-tool\t' "$live"
grep -q $'^scripts/reticulum/mesh-fixture-nested\tmesh-fixture-nested\t' "$live"
grep -q $'^scripts/demo.service\t\t.*\tunit\tsystemd\tunit\t' "$live"
grep -q $'^scripts/tests/sample.fixture\t\t.*\tfixture\tnone\tnone\t' "$live"
grep -q $'^scripts/__pycache__/sample.cpython-312.pyc\t\t.*\tasset\tnone\tnone\t' "$live"
grep -q $'^job/mesh-fixture-job\tmesh-fixture-job\t' "$live"
! grep -q 'outside/not-a-source' "$live"

mkdir -p "$repo/scripts/other"
printf '#!/usr/bin/env bash\necho duplicate-a\n' > "$repo/scripts/reticulum/mesh-duplicate"
printf '#!/usr/bin/env bash\necho duplicate-b\n' > "$repo/scripts/other/mesh-duplicate"
chmod +x "$repo/scripts/reticulum/mesh-duplicate" "$repo/scripts/other/mesh-duplicate"
if MESH_REPO="$repo" "$manifest" --check >/dev/null 2>"$tmp/duplicate.err"; then
  echo 'mesh-manifest: duplicate install basename was accepted' >&2
  exit 1
fi
grep -q 'duplicate installed basename' "$tmp/duplicate.err"

echo 'mesh manifest contract: fixture matrix and duplicate guard pass'
