#!/usr/bin/env python3
# mesh phone MULTI-SENSOR collector — token-gated HTTPS, append-only, GENERIC.
# The phone beacon GETs /loc?token=..&<any sensor fields>..  We store EVERY query param
# (except token) into one JSON line per fix — so new sensors need NO collector change.
import json, os, ssl, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

TRACK_LOG = "/root/.mesh/phone-track.log"
TOKEN_FILE = "/root/.mesh/loc-token"
CERT = "/etc/letsencrypt/live/38-49-216-141.sslip.io/fullchain.pem"
KEY = "/etc/letsencrypt/live/38-49-216-141.sslip.io/privkey.pem"
PORT = 8092

def load_token():
    try:
        return open(TOKEN_FILE).read().strip()
    except Exception:
        return None

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
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), H)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
