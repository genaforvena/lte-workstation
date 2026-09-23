#!/usr/bin/env bash
# Regression test for `mesh-devto-publish --list --dupes`.
#
# The front page is the only surface a reader can land on, so the duplicate guard must
# measure LIVE articles. The first implementation pooled /published and /unpublished,
# which made its exit-0 "clean" verdict unreachable: the 2026-09-23 cleanup deliberately
# kept the 11 superseded copies as DRAFTS (dev.to has no merge API, so their URLs had to
# stay recoverable), and pooled counting reported those retained drafts as standing
# duplicates forever. A verdict a script can never render is not a verdict.
#
# The two fixtures differ ONLY in whether the second byte-identical copy is LIVE or DRAFT,
# which is exactly the distinction the guard exists to draw. The dev.to API is stubbed by a
# local HTTP server, so the test needs no network, no real account, and no real key.

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL="${MESHDUPE_TOOL:-$HERE/../scripts/mesh-devto-publish}"

PORT="$((38000 + RANDOM % 2000))"
PID=""
cleanup(){ [ -n "$PID" ] && kill "$PID" 2>/dev/null; }
trap cleanup EXIT

fails=0
pass(){ echo "PASS  $*"; }
fail(){ echo "FAIL  $*"; fails=$((fails+1)); }
check_rc(){ # <desc> <want> <got>
  if [ "$2" = "$3" ]; then pass "$1 (rc=$3)"; else fail "$1 (want rc=$2, got rc=$3)"; fi
}

TITLE="A Failed Voice Path Should Change the Next Call"
BODY="same body"

live_only(){      # second copy is NOT present at all
  printf '[{"id":4633089,"title":"%s","body_markdown":"%s","published_at":"2026-09-11T14:19:30.741Z","comments_count":3,"url":"https://dev.to/canonical","published":true,"slug":"canonical"}]' \
    "$TITLE" "$BODY"
}
live_with_dupe(){ # second copy IS live — the accident the guard exists to catch
  printf '[{"id":4633089,"title":"%s","body_markdown":"%s","published_at":"2026-09-11T14:19:30.741Z","comments_count":3,"url":"https://dev.to/canonical","published":true,"slug":"canonical"},{"id":4610677,"title":"%s","body_markdown":"%s","published_at":"2026-09-09T03:05:30.046Z","comments_count":2,"url":"https://dev.to/dupe","published":true,"slug":"dupe"}]' \
    "$TITLE" "$BODY" "$TITLE" "$BODY"
}
# NOTE the last record carries published:false — this fixture is the /unpublished index, and
# the client reads the INDEX, not the per-record flag; keeping them consistent means the
# fixture cannot accidentally inflate the LIVE count.
draft_retained(){ # canonical live, second copy retained as a draft (2026-09-23 cleanup shape)
  printf '[{"id":4610677,"title":"%s","body_markdown":"%s","published_at":"2026-09-09T03:05:30.046Z","comments_count":2,"url":"https://dev.to/retained","published":false,"slug":"retained"}]' \
    "$TITLE" "$BODY"
}

# A small threaded HTTP stub standing in for the dev.to API. Written in Python because a bash
# read loop is fragile under the rapid connect/close this tool does: it exits with the first
# client and leaves the port refusing connections.
STUB_PY="$HERE/.devto-stub.py"
cat > "$STUB_PY" <<'PYEOF'
import http.server, json, os, sys

PUB = json.loads(os.environ["STUB_PUB"])
UNPUB = json.loads(os.environ["STUB_UNPUB"])

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/published"):
            body = PUB
        elif self.path.endswith("/unpublished"):
            body = UNPUB
        else:
            body = []
        raw = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
PYEOF

# start_stub <published-json> <unpublished-json>
start_stub(){
  STUB_PUB="$1" STUB_UNPUB="$2" python3 "$STUB_PY" "$PORT" 2>/dev/null & PID=$!
  # wait for the port to accept a connection instead of racing a fixed sleep
  for _ in $(seq 1 100); do
    nc -z 127.0.0.1 "$PORT" 2>/dev/null && return 0
    sleep 0.05
  done
  return 1
}
stop_stub(){ [ -n "${PID:-}" ] && kill "$PID" 2>/dev/null; wait "$PID" 2>/dev/null; PID=""; }

ENVF="$HERE/.fake-devto.env"
printf 'DEVTO_API_KEY=stub-key-for-test-only\n' > "$ENVF"
export MESH_DEVTO_API="http://127.0.0.1:$PORT"

run_dupes(){ MESH_DEVTO_ENV="$ENVF" bash "$TOOL" --list --dupes "$@" 2>&1; }

# --- case 1: clean front page, retained draft only ------------------------
if ! start_stub "$(live_only)" "$(draft_retained)"; then fail "stub server did not come up"; fi
out="$(run_dupes)"; rc=$?
check_rc "default --dupes reports clean when the second copy is only a draft" 0 "$rc"
echo "  $out"
stop_stub; sleep 0.2

# --- case 2: a genuine second LIVE copy ------------------------------------
if ! start_stub "$(live_with_dupe)" '[]'; then fail "stub server did not come up"; fi
out="$(run_dupes)"; rc=$?
check_rc "default --dupes flags a second LIVE copy" 1 "$rc"
if printf '%s' "$out" | grep -q 'id=4610677'; then
  pass "names the offending live copy"
else
  fail "names the offending live copy"; echo "$out"
fi
stop_stub; sleep 0.2

# --- case 3: --all still audits the retention -----------------------------
if ! start_stub "$(live_only)" "$(draft_retained)"; then fail "stub server did not come up"; fi
out="$(run_dupes --all)"; rc=$?
check_rc "--all flags a retained draft as account-wide duplication" 1 "$rc"
if printf '%s' "$out" | grep -q '2 identical copies'; then
  pass "--all groups the canonical + retained pair"
else
  fail "--all groups the canonical + retained pair"; echo "$out"
fi
stop_stub

rm -f "$ENVF" "$STUB_PY"
echo "-----------------------------"
if [ "$fails" = 0 ]; then echo "ALL PASS"; exit 0; fi
echo "$fails FAILURES"; exit 1
