#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$(readlink -f "$0")")/.." && pwd)
td=$(mktemp -d)
trap 'kill "${live:-}" 2>/dev/null || true; rm -rf "$td"' EXIT
export HOME="$td/home" MESH_DIR="$td/mesh" MESH_BG_DIR="$td/mesh/bg"
mkdir -p "$HOME/.local/bin" "$MESH_DIR"
reg="$ROOT/scripts/mesh-bg-register"
done_tool="$ROOT/scripts/mesh-bg-done"
retry="$ROOT/scripts/mesh-bg-retry"
clear_tool="$ROOT/scripts/mesh-clear"

sink="$td/receipts"
retry_sink="$td/retry-receipts"
child="$td/child"

# A real detached child owns registration, artifact creation, completion and delivery.
bash -c 'f="$1"; r="$2"; d="$3"; s="$4"; p="$5";
  m=$("$r" lane real-child --target local-sink --on-done "printf receipt >> $s");
  printf "%s\n" "$m" > "$p"; printf artifact > "$f"; "$d" "$m"' \
  _ "$td/artifact" "$reg" "$done_tool" "$sink" "$child" &
child_pid=$!
wait "$child_pid"
manifest=$(<"$child")
grep -qx 'status=delivered' "$manifest"
test "$(grep -c '^receipt$' "$sink")" = 1

# Repeated successful completion is a no-op: one run produces one receipt.
"$done_tool" "$manifest" >/dev/null
test "$(grep -c '^receipt$' "$sink")" = 1

# A failed delivery remains retryable, then a local sink retry preserves the same batch.
failed_path="$td/failed.manifest"
bash -c 'm=$("$1" lane failed-child --target local-sink --on-done "exit 7");
  "$3" "$m" || true; printf "%s\n" "$m" > "$2"' _ "$reg" "$failed_path" "$done_tool" &
failed_pid=$!
wait "$failed_pid" || true
failed=$(<"$failed_path")
grep -qx 'status=done-undelivered' "$failed"
# The completion child is reaped by its parent, but the manifest's PPID can remain a zombie under
# a different init policy. Make the retry fixture unambiguously dead while retaining its identity.
sed -i 's/^pid=.*/pid=99999999/' "$failed"
sed -i "s#^on-done=.*#on-done=printf 'retry-receipt\\\\n' >> $retry_sink#" "$failed"
MESH_BG_RETRY_LOG="$td/retry.log" MESH_BG_RETRY_MAX_ATTEMPTS=2 \
  MESH_BG_DONE_CMD="$done_tool" "$retry" --apply --window lane --max 1 >/dev/null
grep -qx 'status=delivered' "$failed"
test "$(grep -c '^retry-receipt$' "$retry_sink")" = 1

# Simulate PID reuse: the numeric pid is live but its recorded start identity is stale.
live_manifest=$("$reg" lane reused-pid --target local-sink --on-done 'true')
sed -i 's/^pid_start_ticks=.*/pid_start_ticks=0/; s/^updated=.*/updated=1/' "$live_manifest"
if MESH_BG_CRASH_GRACE=0 "$clear_tool" --gate lane >"$td/gate.out" 2>&1; then
  grep -qx 'status=crashed' "$live_manifest"
else
  echo "background lifecycle: PID reuse remained blocking" >&2
  cat "$td/gate.out" >&2
  exit 1
fi

# A live, matching child is never retried merely because observation is delayed.
sleep 30 & live=$!
live_manifest=$("$reg" lane observed-live --target local-sink --on-done "printf bad-restart >> $sink")
sed -i "s/^pid=.*/pid=$live/; s/^updated=.*/updated=1/" "$live_manifest"
MESH_BG_RETRY_LOG="$td/retry-live.log" MESH_BG_RETRY_MAX_ATTEMPTS=1 \
  MESH_BG_DONE_CMD="$done_tool" "$retry" --apply --window lane --max 1 >/dev/null
grep -qx 'status=running' "$live_manifest"
! grep -q '^bad-restart$' "$sink"

echo "PASS: real child lifecycle, one receipt on repeated completion, failure→retry, PID reuse, observation timeout no restart"
