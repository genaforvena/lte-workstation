#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
shim="$repo/scripts/mesh-task-watch"
impl="$repo/scripts/core/mesh-task-watch"

[ -x "$shim" ] || { echo 'FAIL: public mesh-task-watch path is not executable' >&2; exit 1; }
[ -x "$impl" ] || { echo 'FAIL: core implementation is missing or not executable' >&2; exit 1; }
grep -q '^# reflex-cadence: \*/5 \* \* \* \*' "$shim" \
  || { echo 'FAIL: shim lost the existing five-minute cadence' >&2; exit 1; }
grep -q '^# reflex-args: --window 290 --debounce 1 .* -- mesh-task-journal$' "$shim" \
  || { echo 'FAIL: shim lost the deployed reflex arguments' >&2; exit 1; }

manifest="$("$repo/scripts/mesh-manifest" --list)"
printf '%s\n' "$manifest" | awk -F '\t' '$1=="scripts/core/mesh-task-watch" && $3=="core" && $4=="tool" && $5=="none" && $7=="scripts:mesh-task-watch" { ok=1 } END { exit !ok }' \
  || { echo 'FAIL: nested implementation manifest row is not core/non-deploying under the shim owner' >&2; exit 1; }
printf '%s\n' "$manifest" | awk -F '\t' '$1=="scripts/mesh-task-watch" && $3=="core" && $4=="tool" && $5=="install" && $6=="header" && $7=="scripts:mesh-task-watch" { ok=1 } END { exit !ok }' \
  || { echo 'FAIL: public shim manifest row does not preserve install/cadence ownership' >&2; exit 1; }

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin/core"
cp "$shim" "$td/bin/mesh-task-watch"
cat > "$td/bin/core/mesh-task-watch" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$CAPTURE_ARGS"
EOF
chmod +x "$td/bin/core/mesh-task-watch"
CAPTURE_ARGS="$td/args" "$td/bin/mesh-task-watch" --window 8 "$td/chat.log" -- "$td/run" arg1
printf '%s\n' --window 8 "$td/chat.log" -- "$td/run" arg1 > "$td/expected"
cmp -s "$td/expected" "$td/args" \
  || { echo 'FAIL: compatibility shim did not forward the original arguments' >&2; exit 1; }

# An installed shim has no sibling core/ tree; it must resolve through MESH_REPO.
mkdir -p "$td/installed"
cp "$shim" "$td/installed/mesh-task-watch"
set +e
fallback_out="$(MESH_REPO="$repo" "$td/installed/mesh-task-watch" --test 2>&1)"
fallback_rc=$?
set -e
case "$fallback_rc:$fallback_out" in
  0:*'mesh-task-watch --test: PASS'*) ;;
  2:*'mesh-task-watch --test: n/a'*) ;;
  *) echo "FAIL: deployed-shim fallback returned rc=$fallback_rc: $fallback_out" >&2; exit 1 ;;
esac

# Exercise the existing watcher event path through the public basename from outside the repo.
(cd /tmp && bash "$repo/tests/test-mesh-task-watch.sh")

# Rehearse the inverse move in a scratch repo: put the nested implementation back at its old public
# path, remove the core location, and prove the old event test still resolves it directly.
mkdir -p "$td/rollback/scripts" "$td/rollback/job" "$td/rollback/tests"
cp "$impl" "$td/rollback/scripts/mesh-task-watch"
cp "$repo/tests/test-mesh-task-watch.sh" "$td/rollback/tests/test-mesh-task-watch.sh"
chmod +x "$td/rollback/scripts/mesh-task-watch"
rollback_manifest="$(MESH_REPO="$td/rollback" "$repo/scripts/mesh-manifest" --list)"
printf '%s\n' "$rollback_manifest" | awk -F '\t' '$1=="scripts/mesh-task-watch" && $3=="core" && $4=="tool" && $5=="install" && $6=="header" { ok=1 } END { exit !ok }' \
  || { echo 'FAIL: inverse move does not restore the old public installable tool row' >&2; exit 1; }
(cd /tmp && bash "$td/rollback/tests/test-mesh-task-watch.sh")
echo 'PASS: core ownership, deployed fallback, argument forwarding, preserved cadence, chat.log dispatch, and inverse-move rollback'
