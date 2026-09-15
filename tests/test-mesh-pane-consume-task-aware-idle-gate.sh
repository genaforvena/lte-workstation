#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-pane-consume"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/mesh-task" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  "queue --dispatch --owner genome")
    if [ "${MESH_TASK_CANDIDATE_OWNER:-}" = genome ]; then
      printf 'genome\tchain/step\t95\teligible exact-owner work\n'
    fi
    printf 'witness\tother/step\t95\tother owner work\n'
    ;;
  "check dispatch chain/step genome") exit 0 ;;
  *) exit 1 ;;
esac
EOF
chmod +x "$td/mesh-task"
mkdir -p "$td/expect"
printf '# expires: %s\n^state=UP$\n' "$(( $(date +%s) + 600 ))" > "$td/expect/genome"

candidate="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=genome \
  "$tool" --task-candidate genome)"
[ "$candidate" = $'genome\tchain/step\t95\teligible exact-owner work' ] || {
  echo "FAIL: exact-owner candidate was not surfaced: $candidate" >&2
  exit 1
}

message="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=genome \
  "$tool" --wake-message genome)"
printf '%s' "$message" | grep -Fq \
  'Eligible exact-owner task candidate: chain/step. Owner-authored take is required: MESH_TASK_ACTOR=genome mesh-task take chain step.' || {
  echo "FAIL: wake did not surface the exact candidate with an owner-authored take: $message" >&2
  exit 1
}

ordinary_empty="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" "$tool" --wake-message blocked)"
if printf '%s' "$ordinary_empty" | grep -Fq 'create one canonical exact-owner task'; then
  echo "FAIL: a routine telemetry wake must not bypass the recurring self-pick spend gate" >&2
  exit 1
fi
fallback="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" "$tool" --wake-message blocked --self-pick)"
printf '%s' "$fallback" | grep -Fq 'Do not reject a blocked task' || {
  echo "FAIL: no-candidate wake did not forbid rejection as an idle shortcut: $fallback" >&2
  exit 1
}
printf '%s' "$fallback" | grep -Fq 'create one canonical exact-owner task' || {
  echo "FAIL: no-candidate wake did not require bounded self-authored work: $fallback" >&2
  exit 1
}

retry_due="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_PICK_RETRY=900 \
  "$tool" --task-retry-check 'genome eligible candidate' 100 1000)"
[ "$retry_due" = due ] || { echo "FAIL: a still-eligible task must be re-offered after the retry interval, got: $retry_due" >&2; exit 1; }
retry_early="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_PICK_RETRY=900 \
  "$tool" --task-retry-check 'genome eligible candidate' 500 1000 || true)"
[ "$retry_early" = hold ] || { echo "FAIL: a task prompt retry must respect its interval, got: $retry_early" >&2; exit 1; }
retry_empty="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_PICK_RETRY=900 \
  "$tool" --task-retry-check '' 0 10000 || true)"
[ "$retry_empty" = hold ] || { echo "FAIL: no candidate must not cause recurring task prompts, got: $retry_empty" >&2; exit 1; }

printf '^state=UP$\n^queue depth [0-9]+$\n' >> "$td/expect/genome"
cp "$td/expect/genome" "$td/expect/blocked"
eligible_gate="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=genome \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --gate-check genome \
  'state=UP' $'state=UP\nqueue depth 2' 2)"
case "$eligible_gate" in
  WAKE:deaf:task) ;;
  *) echo "FAIL: eligible exact-owner work must keep the wake candidate, got: $eligible_gate" >&2; exit 1 ;;
esac

blocked="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=blocked \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --gate-check blocked \
  'state=UP' $'state=UP\nqueue depth 2' 2)"
[ "$blocked" = 'HOLD:no-eligible' ] || {
  echo "FAIL: unchanged blocked/no-eligible state must hold, got: $blocked" >&2
  exit 1
}

absent="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=blocked \
  MESH_WAKE_EXPECT_DIR="$td/no-expect" "$tool" --gate-check blocked \
  'state=UP' 'state=UP' 0)"
[ "$absent" = 'HOLD:no-eligible' ] || {
  echo "FAIL: absent expectation plus unchanged no-candidate state must hold, got: $absent" >&2
  exit 1
}

printf '# expires: %s\n^state=UP$\n' "$(( $(date +%s) - 10 ))" > "$td/expect/expired"
expired="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=blocked \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --gate-check expired \
  'state=UP' 'state=UP' 0)"
[ "$expired" = 'HOLD:no-eligible' ] || {
  echo "FAIL: expired expectation plus unchanged no-candidate state must hold, got: $expired" >&2
  exit 1
}

printf '# expires: %s\n^state=(UP|DOWN)$\n' "$(( $(date +%s) - 10 ))" > "$td/expect/expired-match"
expired_match="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=blocked \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --task-transition-check expired-match \
  '' '' 'state=UP' 'state=DOWN' 0)"
[ "$expired_match" = 'HOLD:no-eligible' ] || {
  echo "FAIL: expired expectation plus changed fully-predicted pane delta must hold, got: $expired_match" >&2
  exit 1
}

expired_surprise="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=blocked \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --task-transition-check expired-match \
  '' '' 'state=UP' $'state=DOWN\nnovel=1' 0)"
case "$expired_surprise" in
  WAKE:plain|WAKE:surprise:*) ;;
  *) echo "FAIL: expired expectation plus an unpredicted pane line must wake, got: $expired_surprise" >&2; exit 1 ;;
esac

empty_to_eligible="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=genome \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --task-transition-check genome \
  '' 'genome\tchain/step\t95\tel eligible' 'state=UP' 'state=UP' 0)"
case "$empty_to_eligible" in
  WAKE:surprise:task) ;;
  *) echo "FAIL: empty-to-eligible transition must wake, got: $empty_to_eligible" >&2; exit 1 ;;
esac

eligible_to_empty="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=blocked \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --task-transition-check blocked \
  'genome\tchain/step\t95\tel eligible' '' 'state=UP' 'state=UP' 0)"
[ "$eligible_to_empty" = 'HOLD:no-eligible' ] || {
  echo "FAIL: eligible-to-empty transition must not buy a follow-up owner turn, got: $eligible_to_empty" >&2
  exit 1
}

surprise="$(PATH="$td:/usr/bin:/bin" HOME="$td/home" MESH_TASK_CANDIDATE_OWNER=blocked \
  MESH_WAKE_EXPECT_DIR="$td/expect" "$tool" --gate-check blocked \
  'state=UP' $'state=DOWN\ntask state changed' 0)"
case "$surprise" in
  WAKE:surprise:*) ;;
  *) echo "FAIL: unpredicted pane/task-state change must still wake, got: $surprise" >&2; exit 1 ;;
esac

echo 'test-mesh-pane-consume-task-aware-idle-gate: PASS'
