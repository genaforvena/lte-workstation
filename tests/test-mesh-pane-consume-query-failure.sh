#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-pane-consume"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/mesh-task" <<'EOF'
#!/usr/bin/env bash
printf 'genome\tpartial/row\t0\tpartial output must be discarded\n'
exit 9
EOF
chmod +x "$td/mesh-task"

candidate="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" "$tool" --task-candidate genome)"
[ "$candidate" = $'!queue-unavailable\t\t0\tmesh-task queue --dispatch failed' ] || {
  echo "FAIL: failed queue query was not surfaced as UNKNOWN: $candidate" >&2
  exit 1
}

message="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" "$tool" --wake-message genome)"
printf '%s' "$message" | grep -Fq 'state is UNKNOWN, not an empty queue' || {
  echo "FAIL: wake message converted queue failure into idle/fallback work: $message" >&2
  exit 1
}
printf '%s' "$message" | grep -Fq 'do not idle' || {
  echo "FAIL: queue failure wake omitted the no-idle guard: $message" >&2
  exit 1
}
printf '%s\n' 'test-mesh-pane-consume-query-failure: PASS (partial failed query is UNKNOWN and wakes retry)'
