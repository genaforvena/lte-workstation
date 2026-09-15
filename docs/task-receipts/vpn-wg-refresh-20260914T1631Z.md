# VPN WireGuard freshness refresh — 2026-09-14

Task: `vpn-wg-refresh-20260914T1631Z/refresh-current-wg-freshness`.

## Finding

The pane's 16:30Z DEGRADED verdict is still localized to WireGuard peer freshness. At 16:34:41Z, `wg-quick@wg0` was active with 16 peers: 0 handshakes under one hour, 0 between one and 24 hours, 12 older than 24 hours, and 4 never-handshaken. The newest handshake was 1,330,026 seconds old. That agrees with the pane's 16:30:14Z row (0 active / 0 idle / 12 stale / 4 never; newest age 1,329,755s) within elapsed wall time. The end-to-end port-8444 probe passed at 16:29Z. This shows peer inactivity, not a demonstrated client-side failure. No VPN service, peer, route, or configuration state was changed.

## Ordered evidence

- `2026-09-14T16:31:16Z` — `mesh-dash --once vpn` exited 0 and rendered the complete unfiltered state stream. It showed Phaedra's VPN DEGRADED because no WG client handshake had occurred in over 24h; SS, Trojan, and WG services were up; port 8444 passed with egress `38.49.216.141`; the WG roster was 16 peers, 0 active / 0 idle / 12 stale / 4 never, newest handshake age 1,329,755s.
- `2026-09-14T16:34:18Z` — local transport preflight completed before the remote read:

  ```text
  timeout 15 tailscale status --json | jq -r '"backend=\(.BackendState // "na") self_online=\(.Self.Online // false) self_ip=\(.Self.TailscaleIPs[0] // "na") phaedra_online=\([.Peer[]? | select(.HostName == "phaedra") | .Online][0] // false) phaedra_ip=\([.Peer[]? | select(.HostName == "phaedra") | .TailscaleIPs[0]][0] // "missing")"'
  backend=Running self_online=true self_ip=100.81.222.19 phaedra_online=true phaedra_ip=100.94.116.17
  systemctl is-active tailscaled
  active
  awk '{print $1}' /proc/uptime
  104318.17
  curl -fsS --max-time 8 https://api.ipify.org
  38.49.216.141
  ```

- `2026-09-14T16:34:41Z` — after preflight passed, this read-only command ran on Phaedra. Its Python aggregator emitted only service state, peer count, age buckets, and newest age; no public keys were retained or printed:

  ```sh
  ssh -o BatchMode=yes -o ConnectTimeout=8 phaedra "python3 -c 'import subprocess,time,datetime; now=int(time.time()); print(\"remote_utc=\"+datetime.datetime.now(datetime.timezone.utc).strftime(\"%Y-%m-%dT%H:%M:%SZ\")); s=subprocess.run([\"systemctl\",\"is-active\",\"wg-quick@wg0\"],capture_output=True,text=True); print(\"wg_service=\"+s.stdout.strip()); lines=subprocess.run([\"wg\",\"show\",\"wg0\",\"latest-handshakes\"],capture_output=True,text=True,check=True).stdout.splitlines(); stamps=[int(line.split()[-1]) for line in lines if len(line.split())>=2]; ages=[now-stamp for stamp in stamps if stamp>0]; never=sum(stamp==0 for stamp in stamps); print(\"peers=%d fresh_lt1h=%d idle_1h_24h=%d stale_gt24h=%d never=%d newest_age_s=%s\"%(len(stamps),sum(age<3600 for age in ages),sum(3600<=age<=86400 for age in ages),sum(age>86400 for age in ages),never,min(ages) if ages else \"none\"))'"
  ```

  ```text
  remote_utc=2026-09-14T16:34:41Z
  wg_service=active
  peers=16 fresh_lt1h=0 idle_1h_24h=0 stale_gt24h=12 never=4 newest_age_s=1330026
  ```

## Disposition

The peer-freshness condition persists and the current age tracks elapsed time since the prior check. With no active or idle clients reported and no client attempt evidence, client demand or failure remains unknown. There is no demonstrated service fault or safe one-line repair to apply. Keep diagnosis read-only; do not restart WG or edit peers/routes based on inactivity alone.
