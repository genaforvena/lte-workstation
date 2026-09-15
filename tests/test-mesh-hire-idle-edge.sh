#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="${HIRE_IDLE_TOOL:-$repo/scripts/mesh-hire-idle}"
td="$(mktemp -d)"; trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh/handoff"
cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$MESH_CHAT_POSTS"
EOF
chmod +x "$td/bin/mesh-chat"
export PATH="$td/bin:$PATH"
export MESH_CHAT_POSTS="$td/posts"
export MESH_HIRE_IDLE_STATE="$td/mesh/hire-idle.state"
export MESH_HIRE_IDLE_LOG="$td/mesh/hire-idle-receipts.log"

receipt="$td/receipt.md"
printf '%s\n' 'receipt-one' >"$receipt"

# First blocked observation emits exactly one edge and records the check.
"$tool" --blocker credential-gate --receipt "$receipt" >/dev/null
[[ "$(wc -l <"$MESH_CHAT_POSTS")" -eq 1 ]]
[[ "$(wc -l <"$MESH_HIRE_IDLE_LOG")" -eq 1 ]]

# Repeated unchanged blocker + receipt is retained off-board but does not emit.
"$tool" --blocker credential-gate --receipt "$receipt" >/dev/null
[[ "$(wc -l <"$MESH_CHAT_POSTS")" -eq 1 ]]
[[ "$(wc -l <"$MESH_HIRE_IDLE_LOG")" -eq 2 ]]

# A new receipt hash is a new blocker edge.
printf '%s\n' 'receipt-two' >"$receipt"
"$tool" --blocker credential-gate --receipt "$receipt" >/dev/null
[[ "$(wc -l <"$MESH_CHAT_POSTS")" -eq 2 ]]
[[ "$(wc -l <"$MESH_HIRE_IDLE_LOG")" -eq 3 ]]

# Recovery emits once, then repeated recovery remains silent while checks persist.
"$tool" --recovered --receipt "$receipt" >/dev/null
[[ "$(wc -l <"$MESH_CHAT_POSTS")" -eq 3 ]]
"$tool" --recovered --receipt "$receipt" >/dev/null
[[ "$(wc -l <"$MESH_CHAT_POSTS")" -eq 3 ]]
[[ "$(wc -l <"$MESH_HIRE_IDLE_LOG")" -eq 5 ]]

grep -q 'blocked' "$MESH_HIRE_IDLE_LOG"
grep -q 'recovered' "$MESH_HIRE_IDLE_LOG"
printf 'test-mesh-hire-idle-edge: PASS (unchanged gate deduped, receipt change emitted, recovery edge emitted, all checks retained)\n'
