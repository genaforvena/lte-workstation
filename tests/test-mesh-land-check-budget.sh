#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/repo/scripts" "$td/home/.mesh" "$td/bin"
git -C "$td/repo" init -q
git -C "$td/repo" config user.email test@example.invalid
git -C "$td/repo" config user.name test
printf 'seed\n' > "$td/repo/README.md"
git -C "$td/repo" add README.md
git -C "$td/repo" commit -qm seed
git -C "$td/repo" branch -M main
git init -q --bare "$td/origin.git"
git -C "$td/repo" remote add origin "$td/origin.git"
git -C "$td/repo" push -q -u origin main
for name in mesh-slow-one mesh-slow-two; do
    printf '#!/usr/bin/env bash\ncase "${1:-}" in --test) sleep 8; exit 0;; esac\n' > "$td/repo/scripts/$name"
    chmod +x "$td/repo/scripts/$name"
done
printf '%s\n' 'mesh_manifest_source_paths(){ printf "%s\n" scripts/mesh-slow-one scripts/mesh-slow-two; }' > "$td/manifest-reader.sh"
printf '#!/bin/sh\nprintf "%%s\\n" "$*" >> "$TEST_BOARD"\nexit 0\n' > "$td/bin/mesh-chat"
chmod +x "$td/bin/mesh-chat"

start="$(date +%s)"
set +e
HOME="$td/home" PATH="$td/bin:$PATH" TEST_BOARD="$td/board" MESH_REPO="$td/repo" \
    MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_SETTLE=0 \
    MESH_LAND_CHECK_BULK_THRESHOLD=1 MESH_LAND_CHECK_BACKLOG="$td/backlog.tsv" \
    MESH_LAND_CHECK_BACKLOG_STATE="$td/backlog.state" \
    MESH_LAND_CHECK_POOL=2 MESH_LAND_CHECK_BUDGET=2 \
    MESH_LAND_TEST_FLOOR=1 MESH_LAND_TEST_TIMEOUT=20 \
    bash "$repo_root/scripts/mesh-land" --check > "$td/out" 2>&1
rc=$?
set -e
elapsed=$(( $(date +%s) - start ))
[[ "$rc" -eq 1 ]]
[[ "$elapsed" -lt 6 ]] || { echo "FAIL: --check ignored its 2s pool (elapsed=${elapsed}s)" >&2; exit 1; }
grep -Fq 'land-backlog/' "$td/board"
[[ "$(wc -l < "$td/backlog.tsv")" -eq 3 ]]
grep -Fq $'path\tage_s\treason\tnext_action' "$td/backlog.tsv"
HOME="$td/home" PATH="$td/bin:$PATH" TEST_BOARD="$td/board" MESH_REPO="$td/repo" \
    MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_SETTLE=0 \
    MESH_LAND_CHECK_BULK_THRESHOLD=1 MESH_LAND_CHECK_BACKLOG="$td/backlog.tsv" \
    MESH_LAND_CHECK_BACKLOG_STATE="$td/backlog.state" \
    bash "$repo_root/scripts/mesh-land" --check > /dev/null 2>&1 || true
[[ "$(grep -Fc 'land-backlog/' "$td/board")" -eq 1 ]] || {
    echo 'FAIL: unchanged backlog posted a second task because observation time changed' >&2
    exit 1
}

(
    exec 9> "$td/run.lock"
    flock 9
    sleep 5
) &
holder=$!
for _ in $(seq 1 100); do
    flock -n "$td/run.lock" true 2>/dev/null || break
    sleep 0.01
done
set +e
HOME="$td/home" PATH="$td/bin:$PATH" TEST_BOARD="$td/board" MESH_REPO="$td/repo" \
    MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_RUN_LOCK="$td/run.lock" \
    bash "$repo_root/scripts/mesh-land" --autoland > "$td/overlap.out" 2>&1
