#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
reporter="$repo/scripts/mesh-token-usage-report"
td="$(mktemp -d -t mesh-token-report-test.XXXXXX)"
trap 'rm -rf "$td"' EXIT
printf '%s\n%s\n' \
  '{"event_key":"codex:t:1","window":"genome","model":"m","usage":{"total":3,"input":2,"output":1}}' \
  '{"event_key":"codex:t:2","window":"genome","model":"m","usage":{"total":null,"input":2,"output":null}}' >"$td/records.jsonl"
"$reporter" --records "$td/records.jsonl" >"$td/out.json"
python3 - "$td/out.json" <<'PY'
import json, sys
r=json.load(open(sys.argv[1]))
assert r["groups"] == [{"model":"m","rows":2,"missing_fields":6,"window":"genome"}]
PY
echo "token-report-test: ok (grouped coverage and missing fields)"
