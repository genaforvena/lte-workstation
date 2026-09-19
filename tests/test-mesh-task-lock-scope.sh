#!/usr/bin/env bash
# A slow board receipt for one chain must not create a mesh-wide task stop.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh/chains"
printf 'alpha\twork\tproduce a durable artifact\n' >"$td/one.tsv"
printf 'beta\twork\tproduce a separate durable artifact\n' >"$td/two.tsv"

cat >"$td/bin/mesh-chat" <<EOF
#!/usr/bin/env bash
set -euo pipefail
if [[ "\${1:-}" == --task-state ]]; then
  # Sandbox-faithful ledger append: the real append entry point against the
  # fixture MESH_DIR, so take/load replays the chain from the sandbox chat.log
  # (at land time the hardcoded real mesh-chat did this; the flood fix routes
  # save() through MESH_TASK_CHAT_CMD, and a fake that swallows --task-state
  # leaves no log for take to replay -> false red).
  # NOTE: outer heredoc is unquoted so $repo/$td bind at fixture creation;
  # fake-runtime vars stay backslash-escaped.
  exec python3 "$repo/scripts/mesh_task_log.py" append "$td/mesh" "test" "\$2"
fi
if [[ "\${1:-}" == '[taking] one/work:'* ]]; then
  : >"\$TEST_TAKING"
  while [[ ! -e "\$TEST_RELEASE" ]]; do sleep 0.02; done
fi
printf '%s\n' "\$1" >>"\$TEST_BOARD"
EOF
chmod +x "$td/bin/mesh-chat"

base=(MESH_DIR="$td/mesh" MESH_TASK_DIR="$td/mesh/chains" MESH_TASK_CHAT_CMD="$td/bin/mesh-chat" MESH_TASK_HANDOFF_CMD=/bin/true TEST_BOARD="$td/board" TEST_TAKING="$td/taking" TEST_RELEASE="$td/release")
env "${base[@]}" MESH_TASK_ACTOR=alpha python3 "$repo/scripts/mesh-task" create one "$td/one.tsv" >/dev/null

env "${base[@]}" MESH_TASK_ACTOR=alpha python3 "$repo/scripts/mesh-task" take one work >"$td/one.out" 2>"$td/one.err" &
take_pid=$!
for _ in $(seq 1 100); do [[ -e "$td/taking" ]] && break; sleep 0.02; done
[[ -e "$td/taking" ]] || { echo 'FAIL: first chain never reached its held receipt' >&2; exit 1; }

# This command touches a distinct chain and owner. It must finish while the
# first chain's receipt remains intentionally blocked.
timeout 2 env "${base[@]}" MESH_TASK_ACTOR=beta python3 "$repo/scripts/mesh-task" create two "$td/two.tsv" >"$td/two.out" 2>"$td/two.err"
grep -Fq 'created two:' "$td/two.out"

: >"$td/release"
wait "$take_pid"
python3 - "$td/mesh/chains/one.json" "$td/mesh/chains/two.json" <<'PY'
import json, sys
one, two = (json.load(open(path, encoding='utf-8')) for path in sys.argv[1:])
assert one['steps'][0]['status'] == 'active', one
assert two['steps'][0]['status'] == 'open', two
PY

echo 'test-mesh-task-lock-scope: PASS (chain-local receipt lock; unrelated chain progresses)'
