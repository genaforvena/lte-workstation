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
    [ "${BT_MODE:-bose}" = empty ] && exit 0
    printf 'Device 28:11:A5:B8:9E:A2 LE-Bose Revolve SoundLink\n'
    ;;
  info)
    cat <<INFO
Device $2 (public)
	Name: LE-Bose Revolve SoundLink
	RSSI: 0xffffffc0 (-64)
	ManufacturerData.Key: 0x0310 (784)
	ManufacturerData.Value:
  40 10 01 31 b8 94 e7 f4 37 87                    @..1....7.
INFO
    ;;
  *) cat >/dev/null ;;
esac
EOF
chmod +x "$td/stub/bluetoothctl"

env_base=(HOME="$td" PATH="$td/stub:$PATH" MESH_PRESENCE_BT_SYSFS="$td/sysfs" \
  MESH_PRESENCE_COALESCE_S=0 MESH_PRESENCE_ANCHOR_MAX_AGE_S=3600)

env "${env_base[@]}" "$tool" 1 --log --fresh >/dev/null
line=$(tail -n 1 "$td/.mesh/presence.log")
case "$line" in
  *'manufacturer=28:11:A5:B8:9E:A2/0310:40100131b894e7f43787'*) : ;;
  *) echo "FAIL: Bose manufacturer payload was not captured opaquely: $line" >&2; exit 1 ;;
esac
case "$line" in
  *'manufacturer_decoded='*) echo "FAIL: proprietary manufacturer payload was decoded: $line" >&2; exit 1 ;;
esac

json=$(env "${env_base[@]}" "$tool" 1 --json --fresh | tail -n 1)
python3 - "$json" <<'PY'
import json, sys
record = json.loads(sys.argv[1])
assert record["manufacturer_data"] == {
    "28:11:A5:B8:9E:A2": "0310:40100131b894e7f43787"
}, record
PY

env "${env_base[@]}" BT_MODE=empty "$tool" 1 --log --fresh >/dev/null
empty_line=$(tail -n 1 "$td/.mesh/presence.log")
case "$empty_line" in
  *'n=0'*'manufacturer=unknown'*) : ;;
  *) echo "FAIL: absent device did not preserve manufacturer payload as unknown: $empty_line" >&2; exit 1 ;;
esac

echo 'mesh-presence manufacturer payload capture: PASS'
