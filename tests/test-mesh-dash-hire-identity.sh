#!/usr/bin/env bash
set -u

repo="$(cd "$(dirname "$0")/.." && pwd)"
dash="$repo/scripts/mesh-dash"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh/hire" "$td/.config/gh"
printf 'github.com/genaforvena (authorized hire identity)\n' > "$td/.mesh/hire/identity.txt"
cat > "$td/.config/gh/hosts.yml" <<'EOF_HOSTS'
github.com:
    user: genaforvena
    oauth_token: DO_NOT_READ
EOF_HOSTS

out="$(HOME="$td" MESH_DIR="$td/.mesh" PATH="$repo/scripts:$PATH" "$dash" --once hire 2>&1)" || {
  rc=$?
  echo "FAIL: hire dash exited rc=$rc"
  exit 1
}
printf '%s\n' "$out" | grep -Fq -- '-- identity: github.com/genaforvena' \
  || { echo 'FAIL: authorized hire identity disappeared'; exit 1; }
printf '%s\n' "$out" | grep -Fq -- '-- authorized GitHub account: genaforvena (local config; token not read)' \
  || { echo 'FAIL: authorized local GitHub account missing from hire dash'; exit 1; }
if printf '%s\n' "$out" | grep -Fq 'DO_NOT_READ'; then
  echo 'FAIL: hire dash rendered a credential value'
  exit 1
fi
if printf '%s\n' "$out" | grep -Fq -- 'ghIsPureTrash'; then
  echo 'FAIL: stale ghIsPureTrash identity rendered'
  exit 1
fi

echo 'test-mesh-dash-hire-identity: PASS'
