#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-gpu-display"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/nvidia-smi" <<'EOF'
#!/usr/bin/env bash
printf 'GPU-d8865ef1-4f85-b7a9-43e0-3af1bd46a3ef, 00000000:2B:00.0, No, Disabled\n'
EOF
chmod +x "$td/nvidia-smi"

out="$(MESH_GPU_DISPLAY_SMI="$td/nvidia-smi" "$TOOL")"
[ "$out" = '[gpu-display] display_attached=No display_active=Disabled gpu=GPU-d8865ef1-4f85-b7a9-43e0-3af1bd46a3ef pci=00000000:2B:00.0' ] || {
  echo "FAIL: fixture read: $out" >&2
  exit 1
}

json="$(MESH_GPU_DISPLAY_SMI="$td/nvidia-smi" "$TOOL" --json)"
printf '%s\n' "$json" | grep -q '"display_attached":"No"' || { echo "FAIL: JSON attachment field" >&2; exit 1; }
printf '%s\n' "$json" | grep -q '"display_active":"Disabled"' || { echo "FAIL: JSON active field" >&2; exit 1; }

cat >"$td/bad-smi" <<'EOF'
#!/usr/bin/env bash
printf 'GPU, bus, maybe, maybe\n'
EOF
chmod +x "$td/bad-smi"
MESH_GPU_DISPLAY_SMI="$td/bad-smi" "$TOOL" >/dev/null 2>&1 && {
  echo "FAIL: malformed nvidia-smi output must fail" >&2
  exit 1
}

echo "test-mesh-gpu-display: ok"
