#!/usr/bin/env bash
# Exercise the synthetic authority command and the actual producer wake seams.
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export MESH_MISHE_HOME="$tmp" MESH_MISHE_CORE="${MESH_MISHE_CORE:-/home/mesh-home/mishe-tauftauf}"
"$repo/scripts/mesh-mishe-authority" legacy-allowed synthetic >/dev/null
PYTHONPATH="$MESH_MISHE_CORE/src" python3 -c 'from mishe_tauftauf.feed import Feed; import os; Feed(os.environ["MESH_MISHE_HOME"]).append_runtime("mishe-tauftauf", "shadow")'
"$repo/scripts/mesh-mishe-authority" switch synthetic --to mishe --expect-generation 0 --feed-seq 1 >/dev/null
set +e
"$repo/scripts/mesh-mishe-authority" legacy-allowed synthetic >/dev/null
rc=$?
set -e
[ "$rc" = 1 ] || { echo "legacy fence: expected mishe rc=1, got $rc" >&2; exit 1; }
"$repo/scripts/mesh-pane-consume" --test >/dev/null
"$repo/scripts/mesh-consume-all" --test >/dev/null
"$repo/scripts/mesh-loop-baton" --test >/dev/null
echo 'test-mesh-mishe-legacy-fence: PASS (synthetic authority and producer wake seams)'
