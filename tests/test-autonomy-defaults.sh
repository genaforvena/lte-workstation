#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh" "$td/bin"
cat > "$td/.mesh/study-fields.list" <<'EOF'
test | https://fake.example/search
EOF
cat > "$td/bin/curl" <<'EOF'
#!/bin/sh
printf '%s\n' '{"hits":[{"title":"fresh","url":"https://fake.example/fresh","points":1}]}'
EOF
cat > "$td/bin/claude" <<'EOF'
#!/bin/sh
printf '%s\n' 'autonomous selection: choose the measured default and record its seed'
EOF
cat > "$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x "$td/bin/curl" "$td/bin/claude" "$td/bin/mesh-chat"

out="$(HOME="$td" PATH="$td/bin:/usr/bin:/bin" MESH_AUTONOMY=1 \
  timeout 10 "$ROOT/scripts/mesh-study" 2>&1)"
grep -q 'distilled -> study.log' <<<"$out"
grep -q 'autonomous selection' "$td/.mesh/study.log"

mkdir -p "$td/.mesh/channels"
printf '%s\n' learning > "$td/.mesh/learnings.log"
printf '%s\n' chaos > "$td/.mesh/chaos.log"
printf '%s\n' roadmap > "$td/.mesh/roadmap.md"
out="$(HOME="$td" PATH="$td/bin:/usr/bin:/bin" MESH_AUTONOMY=1 \
  timeout 10 "$ROOT/scripts/mesh-reflect" 2>&1)"
grep -q 'reflection appended to telos.log' <<<"$out"
grep -q 'autonomous selection' "$td/.mesh/telos.log"

out="$(HOME="$td" PATH="$td/bin:/usr/bin:/bin" MESH_AUTONOMY=0 \
  timeout 10 "$ROOT/scripts/mesh-study" 2>&1)"
grep -q 'a mind may self-distill' <<<"$out"

out="$(HOME="$td" PATH="$td/bin:/usr/bin:/bin" MESH_AUTONOMY=0 MESH_STUDY_AUTO=1 \
  timeout 10 "$ROOT/scripts/mesh-study" 2>&1)"
grep -q 'distilled -> study.log' <<<"$out"

echo 'autonomy-defaults: ok'
