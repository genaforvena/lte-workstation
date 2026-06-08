#!/usr/bin/env bash
# mesh-card-watchdog.sh — periodic invariant checker.
# Runs mesh-card --refresh; on non-zero exit (invariant violation), writes a loud
# line to mesh-trace and sends a Telegram notification via mesh-tg.
#
# Intended to be triggered by mesh-card-watchdog.timer (systemd), following the same
# pattern as mtg-watchdog. Runs as the current user (user-level systemd unit).
set -uo pipefail

CARD="${MESH_CARD:-$HOME/.mesh-card}"
MESH_DIR="${HOME}/.mesh"
LOG="${MESH_DIR}/traces.log"
HOST="$(hostname)"
MESH_CARD_BIN="${HOME}/.local/bin/mesh-card"
MESH_TG_BIN="${HOME}/.local/bin/mesh-tg"
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }

[ -x "$MESH_CARD_BIN" ] || { echo "mesh-card not found at $MESH_CARD_BIN" >&2; exit 1; }

# Run the invariant check
output="$("$MESH_CARD_BIN" --refresh 2>&1)"
rc=$?

if [ $rc -eq 0 ]; then
    # Invariant holds — nothing to do
    exit 0
fi

# Violation detected — alert
echo "$output" >&2
echo "$(ts)  mesh-card-watchdog@$HOST  ::  [ALERT] mesh-card INVARIANT VIOLATION (exit $rc)" >> "$LOG"

# Notify via Telegram
if [ -x "$MESH_TG_BIN" ]; then
    # Extract the violation line from the card output
    viol="$(echo "$output" | grep -i 'invariant-check\|VIOLATION' | head -3 | tr '\n' ' ')"
    "$MESH_TG_BIN" "[ALERT] mesh-card invariant violation on $HOST: $viol" 2>/dev/null || true
fi

exit $rc
