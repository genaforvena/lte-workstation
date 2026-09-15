#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
sync="$repo/scripts/mesh-chat-sync"
default="$(sed -n 's/^BOARD_CAP="${MESH_CHATSYNC_BOARD_CAP:-\([0-9][0-9]*\)}".*/\1/p' "$sync")"

[ "$default" = 14000 ] || {
  echo "FAIL: default chat.log retention is $default rows, want 14000 (week-scale headroom)" >&2
  exit 1
}
echo "PASS: chat.log default retention is 14000 rows"
