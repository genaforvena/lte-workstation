#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-pane-consume"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/home"
cat >"$td/bin/mesh-task" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  "queue --dispatch --owner witness") exit 0 ;;
  *) exit 1 ;;
esac
EOF
chmod +x "$td/bin/mesh-task"

message="$(PATH="$td/bin:/usr/bin:/bin" HOME="$td/home" "$tool" --wake-message witness)"
for required in \
  'sweep the live top pane' \
  'read ~/.mesh/chat.log' \
  'read ~/.mesh/tasks.journal' \
  'mesh-task audit' \
  'duplicate' \
  'health' \
  'loop' \
  'Only after this sweep'; do
  printf '%s' "$message" | grep -Fqi -- "$required" || {
    echo "FAIL: sweep nudge is missing '$required': $message" >&2
    exit 1
  }
done
printf '%s' "$message" | grep -Fqi 'post exactly one terse [idle] line' || {
  echo "FAIL: nudge must still permit a single evidence-based idle line after the sweep" >&2
  exit 1
}
echo 'test-mesh-pane-consume-sweep-nudge: PASS'
