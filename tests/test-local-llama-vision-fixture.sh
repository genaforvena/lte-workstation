#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
fixture="${VISION_FIXTURE:-$repo/docs/board.png}"
base_url="${LLAMA_SERVER_URL:-http://127.0.0.1:43747}"

[[ -s "$fixture" ]] || { echo "test-local-llama-vision-fixture: FAIL (missing fixture: $fixture)" >&2; exit 1; }
python3 - "$fixture" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = path.read_bytes()
assert data.startswith(b"\x89PNG\r\n\x1a\n"), f"not a PNG: {path}"
assert len(data) > 1024, f"fixture is implausibly small: {path}"
PY

models="$(curl -fsS --max-time 5 "$base_url/v1/models" 2>/dev/null)" || {
    echo "test-local-llama-vision-fixture: n/a (llama-server unavailable at $base_url)"
    exit 2
}
model="$(printf '%s' "$models" | python3 -c '
import json,sys
d=json.load(sys.stdin)
entries=d.get("models", []) + d.get("data", [])
for m in entries:
    if "multimodal" in m.get("capabilities", []):
        print(m.get("id") or m.get("name")); break
')"
[[ -n "$model" ]] || { echo "test-local-llama-vision-fixture: FAIL (no multimodal model advertised)" >&2; exit 1; }

request="$(mktemp)"
response="$(mktemp)"
trap 'rm -f "$request" "$response"' EXIT
python3 - "$fixture" "$model" >"$request" <<'PY'
import base64, json, sys
image = base64.b64encode(open(sys.argv[1], "rb").read()).decode()
print(json.dumps({
    "model": sys.argv[2],
    "messages": [{"role": "user", "content": [
        {"type": "text", "text": "Read the title bar in this image. Reply with the exact visible title."},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + image}},
    ]}],
    "temperature": 0.0,
    "max_tokens": 100,
}))
PY

curl -fsS --max-time 30 "$base_url/v1/chat/completions" \
    -H 'Content-Type: application/json' -d "@$request" >"$response" || {
    echo "test-local-llama-vision-fixture: FAIL (multimodal request failed)" >&2
    exit 1
}
python3 - "$response" <<'PY'
import json, re, sys
data = json.load(open(sys.argv[1]))
answer = data["choices"][0]["message"]["content"].strip()
assert re.search(r"mesh.*chat.*board", answer, re.I), f"OCR predicate failed: {answer!r}"
print(f"test-local-llama-vision-fixture: PASS (model={data.get('model', 'unknown')}; answer={answer!r})")
PY
