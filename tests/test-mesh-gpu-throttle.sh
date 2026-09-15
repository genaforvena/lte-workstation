#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-gpu-throttle"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/smi" <<'STUB'
#!/usr/bin/env bash
case "${THROTTLE_MODE:-active}" in
  active) printf '0, 0x0000000000000004\n' ;;
  none) printf '0, 0x0000000000000000\n' ;;
  unavailable) exit 1 ;;
  malformed) printf '0, N/A\n' ;;
esac
STUB
chmod +x "$td/smi"

active="$(MESH_GPU_THROTTLE_SMI="$td/smi" "$TOOL" --json)"
[[ "$active" == *'"gpu_index":0,"active_mask":"0x0000000000000004","active":true'* ]] || {
  echo "FAIL: active mask was not preserved: $active" >&2
  exit 1
}

none="$(THROTTLE_MODE=none MESH_GPU_THROTTLE_SMI="$td/smi" "$TOOL" --json)"
[[ "$none" == *'"active_mask":"0x0000000000000000","active":false'* ]] || {
  echo "FAIL: zero mask was not represented as no active reason: $none" >&2
  exit 1
}

set +e
THROTTLE_MODE=unavailable MESH_GPU_THROTTLE_SMI="$td/smi" "$TOOL" --json >/dev/null 2>&1
rc=$?
set -e
[[ "$rc" -eq 2 ]] || { echo "FAIL: unreachable driver must exit 2, got $rc" >&2; exit 1; }

set +e
THROTTLE_MODE=malformed MESH_GPU_THROTTLE_SMI="$td/smi" "$TOOL" --json >/dev/null 2>&1
rc=$?
set -e
[[ "$rc" -eq 2 ]] || { echo "FAIL: unsupported driver value must exit 2, got $rc" >&2; exit 1; }

"$TOOL" --test
