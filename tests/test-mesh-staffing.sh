#!/usr/bin/env bash
set -euo pipefail

# Census source is the canonical task ledger (`mesh-task audit`, stubbed here via
# MESH_STAFFING_TASK_BIN). The retired promises replay is no longer read.
root=$(cd "$(dirname "$0")/.." && pwd)
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/charter" "$td/bin"

cat >"$td/charter/tg.md" <<'EOF'
# tg — operator channel
role: communication
EOF
cat >"$td/charter/haunt.md" <<'EOF'
# haunt — research
role: research
EOF
cat >"$td/charter/discover.md" <<'EOF'
# discover — research
role: research
EOF
cat >"$td/charter/genome.md" <<'EOF'
# genome — substrate
role: substrate
protected: true
EOF
cat >"$td/bin/mesh-task" <<'EOF'
#!/usr/bin/env bash
[[ ${1:-} == audit ]] || exit 2
printf '%s\n' 'RUNNING	haunt	chain/hold	lease=2026-09-12T09:00:00Z'
EOF
chmod +x "$td/bin/mesh-task"

out=$(MESH_STAFFING_LIVE_WINDOWS='tg haunt genome' \
  MESH_STAFFING_CHARTER_DIR="$td/charter" MESH_STAFFING_TASK_BIN="$td/bin/mesh-task" \
  "$root/scripts/mesh-staffing" --json)
OUT="$out" python3 - <<'PY'
import json, os
d = json.loads(os.environ["OUT"])
assert set(d) == {"observed_at", "windows"}
assert d["observed_at"].endswith("Z")
rows = {r["window"]: r for r in d["windows"]}
assert rows["tg"]["reason"] == "communication-window"
assert rows["haunt"]["reason"] == "open-hold"
assert rows["genome"]["reason"] == "protected-role-or-substrate"
for row in rows.values():
    assert set(row) == {"window", "role", "live", "protected", "open_promises", "open_holds",
                        "active_promises", "active_holds", "leaked_promises", "leaked_holds",
                        "eligible", "reason", "observed_at"}
PY

# Mutation arm: a free-looking TG row remains excluded by the policy.
cat >"$td/bin/mesh-task-free" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$td/bin/mesh-task-free"

# A nonzero census is unreadable, full stop: `mesh-task audit` has no
# truthful-leak exit code (that semantic belonged to the retired replay).
cat >"$td/bin/mesh-task-failing" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'QUEUED	genome	chain/queued	current=chain/queued'
exit 1
EOF
chmod +x "$td/bin/mesh-task-failing"

if MESH_STAFFING_LIVE_WINDOWS='tg haunt genome' MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_TASK_BIN="$td/bin/mesh-task-failing" "$root/scripts/mesh-staffing" --json >/dev/null 2>&1; then
  echo "staffing test: FAIL (a failing task census was accepted)" >&2
  exit 1
fi

# A leaked obligation is still reported, but it is not current ownership.  Treating every
# historical leak as an active hold deadlocks otherwise-idle minds (the live failure was 55
# leaked holds making 13 of 14 windows ineligible). BLOCKED/OVERDUE rows are the
# task-ledger form of a leak: parked on an external event / an expired lease.
cat >"$td/bin/mesh-task-leaked-hold" <<'EOF'
#!/usr/bin/env bash
[[ ${1:-} == audit ]] || exit 2
printf '%s\n' 'BLOCKED	haunt	chain/blocked	external-event	event:operator-says' 'OVERDUE	haunt	chain/overdue	lease=2026-09-08T00:00:00Z' 'QUEUED	discover	chain/queued	current=chain/queued' 'RUNNING	discover	chain/hold	lease=2026-09-12T09:00:00Z'
EOF
chmod +x "$td/bin/mesh-task-leaked-hold"
leaked_hold=$(MESH_STAFFING_LIVE_WINDOWS='haunt discover' MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_TASK_BIN="$td/bin/mesh-task-leaked-hold" "$root/scripts/mesh-staffing" --json)
LEAKED_HOLD="$leaked_hold" python3 - <<'PY'
import json, os
rows = {r["window"]: r for r in json.loads(os.environ["LEAKED_HOLD"])["windows"]}
assert rows["haunt"]["open_promises"] == 1 and rows["haunt"]["open_holds"] == 1
assert rows["haunt"]["leaked_promises"] == 1 and rows["haunt"]["leaked_holds"] == 1
assert rows["haunt"]["eligible"] is True and rows["haunt"]["reason"] == "eligible-with-leaks"
assert rows["discover"]["eligible"] is False and rows["discover"]["reason"] == "open-hold"
PY

mutated=$(MESH_STAFFING_LIVE_WINDOWS='tg' MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_TASK_BIN="$td/bin/mesh-task-free" "$root/scripts/mesh-staffing" --json)
MUTATED="$mutated" python3 - <<'PY'
import json, os
row = json.loads(os.environ["MUTATED"])["windows"][0]
assert row["eligible"] is False and row["reason"] == "communication-window"
PY

if MESH_STAFFING_LIVE_WINDOWS=tg MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_TASK_BIN="$td/bin/missing" "$root/scripts/mesh-staffing" --json >/dev/null 2>&1; then
  echo "staffing test: FAIL (unreadable task census was accepted)" >&2
  exit 1
fi

# Malformed census rows fail closed, never silently dropped.
cat >"$td/bin/mesh-task-malformed" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'RUNNING'
EOF
chmod +x "$td/bin/mesh-task-malformed"
if MESH_STAFFING_LIVE_WINDOWS=tg MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_TASK_BIN="$td/bin/mesh-task-malformed" "$root/scripts/mesh-staffing" --json >/dev/null 2>&1; then
  echo "staffing test: FAIL (a malformed task census was accepted)" >&2
  exit 1
fi

board=$(MESH_STAFFING_LIVE_WINDOWS='tg' MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_TASK_BIN="$td/bin/mesh-task-free" "$root/scripts/mesh-board" available --json)
BOARD="$board" python3 - <<'PY'
import json, os
assert json.loads(os.environ["BOARD"])["windows"][0]["reason"] == "communication-window"
PY

echo "test-mesh-staffing: PASS (schema, exclusions, TG mutation, fail-closed task census, board read path)"
