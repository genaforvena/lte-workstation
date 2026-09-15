#!/usr/bin/env bash
set -euo pipefail

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

repo="$td/repo"
home="$td/home"
bin="$td/bin"
mkdir -p "$repo" "$home/.mesh" "$home/.local/bin" "$bin"
printf 'mesh-land version one\n' >"$td/live-mesh-land"

PATH="$bin:/usr/bin:/bin" \
HOME="$home" \
MESH_LAND_WAKE_BIN="$td/live-mesh-land" \
MESH_LAND_WAKE_STATE="$home/.mesh/land-wake.state" \
MESH_LAND_WAKE_WINDOW=genome \
MESH_REPO="$repo" \
  scripts/mesh-land-wake --once

[ ! -e "$home/tells" ] || { echo 'FAIL: first observation must baseline without waking'; exit 1; }

printf 'mesh-land version one\n' >"$td/live-mesh-land"
PATH="$bin:/usr/bin:/bin" HOME="$home" MESH_LAND_WAKE_BIN="$td/live-mesh-land" \
  MESH_LAND_WAKE_STATE="$home/.mesh/land-wake.state" MESH_LAND_WAKE_WINDOW=genome \
  MESH_REPO="$repo" scripts/mesh-land-wake --once
[ ! -e "$home/tells" ] || { echo 'FAIL: unchanged deployed mesh-land must stay quiet'; exit 1; }

printf 'mesh-land version two\n' >"$td/live-mesh-land"
if PATH="$bin:/usr/bin:/bin" HOME="$home" MESH_LAND_WAKE_BIN="$td/live-mesh-land" \
  MESH_LAND_WAKE_STATE="$home/.mesh/land-wake.state" MESH_LAND_WAKE_WINDOW=genome \
  MESH_REPO="$repo" scripts/mesh-land-wake --once; then
  echo 'FAIL: changed deployed mesh-land must remain pending when mesh-tell refuses'; exit 1
fi

cat >"$home/.local/bin/mesh-tell" <<'EOF'
#!/usr/bin/env bash
printf '%s\t%s\n' "$1" "$2" >>"$HOME/tells"
EOF
chmod +x "$home/.local/bin/mesh-tell"
PATH="/usr/bin:/bin" HOME="$home" MESH_LAND_WAKE_BIN="$td/live-mesh-land" \
  MESH_LAND_WAKE_STATE="$home/.mesh/land-wake.state" MESH_LAND_WAKE_WINDOW=genome \
  MESH_REPO="$repo" scripts/mesh-land-wake --once
[ "$(wc -l <"$home/tells")" = 1 ] || { echo 'FAIL: deployed mesh-land change must wake exactly once'; exit 1; }
grep -q $'^genome\t' "$home/tells" || { echo 'FAIL: wake target must be genome'; exit 1; }
grep -q 'mesh-land' "$home/tells" || { echo 'FAIL: wake must identify mesh-land'; exit 1; }

PATH="/usr/bin:/bin" HOME="$home" MESH_LAND_WAKE_BIN="$td/live-mesh-land" \
  MESH_LAND_WAKE_STATE="$home/.mesh/land-wake.state" MESH_LAND_WAKE_WINDOW=genome \
  MESH_REPO="$repo" scripts/mesh-land-wake --once
[ "$(wc -l <"$home/tells")" = 1 ] || { echo 'FAIL: one deployed hash must not wake repeatedly'; exit 1; }

echo 'mesh-land-wake: test ok'
