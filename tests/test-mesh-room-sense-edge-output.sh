#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-room-sense"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
home="$td/home"
bin="$home/.local/bin"
mesh="$td/mesh"
mkdir -p "$bin" "$home/.mesh" "$mesh"

cat >"$bin/mesh-presence" <<'EOF'
#!/usr/bin/env bash
if [ "${1:-}" = --addrtype-map ]; then exit 0; fi
if [ -f "$MESH_DIR/fixture-present" ]; then
  printf '%s\n' '-60|AA:BB:CC:DD:EE:01|iPhone'
else
  printf '%s\n' '=== mesh-presence fixture — 0 device(s) in range ==='
fi
EOF
cat >"$bin/mesh-phone-ip" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat >"$bin/mesh-peer-addr" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat >"$bin/mesh-ambient-level" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'SILENCE'
EOF
cat >"$bin/mesh-wifi-motion" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'STILL'
EOF
cat >"$bin/mesh-light" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'DARK source=fixture'
EOF
cat >"$bin/mesh-screen-state" <<'EOF'
#!/usr/bin/env bash
exit 2
EOF
cat >"$bin/mesh-state-touch" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat >"$bin/mesh-note3-gfxinfo" <<'EOF'
#!/usr/bin/env bash
exit 2
EOF
chmod +x "$bin"/*

run_edge() {
  HOME="$home" MESH_DIR="$mesh" MESH_ROOM_AUDIO_SELF=SILENT \
    PATH="$bin:$PATH" "$tool" --edge
}

# First evaluation seeds the cached verdict and must not emit an edge.
seed="$(run_edge)"
[ -z "$seed" ] || { echo "FAIL: seed emitted output: $seed"; exit 1; }
grep -q '^EMPTY|' "$mesh/.room-sense.state" \
  || { echo 'FAIL: producer did not seed EMPTY state'; exit 1; }

# A single changed sample is held by the producer's two-scan debounce.
touch "$mesh/fixture-present"
hold="$(run_edge)"
[ -z "$hold" ] || { echo "FAIL: first changed sample emitted: $hold"; exit 1; }
grep -q '^EMPTY|' "$mesh/.room-sense.state" \
  || { echo 'FAIL: debounce changed state on first candidate'; exit 1; }

# The second agreeing sample confirms the transition and emits the real wake line.
fire="$(run_edge)"
case "$fire" in
  *'[room-sense] PRESENT'*) : ;;
  *) echo "FAIL: confirmed producer edge did not emit: $fire"; exit 1 ;;
esac
grep -q '^PRESENT|' "$mesh/.room-sense.state" \
  || { echo 'FAIL: confirmed producer edge did not persist PRESENT'; exit 1; }
[ "$(wc -l < "$mesh/room-sense-tape.log")" -eq 3 ] \
  || { echo 'FAIL: observation tape must record all three evaluations'; exit 1; }

echo 'mesh-room-sense producer edge output: PASS'
