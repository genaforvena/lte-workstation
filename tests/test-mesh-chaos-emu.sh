#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-chaos-emu"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
export MESH_CHAOS_EMU_DIR="$td/state"

set +e
"$tool" --id sequence --fail-rcs 75,75,125 -- true
rc1=$?
"$tool" --id sequence --fail-rcs 75,75,125 -- true
rc2=$?
"$tool" --id sequence --fail-rcs 75,75,125 -- true
rc3=$?
set -e
[ "$rc1" -eq 75 ]
[ "$rc2" -eq 75 ]
[ "$rc3" -eq 125 ]
[ "$("$tool" --count sequence)" -eq 3 ]

if "$tool" --id bad --fail-rcs 75,nope -- true >/dev/null 2>&1; then
  echo 'invalid --fail-rcs value unexpectedly accepted' >&2
  exit 1
fi

if "$tool" --id success-is-not-failure --fail-rcs 0 -- true >/dev/null 2>&1; then
  echo 'success exit code was accepted as an injected failure' >&2
  exit 1
fi

if "$tool" --id success-is-not-failure --fail-first 1 --rc 0 -- true >/dev/null 2>&1; then
  echo 'success --rc was accepted as an injected failure' >&2
  exit 1
fi

echo 'test-mesh-chaos-emu: PASS (scripted transient/terminal rc sequence and validation)'
