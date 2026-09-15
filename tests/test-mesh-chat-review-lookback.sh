#!/usr/bin/env bash
set -euo pipefail

script="$(dirname "$(dirname "$(readlink -f "$0")")")/scripts/mesh-chat-review"
default="$(sed -n 's/^LOOKBACK="${MESH_CHAT_REVIEW_LINES:-\([0-9][0-9]*\)}".*/\1/p' "$script")"

[ "$default" = 800 ] || {
  echo "FAIL: mesh-chat-review default chat.log lookback is $default, want 800" >&2
  exit 1
}
echo "PASS: mesh-chat-review reads 800 chat.log rows by default"
