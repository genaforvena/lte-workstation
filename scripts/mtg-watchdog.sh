#!/bin/bash
# Restart MTG if it has been failing to reach Telegram for >2 minutes.
# Run via mtg-watchdog.service + mtg-watchdog.timer every 5 minutes.

WINDOW=120  # seconds to look back
ERROR_THRESHOLD=3

recent_errors=$(docker logs mtg --since "${WINDOW}s" 2>&1 \
    | grep -c 'cannot dial to telegram' || true)
recent_errors=${recent_errors:-0}

if [[ "$recent_errors" -ge "$ERROR_THRESHOLD" ]]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) mtg-watchdog: $recent_errors errors in last ${WINDOW}s — restarting"
    docker restart mtg
else
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) mtg-watchdog: OK ($recent_errors errors)"
fi
