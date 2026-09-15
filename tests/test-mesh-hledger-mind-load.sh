#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/scripts/mesh-hledger-mind-load"
T="$(mktemp -d -t mesh-hledger-mind-load-test.XXXXXX)"
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/home/.mesh" "$T/repo/docs/task-receipts" "$T/bin"
cat > "$T/bin/mesh-task" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' '{"fixture":{"data":{"steps":[{"id":"chain/a","owner":"genome","status":"done","started":"2026-09-09T00:00:00Z","finished":"2026-09-09T00:00:03Z","artifact":"/repo/a.md"},{"id":"chain/b","owner":"tg","status":"open","started":"2026-09-09T00:00:01Z"}]}}}'
EOF
chmod +x "$T/bin/mesh-task"
cat > "$T/home/.mesh/chat.log" <<'EOF'
2026-09-09T00:00:00Z  genome@node :: [task] chain/a → owner: genome
2026-09-09T00:00:01Z  tg@node :: [task] chain/b → owner: tg
2026-09-09T00:00:02Z  genome@node :: [taking] chain/a
2026-09-09T00:00:03Z  genome@node :: [done] chain/a: artifact=/repo/a.md task:chain/a
2026-09-09T00:00:04Z  genome@node :: [taking] chain/a (reopen)
EOF
cat > "$T/home/.mesh/spend.log" <<'EOF'
2026-09-09T00:00:02Z turn genome codex openai paid unknown event:1 task:chain/a
2026-09-09T00:00:03Z turn genome codex openai paid unknown event:2 task:chain/a
2026-09-09T00:00:04Z turn tg codex openai paid unknown event:3
EOF
printf 'receipt\n' > "$T/repo/docs/task-receipts/a.md"
out="$T/report"
HOME="$T/home" PATH="$T/bin:$PATH" MESH_HLEDGER_REPO="$T/repo" \
  "$BIN" --cutoff 2026-09-09T00:00:05Z --output "$out"

grep -q '^report=mesh-load read_only=true cutoff=2026-09-09T00:00:05Z$' "$out"
grep -q '^mind=genome tasks=1 effort_turns=2 age_seconds=3 rework_reopen=1 completion=1/1 outcome_evidence=1/1 unattributed=0 unknown=0$' "$out"
grep -q '^mind=tg tasks=1 effort_turns=0 age_seconds=4 rework_reopen=0 completion=0/1 outcome_evidence=0/0 unattributed=1 unknown=0$' "$out"
grep -q '^coverage=task_owner=2/2 effort_task_attribution=2/3 outcome_evidence=1/1$' "$out"
grep -q '^load_signal=compare effort_turns, task volume, age, completion and attribution; volume is not quality$' "$out"
test ! -e "$T/home/.mesh/journal"
echo 'test-mesh-hledger-mind-load: PASS'
