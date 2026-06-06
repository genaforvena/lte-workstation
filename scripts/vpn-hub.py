#!/usr/bin/env python3
"""vpn-hub.py — serve WireGuard mesh configs to joining nodes.
Run on the hub machine: python3 vpn-hub.py [port]
Nodes run node-join.sh and automatically get their VPN slot."""

import os, json, subprocess, sys, socket, shutil
from http.server import HTTPServer, BaseHTTPRequestHandler

WG_IFACE = "wg-mesh"
WG_DIR = "/etc/wireguard"
SUBNET = "10.9.0"
HUB_IP = f"{SUBNET}.1"
ENDPOINT = "100.125.157.75"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
DB_FILE = os.path.expanduser("~/.wg-mesh-nodes.json")
VERBOSE = os.environ.get("VPN_HUB_VERBOSE")

DB = {}  # hostname -> {ip, pubkey, privkey}

def save():
    with open(DB_FILE, "w") as f:
        json.dump(DB, f, indent=2)

def load():
    global DB
    try:
        with open(DB_FILE) as f:
            DB = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def shell(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def wg_set(*args):
    shell(f"wg set {WG_IFACE} {' '.join(args)}")

def next_ip():
    used = {info["ip"] for info in DB.values()}
    for i in range(2, 255):
        ip = f"{SUBNET}.{i}"
        if ip not in used:
            return ip
    return None

def gen_config(hostname):
    priv = shell("wg genkey").stdout.strip()
    pub = shell(f"echo '{priv}' | wg pubkey").stdout.strip()
    ip = next_ip()
    if not ip:
        return None, "no free IPs"

    if os.geteuid() == 0:
        wg_set("peer", pub, f"allowed-ips", f"{ip}/32")
    else:
        shell(f"sudo -A wg set {WG_IFACE} peer {pub} allowed-ips {ip}/32")

    DB[hostname] = {"ip": ip, "pubkey": pub, "privkey": priv}
    save()

    server_pub = shell(f"wg show {WG_IFACE} public-key").stdout.strip()

    return f"""[Interface]
PrivateKey = {priv}
Address = {ip}/32
DNS = 1.1.1.1
MTU = 1420

[Peer]
PublicKey = {server_pub}
AllowedIPs = {SUBNET}.0/24
Endpoint = {ENDPOINT}:51821
PersistentKeepalive = 20
""", None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip("/")
        if path == "nodes":
            self.respond(200, json.dumps(DB, indent=2))
        elif path:
            config, err = gen_config(path)
            if config:
                if VERBOSE:
                    print(f"[vpn-hub] + {path} -> {DB[path]['ip']}")
                self.respond(200, config)
            else:
                self.respond(503, err)
        else:
            self.respond(400, "usage: GET /<hostname>")

    def respond(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, f, *a):
        pass  # quiet

if __name__ == "__main__":
    load()
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[vpn-hub] {len(DB)} known nodes, listening on :{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
