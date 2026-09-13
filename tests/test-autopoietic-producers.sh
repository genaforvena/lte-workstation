#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

export HOME="$TMP/home"
export MESH="$TMP/mesh"
export MESH_DIR="$MESH"
mkdir -p "$HOME" "$MESH"

test -x "$ROOT/scripts/mesh-autopoiesis"

if ! "$ROOT/scripts/mesh-autopoiesis" --test; then
  echo "mesh-autopoiesis --test failed" >&2
  exit 1
fi

printf '%s\n' 'raw novelty without an acceptance predicate' \
  | "$ROOT/scripts/mesh-autopoiesis" intake --producer literature --raw \
  || { echo "incomplete novelty intake was rejected instead of retained" >&2; exit 1; }
grep -q 'raw novelty without an acceptance predicate' "$MESH/ideas-queue"

stub="$TMP/mesh-task-stub"
printf '%s\n' '#!/usr/bin/env bash' 'printf "delegated:%s\\n" "$*" > "$TASK_STUB_OUT"' > "$stub"
chmod +x "$stub"
cat > "$TMP/eligible.tsv" <<'EOF'
#origin.kind=literature
#origin.source=source:test-producer
#origin.hypothesis=the bounded mechanism passes
#origin.question=does the real predicate pass?
#origin.acceptance=command exits zero
#origin.feedback=adopt on pass; retain negative evidence otherwise
discover\treview-source\t90\twrite the review artifact
EOF
TASK_STUB_OUT="$TMP/delegated" MESH_TASK_BIN="$stub" \
  "$ROOT/scripts/mesh-autopoiesis" admit --plan "$TMP/eligible.tsv"
grep -q 'delegated:create eligible' "$TMP/delegated"

cat > "$TMP/incomplete.tsv" <<'EOF'
#origin.kind=literature
#origin.source=source:incomplete
discover\treview-source\tmissing fields
EOF
if MESH_TASK_BIN="$stub" "$ROOT/scripts/mesh-autopoiesis" admit --plan "$TMP/incomplete.tsv"; then
  echo "incomplete envelope was admitted" >&2
  exit 1
fi

grep -q 'mesh-autopoiesis' "$ROOT/scripts/mesh-ideate"
grep -q 'mesh-autopoiesis' "$ROOT/scripts/mesh-needs"

echo 'test-autopoietic-producers: ok'
