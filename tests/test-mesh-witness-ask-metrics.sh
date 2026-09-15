#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/promises.json" <<'JSON'
{"asks":[
  {"id":"a","age_h":1.0},
  {"id":"b","age_h":2.0},
  {"id":"c","age_h":10.0},
  {"id":"d","age_h":20.0}
],"ask_closed":{"DONE":4,"DESIGN":0,"DECLINED":0}}
JSON
cat >"$td/promises-bin" <<'SH'
#!/usr/bin/env bash
cat "$MESH_WITNESS_ASK_JSON"
SH
chmod +x "$td/promises-bin"
printf '%s\n' '2026-09-07T18:00:00Z nodes=UNKNOWN minds_live=UNKNOWN minds_work=UNKNOWN reflex=UNKNOWN board1h=UNKNOWN board_age_s=UNKNOWN board_posters=UNKNOWN senses=UNKNOWN spend1h=UNKNOWN' >"$td/witness.log"

out="$(
  HOME="$td" \
  MESH="$td/.mesh" \
  MESH_WITNESS_LEDGER="$td/witness.log" \
  MESH_PROMISES_BIN="$td/promises-bin" \
  MESH_WITNESS_ASK_JSON="$td/promises.json" \
  python3 "$ROOT/scripts/mesh-witness" --json
)"

python3 - "$out" <<'PY'
import json, sys
m = json.loads(sys.argv[1])
assert m["ask_open"] == "1", m
assert m["ask_stale_h"] == "20.0", m
assert m["ask_resolve"] == "0.5", m
assert m["ask_den"] == "8", m
assert m["ask_p90_h"] == "17.0", m
assert m["ask_unknown"] == "0", m
PY
printf '%s\n' "$out"

printf '%s\n' '{"asks":[{"id":"bad"}],"ask_closed":{"DONE":1}}' >"$td/bad.json"
bad_out="$(
  HOME="$td" \
  MESH_WITNESS_LEDGER="$td/witness.log" \
  MESH_PROMISES_BIN="$td/promises-bin" \
  MESH_WITNESS_ASK_JSON="$td/bad.json" \
  python3 "$ROOT/scripts/mesh-witness" --json
)"
python3 - "$bad_out" <<'PY'
import json, sys
m = json.loads(sys.argv[1])
assert m["ask_open"] == "UNKNOWN", m
assert m["ask_stale_h"] == "UNKNOWN", m
assert m["ask_resolve"] == "UNKNOWN", m
assert m["ask_den"] == "2", m
assert m["ask_unknown"] == "1", m
PY
printf '%s\n' "$bad_out"
