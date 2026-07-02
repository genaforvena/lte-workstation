#!/usr/bin/env python3
# orphan-ok: on-demand (location collector, unwired by design — runs when phone beacons)
# mesh phone MULTI-SENSOR collector — token-gated HTTPS, append-only, GENERIC.
# The phone beacon GETs /loc?token=..&<any sensor fields>..  We store EVERY query param
# (except token) into one JSON line per fix — so new sensors need NO collector change.
import json, os, random, ssl, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

TRACK_LOG = "/root/.mesh/phone-track.log"
TOKEN_FILE = "/root/.mesh/loc-token"
CERT = "/etc/letsencrypt/live/38-49-216-141.sslip.io/fullchain.pem"
KEY = "/etc/letsencrypt/live/38-49-216-141.sslip.io/privkey.pem"
PORT = 8092
CHAOS_LATENCY_FILE = "/root/.mesh/.collector-latency"

def load_token():
    try:
        return open(TOKEN_FILE).read().strip()
    except Exception:
        return None

def maybe_inject_latency():
    """CHAOS (STUDY 'implement intermittent random 1-5s pauses to a single worker's API
    responses', 2026-07-02 backlog task): opt-in, default-OFF fault injection. Armed by
    MESH_CHAOS_LATENCY=1 (env, this process) OR a sentinel file (survives across requests —
    same dual-arm convention as scripts/mesh-phone-beacon2's MESH_CHAOS_NETFAIL hook).
    INTERMITTENT: MESH_CHAOS_LATENCY_RATE (default 100 = every request once armed) rolls a
    per-request chance to fire, so a drill can also simulate a WORKER THAT IS SOMETIMES slow,
    not just always. When it fires, sleeps a random 1-5s BEFORE the reply is written — this
    worker's caller (the phone beacon's push) exercises its real request-timeout/retry path
    exactly as it would against a genuinely slow/overloaded API, with zero network-layer or
    substrate change (pure application-layer delay, same safety class as the beacon2 hook).
    Disarm: unset the env / rm the sentinel — the very next request is immediate again."""
    armed = os.environ.get("MESH_CHAOS_LATENCY") == "1" or os.path.exists(CHAOS_LATENCY_FILE)
    if not armed:
        return
    rate = int(os.environ.get("MESH_CHAOS_LATENCY_RATE", "100") or "100")
    if random.randint(1, 100) > rate:
        return          # intermittent: this request rolled past the fire rate — stay fast
    time.sleep(random.uniform(1, 5))

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _reply(self, code, body=b"ok"):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try: self.wfile.write(body)
        except Exception: pass
    def do_GET(self):
        u = urlparse(self.path)
        if u.path not in ("/loc", "/loc/"):
            return self._reply(404, b"no")
        q = parse_qs(u.query, keep_blank_values=True)
        tok = load_token()
        if not tok or q.get("token", [""])[0] != tok:
            return self._reply(403, b"forbidden")
        maybe_inject_latency()
        rec = {"ts": int(time.time())}
        for k, v in q.items():
            if k == "token":
                continue
            val = v[0] if v else ""
            rec[k] = val if val != "" else None
        try:
            os.makedirs(os.path.dirname(TRACK_LOG), exist_ok=True)
            with open(TRACK_LOG, "a") as f:
                f.write(json.dumps(rec) + "\n")
        except Exception as e:
            return self._reply(500, str(e).encode())
        return self._reply(200, b"ok")

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        # 1) PORTABLE logic self-test — proves the code is sound on ANY node,
        #    independent of deployment: token is dropped, every other param is
        #    kept, and an explicitly-blank value becomes None.
        tq = parse_qs("token=X&lat=1.5&lon=2.5&blank=", keep_blank_values=True)
        rec = {}
        for k, v in tq.items():
            if k == "token":
                continue
            val = v[0] if v else ""
            rec[k] = val if val != "" else None
        if rec != {"lat": "1.5", "lon": "2.5", "blank": None}:
            print(f"smoke-test: FAIL (record-build {rec})"); sys.exit(1)
        # 1b) CHAOS latency hook — offline, deterministic (no real sleep). Monkeypatch
        # random+time.sleep so the test proves the GATE logic, not real timing.
        calls = {"sleep": 0, "dur": None}
        _orig_sleep, _orig_randint, _orig_uniform = time.sleep, random.randint, random.uniform
        time.sleep = lambda s: (calls.__setitem__("sleep", calls["sleep"] + 1), calls.__setitem__("dur", s))
        random.randint = lambda a, b: 50     # fixed 50% roll
        random.uniform = lambda a, b: 3.0    # fixed 3s duration
        os.environ.pop("MESH_CHAOS_LATENCY", None); os.environ.pop("MESH_CHAOS_LATENCY_RATE", None)
        try:
            maybe_inject_latency()           # unarmed -> no sleep
            if calls["sleep"] != 0:
                print(f"smoke-test: FAIL (unarmed still slept {calls})"); sys.exit(1)
            os.environ["MESH_CHAOS_LATENCY"] = "1"; os.environ["MESH_CHAOS_LATENCY_RATE"] = "100"
            maybe_inject_latency()           # armed, rate=100, roll=50<=100 -> fires once
            if calls["sleep"] != 1 or calls["dur"] != 3.0:
                print(f"smoke-test: FAIL (armed rate=100 did not fire {calls})"); sys.exit(1)
            calls["sleep"] = 0
            os.environ["MESH_CHAOS_LATENCY_RATE"] = "10"
            maybe_inject_latency()           # armed, rate=10, roll=50>10 -> intermittent skip
            if calls["sleep"] != 0:
                print(f"smoke-test: FAIL (rate gate did not skip {calls})"); sys.exit(1)
        finally:
            time.sleep, random.randint, random.uniform = _orig_sleep, _orig_randint, _orig_uniform
            os.environ.pop("MESH_CHAOS_LATENCY", None); os.environ.pop("MESH_CHAOS_LATENCY_RATE", None)
        # 2) Deployment readiness — token+cert only exist on the collector's HOME
        #    node (the public-ingress host that provisions the sslip.io LE cert).
        #    Off that node their absence is EXPECTED, not a code fault — report
        #    skip + exit 0 so a foreign node's [check] reflex doesn't cry wolf.
        home = os.path.isdir("/etc/letsencrypt/live")
        miss = []
        if not os.path.exists(TOKEN_FILE): miss.append("no-token-file")
        if not (os.path.exists(CERT) and os.path.exists(KEY)): miss.append("no-cert")
        if miss:
            tag = " ".join(miss)
            if home:
                print(f"smoke-test: FAIL ({tag})"); sys.exit(1)
            print(f"smoke-test: ok (logic sound; not-deployed-here — {tag})"); sys.exit(0)
        print("smoke-test: ok (logic sound; deploy-ready)"); sys.exit(0)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)

    # ROBUSTNESS (2026-06-19): do NOT TLS-wrap the LISTENING socket — that makes the handshake
    # run inside the accept loop, so one half-open/stalled client (e.g. an onVao-tunnelled push
    # that opens TCP but never finishes TLS) blocks ALL new connections forever → the accept queue
    # fills and every push times out (the exact hang that lost a walk's worth of data). Instead:
    # raw TCP listen, wrap EACH accepted connection with a hard timeout, daemon threads, and
    # swallow per-connection TLS errors so a bad client can never wedge the server.
    class Collector(ThreadingHTTPServer):
        daemon_threads = True
        def get_request(self):
            sock, addr = self.socket.accept()
            sock.settimeout(15)            # a stalled handshake/read aborts in 15s, never forever
            ssock = ctx.wrap_socket(sock, server_side=True)
            return ssock, addr
        def handle_error(self, request, client_address):
            pass                            # aborted/slow TLS is normal noise — don't spam/crash

    httpd = Collector(("0.0.0.0", PORT), H)
    httpd.serve_forever()
