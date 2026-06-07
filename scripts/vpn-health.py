#!/usr/bin/env python3
"""VPN health watchdog — SCOPED model.

The host egresses CLEAN by design; only forwarded exit-node clients use the VPN.
So "VPN healthy" is tested ON THE TUNNEL (fresh handshake + traffic forwards through
Gtcld), NOT via the host's public IP. On failure it re-applies the SCOPED config
(Table=off + MESH_VPN chain), which keeps the host control plane on the clean route.

Run as root so its wg-quick/wg calls work without a tty:
    sudo nohup python3 ~/.mesh/vpn-health.py >> ~/.mesh/vpn-health.log 2>&1 &
"""
import subprocess, time, os

CONFIG = "/etc/wireguard/Gtcld.conf"   # scoped (Table=off + MESH_VPN chain)
IFACE = "Gtcld"
LOG = "/home/imozerov/.mesh/vpn-health.log"
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
    log("Starting VPN health watchdog (scoped model, tunnel-direct check)")
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
