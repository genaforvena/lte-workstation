#!/usr/bin/env python3
"""VPN health watchdog — SCOPED model.

The host egresses CLEAN by design; only forwarded exit-node clients use the VPN.
So "VPN healthy" is tested ON THE TUNNEL (fresh handshake + traffic forwards through
the VPN iface), NOT via the host's public IP. On failure it re-applies the SCOPED config
(Table=off + MESH_VPN chain), which keeps the host control plane on the clean route.

Run as root so its wg-quick/wg calls work without a tty:
    sudo nohup python3 ~/.mesh/vpn-health.py >> ~/.mesh/vpn-health.log 2>&1 &
"""
import subprocess, time, os, glob, sys, shutil

# Interface/config are node-local — never hardcoded in the genome. Resolve from the
# environment (VPN_EGRESS_IFACE), else from the single scoped config in /etc/wireguard.
def _resolve_iface():
    env = os.environ.get("VPN_EGRESS_IFACE")
    if env:
        return env
    confs = glob.glob("/etc/wireguard/*.conf")
    return os.path.splitext(os.path.basename(confs[0]))[0] if len(confs) == 1 else ""

if len(sys.argv) > 1 and sys.argv[1] == '--test':
    if not shutil.which('wg'):
        print("smoke-test: FAIL (wg not found)"); sys.exit(1)
    iface = _resolve_iface()
    config = os.environ.get("VPN_EGRESS_CONF") or (f"/etc/wireguard/{iface}.conf" if iface else "")
    if not iface or not config:
        print("smoke-test: n/a (no VPN configured on this node)"); sys.exit(2)
    if not os.path.isfile(config):
        print(f"smoke-test: FAIL (config missing: {config})"); sys.exit(1)
    try:
        hs = subprocess.run(["wg", "show", iface, "latest-handshakes"],
                            capture_output=True, text=True, timeout=5)
        if hs.returncode != 0:
            print("smoke-test: ok (interface inactive)"); sys.exit(0)
        if not hs.stdout.strip():
            print("smoke-test: ok (tunnel idle)"); sys.exit(0)
        epochs = [int(p.split()[-1]) for p in hs.stdout.strip().splitlines() if p.split()]
        last = max(epochs) if epochs else 0
        age = int(time.time()) - last
        if last == 0 or age > 180:
            print(f"smoke-test: FAIL (stale handshake — {age}s)"); sys.exit(1)
        print("smoke-test: ok"); sys.exit(0)
    except FileNotFoundError:
        print("smoke-test: FAIL (wg not found)"); sys.exit(1)
    except Exception as e:
        print(f"smoke-test: FAIL (check error: {e})"); sys.exit(1)

IFACE = _resolve_iface()
CONFIG = os.environ.get("VPN_EGRESS_CONF") or (f"/etc/wireguard/{IFACE}.conf" if IFACE else "")
LOG = os.environ.get("VPN_HEALTH_LOG") or os.path.expanduser("~/.mesh/vpn-health.log")
CHECK_INTERVAL = 60
FAIL_THRESHOLD = 3
HANDSHAKE_MAX_AGE = 180   # seconds; healthy tunnel handshakes ~every 2 min

def log(msg):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = f"{ts}  {msg}"
    print(line)
    try:
        with open(LOG, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def check_vpn():
    """Healthy = tunnel up with a recent handshake AND traffic forwards through it."""
    try:
        hs = subprocess.run(["wg", "show", IFACE, "latest-handshakes"],
                            capture_output=True, text=True, timeout=5)
        if hs.returncode != 0 or not hs.stdout.strip():
            return False, "tunnel down (no handshake)"
        epochs = [int(p.split()[-1]) for p in hs.stdout.strip().splitlines() if p.split()]
        last = max(epochs) if epochs else 0
        age = int(time.time()) - last
        if last == 0 or age > HANDSHAKE_MAX_AGE:
            return False, f"stale handshake ({age}s)"
        # does traffic actually forward through the tunnel?
        p = subprocess.run(["ping", "-I", IFACE, "-c", "1", "-W", "3", "1.1.1.1"],
                          capture_output=True, timeout=8)
        if p.returncode != 0:
            return False, f"tunnel up (hs {age}s) but NOT forwarding (provider down?)"
        return True, f"ok (handshake {age}s, forwarding)"
    except Exception as e:
        return False, f"check error: {e}"

def bring_up():
    """Re-apply the SCOPED config. Host control plane stays on the clean route."""
    try:
        subprocess.run(["wg-quick", "down", CONFIG], capture_output=True, timeout=15)
        time.sleep(1)
        r = subprocess.run(["wg-quick", "up", CONFIG], capture_output=True, text=True, timeout=15)
        if r.returncode != 0:
            log(f"wg-quick up failed: {r.stderr.strip()[:200]}")
        return r.returncode == 0
    except Exception as e:
        log(f"ERROR bringing up VPN: {e}")
        return False

def main():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    if not IFACE or not CONFIG:
        log("not an egress-offering node (no VPN_EGRESS_IFACE / single /etc/wireguard conf) — exiting")
        return
    log(f"Starting VPN health watchdog (scoped model, tunnel-direct check) iface={IFACE}")
    fails = 0
    while True:
        ok, info = check_vpn()
        if ok:
            if fails:
                log(f"VPN OK again: {info}")
            fails = 0
        else:
            fails += 1
            log(f"VPN FAIL ({fails}/{FAIL_THRESHOLD}): {info}")
            if fails >= FAIL_THRESHOLD:
                log("attempting recovery — re-applying scoped config")
                if bring_up():
                    time.sleep(3)
                    ok, info = check_vpn()
                    log(f"VPN RECOVERED: {info}" if ok else f"STILL DOWN after recovery: {info}")
                    if ok:
                        fails = 0
                else:
                    log("recovery FAILED (wg-quick)")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
