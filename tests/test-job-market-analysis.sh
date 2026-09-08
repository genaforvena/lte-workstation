#!/usr/bin/env bash
set -eu

repo="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
tool="$repo/job/mesh-job-market-analysis"
weekly="$repo/job/mesh-job-market-analysis-weekly"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/job" "$td/out"

printf '# date\tcompany\trole\tlink\tstate\tnote\treason\n2026-09-01\tA\tLead Go Engineer\thttps://hh.ru/vacancy/101\tviewed\tscan 2026-09-01 | запрос: team lead go | remote | от 500000 ₽\t\n2026-09-02\tB\tLLM Platform Engineer\thttps://jobs.ashbyhq.com/b/abc\tseen\tashby-scan 2026-09-02 | geo=UNSET | compensation not published\t\n2026-09-03\tC\tDSP Engineering Lead\thttps://hh.ru/vacancy/102\trejected\tscan 2026-09-03 | запрос: dsp lead | зарплата не указана\t\n' > "$td/board.tsv"
printf '2026-09-04T10:00:00Z\t101\tA\tLead Go Engineer\n' > "$td/job/sent-log.tsv"
printf 'id\tstate\tdate\ttime\tparticipants\tlink\tplace\tsource\n1\tproposed\t2026-09-10\t10:00\t\thttps://meet/x\t\thh:101\n' > "$td/job/schedule.tsv"
printf '# ts\tstatus\torigin\tquestion\n2026-09-04T11:00:00Z\topen\thh:101\tWhat salary do you expect?\n' > "$td/job/questions.tsv"
printf '2026-09-04T12:00:00Z\t501\tact\temployer\tA\tLead Go Engineer\tMessage\tCan we schedule a call?\n' > "$td/mail.log"
printf '{"900":{"preview":"Lead Go Engineer A Thanks for the reply","seen":"2026-09-04T12:00Z"}}\n' > "$td/job/chatwatch-state.json"

env MESH_JOB_BOARD="$td/board.tsv" MESH_JOB_DIR="$td/job" MESH_JOB_MAIL_LOG="$td/mail.log" \
  MESH_JOB_ANALYSIS_DIR="$td/out" "$tool" --daily >/dev/null

jq -e '.inputs.board.rows == 3 and .identity.unique_links == 3 and .submissions.logged == 1 and .submissions.joined == 1 and .calendar.confirmed == 0 and .chat.questions == 1 and .chat.previews_unknown_author == 1 and .mode == "daily"' "$td/out/latest.json" >/dev/null
grep -q 'current endpoints, not historical conversions' "$td/out/latest.md"
grep -q $'\tsuccess\t' "$td/out/runs.tsv"
test "$(find "$td/out/runs" -type f -name '*.json' | wc -l)" -eq 1

cp "$td/out/latest.json" "$td/last-good.json"
printf '2026-09-05\tD\tDuplicate\thttps://hh.ru/vacancy/101\tseen\tx\t\n' >> "$td/board.tsv"
if env MESH_JOB_BOARD="$td/board.tsv" MESH_JOB_DIR="$td/job" MESH_JOB_MAIL_LOG="$td/mail.log" \
  MESH_JOB_ANALYSIS_DIR="$td/out" "$tool" --weekly >/dev/null 2>&1; then
  echo 'FAIL: duplicate role identity was accepted' >&2
  exit 1
fi
cmp "$td/last-good.json" "$td/out/latest.json"
grep -q $'\tfailure\t' "$td/out/runs.tsv"
env MESH_JOB_BOARD="$td/board.tsv" MESH_JOB_DIR="$td/job" MESH_JOB_MAIL_LOG="$td/mail.log" \
  MESH_JOB_ANALYSIS_DIR="$td/out" "$tool" --test >/dev/null 2>&1 && {
  echo 'FAIL: --test accepted malformed configured real path' >&2
  exit 1
}

rm -f "$td/out/latest.json"
env MESH_JOB_BOARD="$td/board.tsv" MESH_JOB_DIR="$td/job" MESH_JOB_MAIL_LOG="$td/mail.log" \
  MESH_JOB_ANALYSIS_DIR="$td/out" "$weekly" >/dev/null 2>&1 && {
  echo 'FAIL: weekly wrapper accepted malformed input' >&2
  exit 1
}
sed -i '$d' "$td/board.tsv"
env MESH_JOB_BOARD="$td/board.tsv" MESH_JOB_DIR="$td/job" MESH_JOB_MAIL_LOG="$td/mail.log" \
  MESH_JOB_ANALYSIS_DIR="$td/out" "$weekly" >/dev/null
jq -e '.mode == "weekly"' "$td/out/latest.json" >/dev/null
test "$(find "$td/out/runs" -type f -name '*-daily.json' | wc -l)" -ge 1
test "$(find "$td/out/runs" -type f -name '*-weekly.json' | wc -l)" -ge 1
env MESH_JOB_BOARD="$td/board.tsv" MESH_JOB_DIR="$td/job" MESH_JOB_MAIL_LOG="$td/mail.log" \
  MESH_JOB_ANALYSIS_DIR="$td/out" "$weekly" --test >/dev/null

echo 'test-job-market-analysis: ok'