overlap_rc=$?
set -e
kill "$holder" 2>/dev/null || true
wait "$holder" 2>/dev/null || true
[[ "$overlap_rc" -eq 1 ]]
grep -Fq 'autoland overlap refused' "$td/overlap.out"
grep -Fq '[health-fail] mesh-land: autoland overlap refused' "$td/board"

overlap_board_before="$(grep -Fc '[health-fail] mesh-land: autoland overlap refused' "$td/board")"
(
    exec 9> "$td/run.lock"
    flock 9
    sleep 5
) &
overlap_holder=$!
for _ in $(seq 1 100); do
    flock -n "$td/run.lock" true 2>/dev/null || break
    sleep 0.01
done
set +e
for _ in 1 2; do
    HOME="$td/home" PATH="$td/bin:$PATH" TEST_BOARD="$td/board" MESH_REPO="$td/repo" \
        MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_RUN_LOCK="$td/run.lock" \
        MESH_LAND_OVERLAP_STATE="$td/overlap.state" MESH_LAND_OVERLAP_TRACE="$td/overlap.trace" \
        bash "$repo_root/scripts/mesh-land" --autoland > /dev/null 2>&1
done
set -e
kill "$overlap_holder" 2>/dev/null || true
wait "$overlap_holder" 2>/dev/null || true
[[ "$(grep -Fc '[health-fail] mesh-land: autoland overlap refused' "$td/board")" -eq "$(( overlap_board_before + 1 ))" ]] || {
    echo 'FAIL: repeated overlap emitted a duplicate board health-fail' >&2
    exit 1
}
grep -Fq 'overlap alert suppressed' "$td/overlap.trace" || {
    echo 'FAIL: repeated overlap was not recorded in the trace' >&2
    exit 1
}

HOME="$td/home" PATH="$td/bin:$PATH" TEST_BOARD="$td/board" MESH_REPO="$td/repo" \
    MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_SETTLE=0 \
    MESH_LAND_AUTOLAND_BATCH=1 MESH_LAND_AUTOLAND_CURSOR="$td/cursor" \
    MESH_LAND_AUTOLAND_QUEUE="$td/autoland.tsv" MESH_LAND_RUN_LOCK="$td/run.lock" \
    MESH_LAND_TEST_TIMEOUT=1 MESH_LAND_TEST_POOL=1 MESH_LAND_TEST_FLOOR=1 \
    bash "$repo_root/scripts/mesh-land" --autoland > "$td/batch.out" 2>&1 || true
grep -Fq 'autoland batch=1/2 cursor=0 next=1' "$td/batch.out"
[[ "$(cat "$td/cursor")" -eq 1 ]]
[[ "$(wc -l < "$td/autoland.tsv")" -eq 3 ]]

mkdir -p "$td/repo/docs/task-receipts"
printf 'held semantic unit\n' > "$td/repo/docs/task-receipts/held.md"
printf '#!/bin/sh\ntouch "$AUTOWIRE_CALLED"\nsleep 8\n' > "$td/bin/mesh-autowire"
chmod +x "$td/bin/mesh-autowire"
printf '2\n' > "$td/cursor"
HOME="$td/home" PATH="$td/bin:$PATH" TEST_BOARD="$td/board" AUTOWIRE_CALLED="$td/autowire-called" \
    MESH_REPO="$td/repo" MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_SETTLE=0 \
    MESH_LAND_AUTOLAND_BATCH=1 MESH_LAND_AUTOLAND_CURSOR="$td/cursor" \
    MESH_LAND_AUTOLAND_QUEUE="$td/autoland.tsv" MESH_LAND_RUN_LOCK="$td/run.lock" \
    bash "$repo_root/scripts/mesh-land" --autoland > "$td/held.out" 2>&1 || true
[[ ! -e "$td/autowire-called" ]] || {
    echo 'FAIL: held-only batch ran deploy wiring despite landing zero units' >&2
    exit 1
}
echo 'mesh-land-check-budget: PASS (large checks inventory once; autoland locks and rotates bounded batches)'
