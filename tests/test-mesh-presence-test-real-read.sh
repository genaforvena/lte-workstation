#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-presence"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/stub" "$td/.mesh" "$td/sysfs/hci0"
cat > "$td/stub/bluetoothctl" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$BT_CALLS"
case "${1:-}" in
  show) printf 'Controller 00:11:22:33:44:55\n\tPowered: yes\n\tDiscovering: no\n' ;;
  devices)
    case "${BT_MODE:-good}" in
      failed) exit 1 ;;
      empty) exit 0 ;;
    esac
    printf 'Device AA:BB:CC:DD:EE:FF Test Phone\n' ;;
  info) printf 'Device AA:BB:CC:DD:EE:FF (public)\n\tName: Test Phone\n\tRSSI: 0x0000 (-62)\n' ;;
  *) cat >/dev/null ;;
esac
EOF
chmod +x "$td/stub/bluetoothctl"

set +e
out=$(HOME="$td" PATH="$td/stub:$PATH" \
  MESH_PRESENCE_BT_SYSFS="$td/sysfs" BT_CALLS="$td/bluetooth.calls" \
  "$tool" --test 2>&1)
rc=$?
set -e

[ "$rc" -eq 0 ] || { echo "FAIL: stubbed live scan test should pass (rc=$rc): $out"; exit 1; }
grep -q '^smoke-test: real-read artifact: status=ok count=1 fresh=yes$' <<<"$out" \
  || { echo "FAIL: --test must report a fresh real-scan artifact, got: $out"; exit 1; }
grep -qx 'devices' "$td/bluetooth.calls" \
  || { echo "FAIL: --test reported success without asking the live scanner for devices"; exit 1; }
[ ! -e "$td/.mesh/presence.log" ] \
  || { echo "FAIL: --test must not write the liveness ledger"; exit 1; }

set +e
failed_out=$(HOME="$td/failed" PATH="$td/stub:$PATH" \
  MESH_PRESENCE_BT_SYSFS="$td/sysfs" BT_CALLS="$td/bluetooth.calls" BT_MODE=failed \
  MESH_PRESENCE_COALESCE_S=0 "$tool" 3 --fresh --json 2>&1)
failed_rc=$?
set -e
[ "$failed_rc" -eq 2 ] || { echo "FAIL: failed Bluetooth cache query must be unreachable (rc=$failed_rc): $failed_out"; exit 1; }
grep -q '"status":"unreachable"' <<<"$failed_out" \
  || { echo "FAIL: failed cache query must not be a confident empty: $failed_out"; exit 1; }
python3 -c 'import json,sys; d=json.loads(sys.argv[1]); assert d["count"] is None and d["known"] is None, d' \
  "$(tail -n 1 <<<"$failed_out")" \
  || { echo "FAIL: failed cache query must leave count/known unknown: $failed_out"; exit 1; }

set +e
empty_out=$(HOME="$td/empty" PATH="$td/stub:$PATH" \
  MESH_PRESENCE_BT_SYSFS="$td/sysfs" BT_CALLS="$td/bluetooth.calls" BT_MODE=empty \
  MESH_PRESENCE_COALESCE_S=0 "$tool" 3 --fresh --json 2>&1)
empty_rc=$?
set -e
[ "$empty_rc" -eq 0 ] || { echo "FAIL: successful empty scan should remain assessable (rc=$empty_rc): $empty_out"; exit 1; }
python3 -c 'import json,sys; d=json.loads(sys.argv[1]); assert d["status"]=="ok" and d["count"]==0 and d["coalesced_age_s"] is None, d' \
  "$(tail -n 1 <<<"$empty_out")" \
  || { echo "FAIL: a successful fresh zero-device scan must remain a real empty artifact: $empty_out"; exit 1; }

echo 'mesh-presence --test fresh real-read gate: PASS'
