#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/study/scripts" "$td/study/runs/fleet-study-v1" "$td/home/.local/bin"
cp /bin/true "$td/study/scripts/run_study_matrix.py"
cp /bin/true "$td/study/.venv-python"
printf '{"study_id":"frozen-fixture","arms":[],"statistics":{"seeds":[17,29,43]}}\n' > "$td/study/runs/fleet-study-v1/registration.json"
cat > "$td/home/.local/bin/mesh-heavy-run" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$MESH_STUDY_CAPTURE"
printf 'gpu_min=%s\ngpu_smi=%s\n' "${MESH_HEAVY_GPU_MIN_FREE_MB:-}" "${MESH_HEAVY_GPU_SMI:-}" >> "$MESH_STUDY_CAPTURE"
SH
chmod +x "$td/home/.local/bin/mesh-heavy-run"
MESH_STUDY_ROOT="$td/study" MESH_STUDY_PYTHON="$td/study/.venv-python" \
MESH_STUDY_CAPTURE="$td/capture" HOME="$td/home" PATH="/usr/bin:/bin" \
  "$repo/scripts/mesh-study-launch" >"$td/out" 2>&1 || {
    rc=$?; echo "study-launch-test: FAIL (launcher rc=$rc; $(cat "$td/out"))" >&2; exit 1;
  }
grep -qx '10240' "$td/capture"
grep -qx -- '--' "$td/capture"
grep -qx 'gpu_min=2048' "$td/capture"
grep -qx 'gpu_smi=nvidia-smi' "$td/capture"
grep -Fq "$td/study/scripts/run_study_matrix.py" "$td/capture"
grep -Fq "$td/study/runs/fleet-study-v1/registration.json" "$td/capture"
grep -Fq -- '--gpu-wait-s' "$td/capture"
grep -Fq '60' "$td/capture"
grep -Fq -- '--gpu-min-free-mb' "$td/capture"
grep -Fq '2048' "$td/capture"
grep -Fq '"operator_required": false' "$td/study/runs/fleet-study-v1/autonomy-decision.json"
grep -Fq '"registration_sha256":' "$td/study/runs/fleet-study-v1/autonomy-decision.json"
echo 'study-launch-test: ok (frozen registration, bounded VRAM retry, durable heavy queue invocation)'
