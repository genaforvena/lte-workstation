# GL-MT3000 actuator audit — 2026-09-13

Audit window: 2026-09-13 16:44–16:54 UTC. The task was open when checked and was claimed by
`health@mesh-home` at 16:44:30Z. No router configuration was changed.

## Result

I found no scheduled mesh command that writes GL-MT3000 Wi-Fi settings, changes its power, or
directly changes its WAN configuration. One enabled boot service on `mesh-home` does change that
host's firewall and may influence the router's WireGuard/WAN path indirectly. Two recurring
network healers can change only `mesh-home`'s own routes or wireless NIC; their current evidence
shows they stood down. The router itself is presently unreachable, so its own scheduler and runtime
state could not be inspected.

## Live schedule and actuator findings

- `mesh-router-phaedra-relay.service` is enabled and active (oneshot, `RemainAfterExit=yes`). Its
  last `ExecStart` completed successfully at **2026-09-13 11:36:04Z**; the journal records
  `relay up`. On start, `/home/mesh-home/.mesh/relay-router-phaedra.sh` adds local `iptables`
  DNAT/MASQUERADE/FORWARD rules for UDP 51820 received on `wlxbcec43434a22`, forwarding to
  `phaedra` `100.94.116.17:51820`. `ExecStop` runs the script's `down` action and deletes those
  tagged rules. This is a mesh-home packet relay for the router's WireGuard handshake, not a
  command to the GL-MT3000; it is the one mesh-owned actuator found that could indirectly affect
  the router's VPN/WAN path. The configured interface is absent from mesh-home's current `ip -br
  link` output (only `enp42s0`, `tailscale0`, and `docker0` appear). The last prior stop in the
  journal was **2026-09-12 07:13:40Z**, followed by a start at **08:42:44Z**; no stop has occurred
  since the current 11:36:04Z start.
- `mesh-link-heal` is scheduled on mesh-home every minute; latest cron launch observed:
  **2026-09-13 16:54:01Z**. Its code can reassociate or bounce a local wireless interface and
  reload local `rtw88` modules. The latest run log says “no wireless station to tend” and
  “0 radio(s) present”; live interfaces show no wireless NIC and the default route is through wired
  `enp42s0`. This is a local-client actuator, not a router actuator, and it did not act in the
  observed runs.
- `mesh-exit-node-lan-heal` is scheduled on mesh-home every minute; latest launch observed:
  **2026-09-13 16:54:01Z**. It can add a `throw` route in local policy table 52 when the exit node
  swallows a LAN route. Its application tape through **16:54:03Z** shows only `REFUSED`: candidate
  networks `100.74.0.0/16` and `100.76.0.0/16` fail its RFC1918 guard. This writes only the local
  host route table and no route was applied in the observed interval.
- `mesh-router-watch` is scheduled every 15 minutes on both mesh-home and phaedra. Latest launches
  are **16:45:01Z** on each host (phaedra journal: 16:45:01.748Z). The source's remote SSH command
  only reads `/sys/class/thermal/thermal_zone0/temp` and `/proc/loadavg`; it does not write router
  state ([source](../scripts/mesh-router-watch#L293)). Phaedra's latest log says the router probe
  path is down while its separate LAN gateway `38.49.216.129` is alive. Mesh-home's current default
  gateway is `100.76.0.1`, also distinct from the household router.
- `mesh-powerbtn` runs every five minutes on mesh-home and phaedra; latest launches were
  **16:50:01Z** on each. Its code reads kernel wakeup-source event counters for physical button
  presses; it has no shutdown, suspend, or reboot call. `mesh-wifi-rf` on mesh-home last launched at
  **16:51:01Z** and logged no associated wireless interface. `mesh-wifi-link` is also scheduled
  every five minutes on mesh-home, but its log reports the phone/SSH sensor unavailable; it does
  not target the router.
- Phaedra's live root crontab also schedules the Wi-Fi attribution/cross-validation/MIMO sensors and
  `mesh-imac-wifi`; its observed router-watch and power-button launches are timestamped above.
  Phaedra's service inventory had no router/Wi-Fi/WAN actuator service. The online iMac has a
  `mesh.ilya-link` launch agent every 60 seconds that only reconnects its own tmux session over
  SSH; its `mesh.socks`/`mesh.tailscaled` agents are local proxies. They do not configure the
  household AP/router.

The active systemd timers on mesh-home and phaedra contained no Wi-Fi/router/WAN/power-control
timer. Mesh-home has no root crontab. The scheduled-job scans and repository search found no
`uci`/`ubus`, router-side `wifi`/`reboot`, or mutating SSH command targeting the GL-MT3000; the sole
router SSH path found is the read-only thermal/load watcher described above.

## Access and limits

Tailscale currently reports `GL-MT3000` (`100.105.241.84`) offline. `mesh-peer-addr router`
reports both that address and LAN `192.168.8.1` silent and returns the Tailscale address only as a
guess. Thus no router-side logs or scheduler could be read from this node. The online mesh-home
and phaedra probes use different gateways from `192.168.8.1`; those read-only probe failures are
not evidence that a mesh command changed the household router. Router-authorized read-only
inspection remains for the chain's `root-cause-access` step.

Evidence sources: live crontabs and cron journal on mesh-home/phaedra; current systemd timer/unit
state and relay service journal on mesh-home; current `tailscale status`, link/route state, and
the `~/.mesh/{router-watch,link-heal.cron,exit-node-lan-heal,exit-node-lan-heal-applications}.log*`
ledgers; current iMac launch-agent plist and script; repository sources cited above.
