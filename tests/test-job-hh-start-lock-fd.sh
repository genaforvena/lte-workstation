#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
port=$((20000 + $$ % 20000))
cleanup() {
  if [[ -n ${children:-} ]]; then
    kill $children 2>/dev/null || true
  fi
  rm -rf "$tmp"
}
trap cleanup EXIT

home="$tmp/home"
mkdir -p "$home/.local/bin" "$home/.mesh/job" "$home/.mesh/browser" \
  "$home/.venv-browser/bin" "$tmp/bin"

cat >"$home/.local/bin/mesh-pidfile.sh" <<'SH'
mesh_pidfile_alive() { return 1; }
mesh_pidfile_pid() { sed -n '1p' "$1"; }
mesh_pidfile_write() { printf '%s\n' "$2" >"$1"; }
SH

cat >"$home/.venv-browser/bin/python3" <<'PY'
#!/usr/bin/env python3
import os, sys, time
if sys.argv[1:2] == ["-c"]:
    raise SystemExit(0)
with open(os.path.expanduser("~/.mesh/job/test-drive.log"), "a") as f:
    f.write("[ready]\n")
    f.flush()
time.sleep(60)
PY
chmod +x "$home/.venv-browser/bin/python3"

cat >"$tmp/bin/mesh-vantage-socks" <<'PY'
#!/usr/bin/env python3
import socket, sys, time
port = int(sys.argv[sys.argv.index("--port") + 1])
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", port))
s.listen(1)
time.sleep(60)
PY
chmod +x "$tmp/bin/mesh-vantage-socks"

cat >"$tmp/bin/nohup" <<'SH'
#!/usr/bin/env bash
exec "$@"
SH
chmod +x "$tmp/bin/nohup"

export HOME="$home" PATH="$tmp/bin:$PATH" HH_PROFILE=test HH_VANTAGE_PORT="$port"
"$repo/scripts/mesh-hh-drive" --start
children=$(pgrep -f "$home/.venv-browser/bin/python3|mesh-vantage-socks --port $port" || true)
if ! flock -n "$home/.mesh/job/test-drive.start.lock" -c true; then
  echo "HH start lock remained held by a background child" >&2
  exit 1
fi
echo "HH start lock released after daemon launch: PASS"
