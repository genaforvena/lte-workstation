#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
recorder="$repo/scripts/mesh-token-usage-recorder"
td="$(mktemp -d -t mesh-token-recorder-test.XXXXXX)"
trap 'rm -rf "$td"' EXIT
store="$td/store"
event="$td/event.json"

cat >"$event" <<'JSON'
{"type":"agent-turn-complete","engine":"codex","provider":"openai","model":"gpt-test","thread-id":"thread-1","turn-id":"turn-1","window":"genome","received_at":1788842122.9,"usage":{"total":12,"input":8,"cached_input":2,"output":4,"reasoning":1},"message":"must not be retained","cwd":"/secret"}
JSON

expect_fail() { if "$@" >/dev/null 2>&1; then echo "expected failure: $*" >&2; exit 1; fi; }

out="$($recorder --store "$store" --event-file "$event")"
[[ "$out" == *"recorded"* ]]
records="$store/records.jsonl"
[[ "$(wc -l <"$records")" -eq 1 ]]
python3 - "$records" <<'PY'
import json, pathlib, sys
r=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert r["event_key"] == "codex:thread-1:turn-1"
assert r["usage"] == {"total":12,"input":8,"cached_input":2,"output":4,"reasoning":1}
assert "message" not in r and "cwd" not in r
assert r["raw"] == {"type":"agent-turn-complete","engine":"codex","provider":"openai","model":"gpt-test","thread-id":"thread-1","turn-id":"turn-1","window":"genome","received_at":1788842122.9,"usage":{"total":12,"input":8,"cached_input":2,"output":4,"reasoning":1}}
PY

[[ "$(stat -c %a "$store")" == 700 && "$(stat -c %a "$records")" == 600 ]]
[[ "$($recorder --store "$store" --event-file "$event")" == *"duplicate"* ]]
[[ "$(wc -l <"$records")" -eq 1 ]]

sed 's/"total":12/"total":13/' "$event" >"$td/conflict.json"
expect_fail "$recorder" --store "$store" --event-file "$td/conflict.json"
[[ -s "$store/conflicts.jsonl" ]]
[[ "$(wc -l <"$records")" -eq 1 ]]

printf '%s\n%s\n' "$(cat "$event")" "$(cat "$event")" >"$td/replay.jsonl"
[[ "$($recorder --store "$store" --replay "$td/replay.jsonl")" == *"2 duplicate"* ]]
[[ "$(wc -l <"$records")" -eq 1 ]]

cat >"$td/timestamp-free.json" <<'JSON'
{"type":"agent-turn-complete","engine":"codex","thread-id":"thread-no-time","turn-id":"turn-no-time","window":"genome","usage":{"input":1}}
JSON
timestamp_free_store="$td/timestamp-free-store"
[[ "$($recorder --store "$timestamp_free_store" --event-file "$td/timestamp-free.json")" == *"recorded"* ]]
[[ "$($recorder --store "$timestamp_free_store" --event-file "$td/timestamp-free.json")" == *"duplicate"* ]]
timestamp_free_records="$timestamp_free_store/records.jsonl"
[[ "$(wc -l <"$timestamp_free_records")" -eq 1 ]]
python3 - "$timestamp_free_records" <<'PY'
import json, pathlib, sys
r=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert r["observed_at"] is None
PY

cat >"$td/missing.json" <<'JSON'
{"type":"agent-turn-complete","engine":"codex","thread-id":"thread-1","usage":{"input":1}}
JSON
expect_fail "$recorder" --store "$store" --event-file "$td/missing.json"
[[ -s "$store/quarantine.jsonl" ]]

echo "token-recorder-test: ok (record, privacy, permissions, duplicate, conflict, replay, quarantine)"
