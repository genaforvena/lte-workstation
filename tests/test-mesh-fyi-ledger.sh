#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/mesh" "$TMP/fyi"
CHAT="$TMP/chat.log"
MESH_FYI_DIR="$TMP/not-built" "$ROOT/scripts/mesh-fyi-ledger" --dash > "$TMP/unavailable.out"
grep -q 'FYI view: UNAVAILABLE' "$TMP/unavailable.out"
cat > "$CHAT" <<'EOF'
2026-09-12T01:00:00Z  path-watch@node-a  ::  [fyi] path-watch: route absent ; task:route-repair, producer:path-watch, status:observed {#event-1}
2026-09-12T01:01:00Z  path-watch@node-a  ::  [fyi] path-watch: route absent ; task:route-repair, producer:path-watch, status:observed {#event-2}
2026-09-12T01:01:00Z  path-watch@node-a  ::  [fyi] path-watch: route absent ; task:route-repair, producer:path-watch, status:observed {#event-2}
2026-09-12T01:02:00Z  path-watch@node-a  ::  [fyi] path-watch: route absent task:prose-only ; producer:path-watch, status:observed {#event-3}
EOF
printf 'PROMISE 1\n' > "$TMP/mesh/promises.journal"
printf 'DONE\tgenome\tcoordination/route-repair\tcurrent=coordination/route-repair\n' > "$TMP/mesh/tasks.journal"
before_promises="$(sha256sum "$TMP/mesh/promises.journal")"
before_tasks="$(sha256sum "$TMP/mesh/tasks.journal")"

MESH_CHAT_LOG="$CHAT" MESH_FYI_DIR="$TMP/fyi" MESH_TASK_JOURNAL="$TMP/mesh/tasks.journal" "$ROOT/scripts/mesh-fyi-ledger" --build > "$TMP/build.out"
grep -q 'events=4 unique=3 repeats=1 linked=2 partial=no' "$TMP/build.out"
grep -q 'task:route-repair' "$TMP/fyi/fyi.journal"
grep -q 'source_ref:event-1' "$TMP/fyi/fyi.journal"
[ "$(grep -c 'event_id:' "$TMP/fyi/fyi.journal")" -eq 3 ]
[ "$(hledger -f "$TMP/fyi/fyi.journal" balance -N FYI | awk 'NR==2 {print $1}')" = 3 ]
[ "$(hledger -f "$TMP/fyi/fyi.journal" register tag:task=route-repair | grep -c 'FYI path-watch')" -eq 2 ]
! grep -q 'task:prose-only' "$TMP/fyi/fyi.journal"

# Independent replay reports recurrence and the explicit linked disposition.
MESH_CHAT_LOG="$CHAT" MESH_FYI_DIR="$TMP/fyi" MESH_TASK_JOURNAL="$TMP/mesh/tasks.journal" "$ROOT/scripts/mesh-fyi-ledger" --witness > "$TMP/witness.out"
grep -q 'path-watch.*route absent.*count=3.*task:route-repair disposition=DONE' "$TMP/witness.out"
grep -q 'linked-task task:route-repair fyi_events=2 disposition=DONE' "$TMP/witness.out"
grep -q 'source_sha256=' "$TMP/fyi/manifest"
grep -q 'source_cutoff=' "$TMP/fyi/manifest"
grep -q 'replay_count=4' "$TMP/fyi/manifest"
grep -q 'journal_transactions=3' "$TMP/fyi/manifest"
grep -q 'repeat_event_ids=1' "$TMP/fyi/manifest"

# The dashboard consumes the bounded materialization and remains readable if chat.log is absent.
MESH_CHAT_LOG="$TMP/missing-chat.log" MESH_FYI_DIR="$TMP/fyi" "$ROOT/scripts/mesh-fyi-ledger" --dash > "$TMP/dash.out"
grep -q 'FYI view: events=4 coverage=complete replay=pass' "$TMP/dash.out"
grep -q 'path-watch.*route absent.*count=3.*task:route-repair disposition=DONE' "$TMP/dash.out"

# The live witness pane consumes that materialized view through its normal render path.
mkdir -p "$TMP/home/.local/bin"
ln -s "$ROOT/scripts/mesh-fyi-ledger" "$TMP/home/.local/bin/mesh-fyi-ledger"
HOME="$TMP/home" PATH="$PATH" MESH_DIR="$TMP/mesh" MESH_TASK_JOURNAL="$TMP/mesh/tasks.journal" \
  MESH_DASH_CHAT_LOG="$CHAT" MESH_FYI_DIR="$TMP/fyi" \
  "$ROOT/scripts/mesh-dash" --once witness > "$TMP/pane.out"
grep -q 'FYI view: events=4 coverage=complete replay=pass' "$TMP/pane.out"

touch -d '20 minutes ago' "$TMP/fyi/manifest"
MESH_FYI_DIR="$TMP/fyi" "$ROOT/scripts/mesh-fyi-ledger" --dash > "$TMP/stale.out"
grep -q 'age=.* STALE' "$TMP/stale.out"

# A malformed complete FYI row fails loudly instead of disappearing from counts.
printf '2026-09-12T01:03:00Z  path-watch@node-a  ::  [fyi broken row\n' > "$TMP/bad.log"
if MESH_CHAT_LOG="$TMP/bad.log" MESH_FYI_DIR="$TMP/fyi" "$ROOT/scripts/mesh-fyi-ledger" --build > /dev/null 2>&1; then
  echo 'malformed FYI row unexpectedly passed' >&2
  exit 1
fi

# A board thread reference can repeat across distinct messages; the event hashes stay distinct.
cat > "$TMP/collision.log" <<'EOF'
2026-09-12T01:00:00Z  path-watch@node-a  ::  [fyi] route absent ; task:route-repair {#same-id}
2026-09-12T01:02:00Z  path-watch@node-a  ::  [fyi] route recovered ; task:route-repair {#same-id}
EOF
MESH_CHAT_LOG="$TMP/collision.log" MESH_FYI_DIR="$TMP/fyi" "$ROOT/scripts/mesh-fyi-ledger" --build > "$TMP/collision.out"
grep -q 'events=2 unique=2 repeats=0' "$TMP/collision.out"
[ "$(grep -c 'source_ref:same-id' "$TMP/fyi/fyi.journal")" -eq 2 ]

# An incomplete tail is represented as partial coverage, never silently called complete.
printf '2026-09-12T01:03:00Z  path-watch@node-a  ::  [fyi] truncated' >> "$CHAT"
MESH_CHAT_LOG="$CHAT" MESH_FYI_DIR="$TMP/fyi" "$ROOT/scripts/mesh-fyi-ledger" --build > "$TMP/partial.out"
grep -q 'partial=yes' "$TMP/partial.out"
grep -q 'coverage=partial' "$TMP/fyi/manifest"

[ "$(sha256sum "$TMP/mesh/promises.journal")" = "$before_promises" ]
[ "$(sha256sum "$TMP/mesh/tasks.journal")" = "$before_tasks" ]
echo 'test-mesh-fyi-ledger: ok'
