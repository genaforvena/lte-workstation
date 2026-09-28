#!/usr/bin/env bash
set -u -o pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

study="$td/study"
mkdir -p "$study/runs/fleet-study-v1" "$study/corpus/study-v1"
printf '{}\n' > "$study/runs/fleet-study-v1/registration.json"
printf '{}\n' > "$study/corpus/study-v1/manifest.json"
launcher="$td/launcher"
printf '#!/usr/bin/env bash\nprintf launched > "$MESH_STUDY_AUTOWAKE_MARKER"\n' > "$launcher"
chmod +x "$launcher"

state="$study/runs/fleet-study-v1/autonomy-readiness.json"
env_base=(MESH_STUDY_ROOT="$study" MESH_STUDY_LAUNCH="$launcher" MESH_STUDY_AUTOWAKE_STATE="$state" MESH_STUDY_AUTOWAKE_MARKER="$td/launched")

if env "${env_base[@]}" "$ROOT/scripts/mesh-study-autowake"; then :; else
  echo 'mesh-study-autowake: missing frozen adapters must be a quiet wait' >&2
  exit 1
fi
[ -s "$state" ] || { echo 'mesh-study-autowake: no waiting receipt' >&2; exit 1; }
grep -q '"status": "waiting"' "$state" || { echo 'mesh-study-autowake: wrong waiting status' >&2; exit 1; }
[ ! -e "$td/launched" ] || { echo 'mesh-study-autowake: launched before readiness' >&2; exit 1; }

for adapter in study-pooled study-toy_passage_ppl study-executable_code study-rated_style study-adversarial_safety; do
  mkdir -p "$study/adapters/$adapter"
done
env "${env_base[@]}" "$ROOT/scripts/mesh-study-autowake"
[ -e "$td/launched" ] || { echo 'mesh-study-autowake: did not launch when ready' >&2; exit 1; }

# A slow study must not be relaunched by the next five-minute tick. The first
# launcher holds its process open until the fixture releases it.
cat > "$launcher" <<'EOF'
#!/usr/bin/env bash
printf 'launched\n' >> "$MESH_STUDY_AUTOWAKE_MARKER"
touch "$MESH_STUDY_AUTOWAKE_READY"
while [ ! -e "$MESH_STUDY_AUTOWAKE_RELEASE" ]; do sleep 0.05; done
EOF
chmod +x "$launcher"
rm -f "$td/launched"
env "${env_base[@]}" MESH_STUDY_AUTOWAKE_READY="$td/ready" \
  MESH_STUDY_AUTOWAKE_RELEASE="$td/release" "$ROOT/scripts/mesh-study-autowake" &
first=$!
for i in {1..40}; do [ -e "$td/ready" ] && break; sleep 0.05; done
[ -e "$td/ready" ] || { echo 'mesh-study-autowake: first launch did not start' >&2; exit 1; }
timeout 2 env "${env_base[@]}" MESH_STUDY_AUTOWAKE_READY="$td/ready2" \
  MESH_STUDY_AUTOWAKE_RELEASE="$td/release" "$ROOT/scripts/mesh-study-autowake"
second_rc=$?
launched="$(wc -l < "$td/launched")"
touch "$td/release"
wait "$first"
[ "$second_rc" -eq 0 ] && [ "$launched" -eq 1 ] \
  || { echo "mesh-study-autowake: duplicate active study launch (rc=$second_rc count=$launched)" >&2; exit 1; }
env "${env_base[@]}" MESH_STUDY_AUTOWAKE_READY="$td/ready3" \
  MESH_STUDY_AUTOWAKE_RELEASE="$td/release" "$ROOT/scripts/mesh-study-autowake"
[ "$(wc -l < "$td/launched")" -eq 2 ] \
  || { echo 'mesh-study-autowake: completed launch did not release lock' >&2; exit 1; }

echo 'test-mesh-study-autowake: PASS'
