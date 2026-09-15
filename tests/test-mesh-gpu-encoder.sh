#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-gpu-encoder"
td="$(mktemp -d)" || exit 1
trap 'rm -rf "$td"' EXIT

cat >"$td/smi-ok" <<'EOF'
#!/usr/bin/env bash
printf '0, 37\n1, 4\n'
EOF
cat >"$td/smi-na" <<'EOF'
#!/usr/bin/env bash
printf '0, N/A\n'
EOF
chmod +x "$td/smi-ok" "$td/smi-na"

out="$(MESH_GPU_ENCODER_SMI="$td/smi-ok" "$TOOL" --json 2>/dev/null)" || {
  echo 'FAIL: parses two encoder engine readings' >&2; exit 1;
}
[[ "$out" == *'"gpu_index":0,"encoder_utilization_percent":37'* &&
   "$out" == *'"gpu_index":1,"encoder_utilization_percent":4'* ]] || {
  echo "FAIL: unexpected readings: $out" >&2; exit 1;
}

MESH_GPU_ENCODER_SMI="$td/smi-na" "$TOOL" --json >/dev/null 2>&1
rc=$?
[[ "$rc" -eq 2 ]] || { echo "FAIL: N/A must exit 2 (got $rc)" >&2; exit 1; }

echo 'PASS: GPU encoder utilization parser and unavailable path'
