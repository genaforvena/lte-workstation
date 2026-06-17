#!/bin/bash
# Restart MTG if it has been failing to reach Telegram for >2 minutes.
# Run via mtg-watchdog.service + mtg-watchdog.timer every 5 minutes.
#   mtg-watchdog.sh           run the watchdog (needs docker; Docker-MTG nodes)
#   mtg-watchdog.sh --test    smoke — deps + dry-run of the error-count/threshold restart decision

WINDOW=120  # seconds to look back
ERROR_THRESHOLD=3
PATTERN='cannot dial to telegram'   # the load-bearing match — shared by the run path AND --test

if [[ "${1:-}" == "--test" ]]; then
  # grep is the load-bearing dep: the whole detection is `grep -c PATTERN`. Without it the
  # watchdog can neither count failures nor decide to restart — exactly the silent-no-op a
  # smoke test must catch. date is needed for the log line.
  command -v grep >/dev/null 2>&1 || { echo "smoke-test: FAIL (no grep — cannot count failures)"; exit 1; }
  command -v date >/dev/null 2>&1 || { echo "smoke-test: FAIL (no date)"; exit 1; }
  # Dry-run the REAL decision (NOT echo-ok): feed a synthetic `docker logs` stream through the
  # SAME PATTERN + threshold, asserting (a) the count is right and (b) the >=threshold restart
  # decision trips at 3 and NOT at 2. A wrong count = a needless restart or a missed-down proxy.
  three=$(printf '%s\n' 'ok' "$PATTERN" 'noise' "$PATTERN" "$PATTERN" 'ok' | grep -c "$PATTERN")
  [[ "$three" == "3" ]] || { echo "smoke-test: FAIL (count parse drifted: matched $three of 3)"; exit 1; }
  [[ "$three" -ge "$ERROR_THRESHOLD" ]] || { echo "smoke-test: FAIL (3 errors did not trip threshold $ERROR_THRESHOLD)"; exit 1; }
  two=$(printf '%s\n' "$PATTERN" 'ok' "$PATTERN" | grep -c "$PATTERN")
  [[ "$two" -lt "$ERROR_THRESHOLD" ]] || { echo "smoke-test: FAIL (2 errors wrongly tripped threshold $ERROR_THRESHOLD)"; exit 1; }
  none=$(printf '%s\n' 'all' 'fine' 'here' | grep -c "$PATTERN" || true)
  [[ "${none:-0}" == "0" ]] || { echo "smoke-test: FAIL (clean log counted as $none errors — would falsely restart)"; exit 1; }
  if command -v docker >/dev/null 2>&1; then dep="docker present"; else dep="docker ABSENT (not a Docker-MTG node — runtime would no-op here)"; fi
  echo "smoke-test: ok (PATTERN count + threshold trip/no-trip + clean-log guard verified; $dep)"
  exit 0
fi

recent_errors=$(docker logs mtg --since "${WINDOW}s" 2>&1 \
    | grep -c "$PATTERN" || true)
recent_errors=${recent_errors:-0}

if [[ "$recent_errors" -ge "$ERROR_THRESHOLD" ]]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) mtg-watchdog: $recent_errors errors in last ${WINDOW}s — restarting"
    docker restart mtg
else
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) mtg-watchdog: OK ($recent_errors errors)"
fi
