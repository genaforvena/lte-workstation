#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-media-scene"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/gpu-display" <<'EOF'
#!/usr/bin/env bash
printf '{"display_attached":"No","display_active":"Disabled","gpu":"GPU-test","pci":"00000000:2B:00.0"}\n'
EOF
chmod +x "$td/gpu-display"
printf '%s no-tv-here\n' "$(date -u +%FT%TZ)" > "$td/presence"
printf '%s\t-50\tSILENCE\n' "$(date -u +%FT%TZ)" > "$td/mic"

out="$(MESH_MEDIA_WPCTL_CMD=false MESH_MEDIA_IMAC_CMD=false \
  MESH_MEDIA_PRESENCE_LOG="$td/presence" MESH_MEDIA_MIC_TAPE="$td/mic" \
  MESH_MEDIA_GPU_DISPLAY_CMD="$td/gpu-display" "$TOOL" --json)"
printf '%s\n' "$out" | grep -q '"display_attached":"No"' || { echo "FAIL: media JSON omitted display_attached: $out" >&2; exit 1; }
printf '%s\n' "$out" | grep -q '"display_active":"Disabled"' || { echo "FAIL: media JSON omitted display_active: $out" >&2; exit 1; }

echo "test-mesh-media-scene-gpu-display: ok"
