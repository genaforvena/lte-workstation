#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TD="$(mktemp -d)"
trap 'rm -rf "$TD"' EXIT
mkdir -p "$TD/.mesh"

render() {
  HOME="$TD" MESH_DIR="$TD/.mesh" MESH_DASH_FAST=1 \
    timeout 20s bash "$ROOT/scripts/mesh-dash" --once vpn 2>&1
}

printf '%s\n' '[ss-connections] 0 active' > "$TD/.mesh/ss-connections.log"
touch -d '2 hours ago' "$TD/.mesh/ss-connections.log"
stale="$(render)"
grep -Fq 'last observed 2h ago — STALE; current SS connection state UNKNOWN' <<<"$stale"

touch "$TD/.mesh/ss-connections.log"
fresh="$(render)"
grep -Fq '[ss-connections] 0 active (observed ' <<<"$fresh"
! grep -Fq 'current SS connection state UNKNOWN' <<<"$fresh"

rm "$TD/.mesh/ss-connections.log"
missing="$(render)"
grep -Fq 'no SS connection summary artifact — UNKNOWN: the producer has not written a reading' <<<"$missing"

echo 'PASS: VPN SS connection summary distinguishes fresh, stale, and missing readings'
