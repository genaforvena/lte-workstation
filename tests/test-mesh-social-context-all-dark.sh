#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo_root/scripts/mesh-social-context"
tmpd="$(mktemp -d)"
trap 'rm -rf "$tmpd"' EXIT
home="$tmpd/home"
bin="$home/.local/bin"
mkdir -p "$home/.mesh" "$bin"
printf 'DEGRADED\n' > "$home/.mesh/.social-context.state"

# The phone address resolves, but every actual source read is empty or unknown.
cat > "$bin/mesh-audio-energy" <<'EOF'
#!/bin/sh
printf '%s\n' '{"state":"UNKNOWN","rms":null}'
EOF
cat > "$bin/mesh-body-motion" <<'EOF'
#!/bin/sh
echo UNKNOWN
exit 0
EOF
cat > "$bin/mesh-light" <<'EOF'
#!/bin/sh
echo UNKNOWN
exit 0
EOF
cat > "$bin/mesh-presence" <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x "$bin"/*

rc=0
HOME="$home" PATH="$bin:$PATH" "$tool" > "$tmpd/output" 2>&1 || rc=$?
if [ "$rc" -ne 2 ]; then
  echo "FAIL: all-dark fusion must exit 2, got $rc: $(tail -1 "$tmpd/output")"
  exit 1
fi
if [ ! -f "$home/.mesh/.social-context-offline" ]; then
  echo "FAIL: all-dark fusion did not publish its blind marker"
  exit 1
fi
if [ -e "$home/.mesh/.social-context.state" ]; then
  echo "FAIL: all-dark fusion left the prior DEGRADED label available as a live reading"
  exit 1
fi
if grep -q 'DEGRADED\|EMPTY' "$tmpd/output"; then
  echo "FAIL: all-dark fusion emitted a readable verdict: $(tail -1 "$tmpd/output")"
  exit 1
fi
echo "ok: resolved phone address with no live inputs yields a fresh blind marker and exit 2"
