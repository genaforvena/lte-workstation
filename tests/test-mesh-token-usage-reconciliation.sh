#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
reconciler="$repo/scripts/mesh-token-usage-reconcile"
td="$(mktemp -d -t mesh-token-reconcile-test.XXXXXX)"
trap 'rm -rf "$td"' EXIT

cat >"$td/records.jsonl" <<'JSONL'
{"event_key":"codex:t:p","usage":{"total":12,"input":8,"cached_input":2,"output":4,"reasoning":1}}
{"event_key":"codex:t:m","usage":{"total":13,"input":8,"cached_input":2,"output":4,"reasoning":1}}
{"event_key":"codex:t:x","usage":{"total":null,"input":8,"cached_input":2,"output":4,"reasoning":null}}
{"event_key":"codex:t:n","usage":{"total":12,"input":8,"cached_input":9,"output":4,"reasoning":1}}
JSONL

"$reconciler" --records "$td/records.jsonl" --output "$td/report.json" >/dev/null
python3 - "$td/report.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
rows = {x["event_key"]: x for x in r["rows"]}
assert rows["codex:t:p"]["reconciliation"]["status"] == "pass"
assert rows["codex:t:p"]["reconciliation"]["total_check"] == "match"
assert rows["codex:t:p"]["reconciliation"]["non_additive"] == "pass"
assert rows["codex:t:m"]["reconciliation"]["status"] == "mismatch"
assert rows["codex:t:x"]["reconciliation"]["status"] == "missing"
assert rows["codex:t:n"]["reconciliation"]["non_additive"] == "mismatch"
assert r["summary"] == {"rows": 4, "pass": 1, "missing": 1, "mismatch": 2}
PY

cp "$td/report.json" "$td/first.json"
"$reconciler" --records "$td/records.jsonl" --output "$td/report.json" >/dev/null
cmp "$td/first.json" "$td/report.json"

echo "token-reconciliation-test: ok (match, non-additive, missing, mismatch, replay)"
