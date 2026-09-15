#!/usr/bin/env bash
# A corrupt precompiled request worker must be rebuilt, not turn a transport
# failover into a Python "bad magic number" failure.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-local-mind"
td="$(mktemp -d)"
trap 'kill "${pid:-}" 2>/dev/null || true; rm -rf "$td"' EXIT

python3 - "$td/requests" >"$td/port" 2>/dev/null <<'PY' &
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

requests = sys.argv[1]
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
        self.wfile.write(b'{"models":[{"name":"stub:1b"}]}')
    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        with open(requests, 'ab') as f: f.write(body + b'\n')
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
        self.wfile.write(b'{"response":"stub-ok"}')
    def log_message(self, *_): pass

server = HTTPServer(('127.0.0.1', 0), Handler)
print(server.server_address[1], flush=True)
server.serve_forever()
PY
pid=$!
for _ in $(seq 1 50); do [[ -s "$td/port" ]] && break; sleep 0.1; done
port="$(<"$td/port")"
[[ -n "$port" ]] || { echo 'test-mesh-local-mind-jit: FAIL (stub did not start)' >&2; exit 1; }

run() {
    MESH_LOCAL_MIND_JIT_CACHE="$td/jit" OLLAMA_URL="http://127.0.0.1:$port" \
        "$tool" --model stub:1b ping
}

[[ "$(run)" == stub-ok ]] || { echo 'test-mesh-local-mind-jit: FAIL (initial worker request)' >&2; exit 1; }
pyc="$(find "$td/jit" -name '*.pyc' -type f -print -quit)"
[[ -s "$pyc" ]] || { echo 'test-mesh-local-mind-jit: FAIL (initial compilation missing)' >&2; exit 1; }
before="$(sha256sum "$pyc")"
[[ "$(run)" == stub-ok ]] || { echo 'test-mesh-local-mind-jit: FAIL (cached worker request)' >&2; exit 1; }
[[ "$(sha256sum "$pyc")" == "$before" ]] || {
    echo 'test-mesh-local-mind-jit: FAIL (valid worker cache was needlessly recompiled)' >&2
    exit 1
}
printf 'not-python-bytecode' >"$pyc"

[[ "$(run)" == stub-ok ]] || { echo 'test-mesh-local-mind-jit: FAIL (corrupt worker cache was not rebuilt)' >&2; exit 1; }
python3 - "$pyc" <<'PY'
import importlib.util
import pathlib
import sys

# Keep the interpreter magic header but make the marshalled code invalid.  A magic-only
# cache check must reject this before the recovery request tries to load it.
path = pathlib.Path(sys.argv[1])
path.write_bytes(importlib.util.MAGIC_NUMBER + b'\0' * 32)
PY
[[ "$(run)" == stub-ok ]] || { echo 'test-mesh-local-mind-jit: FAIL (malformed worker cache was not rebuilt)' >&2; exit 1; }
python3 - "$pyc" <<'PY'
import importlib.util
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
assert path.read_bytes()[:4] == importlib.util.MAGIC_NUMBER, 'cache was not replaced with this interpreter bytecode'
PY
printf '%s\n' 'test-mesh-local-mind-jit: PASS (corrupt compiled worker rebuilt before inference)'
