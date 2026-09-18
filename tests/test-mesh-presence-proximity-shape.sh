#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-presence"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/stub" "$td/.mesh" "$td/sysfs/hci0"
cat > "$td/stub/bluetoothctl" <<'EOF'
#!/bin/sh
case "${1:-}" in
  show) printf 'Controller 00:11:22:33:44:55\n\tPowered: yes\n\tDiscovering: no\n' ;;
  devices)
    [ "${BT_MODE:-good}" = failed ] && exit 1
    printf 'Device AA:BB:CC:DD:EE:01 One\nDevice AA:BB:CC:DD:EE:02 Two\n'
    ;;
  info)
    case "$2" in
      AA:BB:CC:DD:EE:01) printf 'Device %s (public)\n\tName: One\n\tRSSI: 0x0000 (-52)\n' "$2" ;;
      *) printf 'Device %s (public)\n\tName: Two\n\tRSSI: 0x0000 (-80)\n' "$2" ;;
    esac
    ;;
esac
EOF
chmod +x "$td/stub/bluetoothctl"

out=$(HOME="$td" PATH="$td/stub:$PATH" MESH_PRESENCE_BT_SYSFS="$td/sysfs" \
  MESH_PRESENCE_COALESCE_S=0 "$tool" 3 --fresh --json 2>&1)
python3 -c 'import json,sys; d=json.loads(sys.argv[1]); assert d["status"] == "ok"; assert d["rssi_span_db"] == 28; assert d["proximity_shape"] == "SPREAD", d' \
  "$(tail -n 1 <<<"$out")"

set +e
degraded=$(HOME="$td/missing" PATH="$td/stub:$PATH" MESH_PRESENCE_BT_SYSFS="$td/sysfs" \
  MESH_PRESENCE_COALESCE_S=0 BT_MODE=failed "$tool" 3 --fresh --json 2>&1)
set -e
# A failed cache query is an unreachable read, not a zero-device shape.
python3 -c 'import json,sys; d=json.loads(sys.argv[1]); assert d["status"] == "unreachable"; assert d["proximity_shape"] is None, d' \
  "$(tail -n 1 <<<"$degraded")"

echo 'mesh-presence proximity-shape: PASS'
