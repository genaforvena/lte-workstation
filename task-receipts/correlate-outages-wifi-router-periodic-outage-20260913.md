# Wi-Fi outage correlation — 2026-09-13

Task `wifi-router-periodic-outage-20260913/correlate-outages` was open in the live chain at
17:04Z and assigned to `health`; its instruction is consistent with the incident record and current
host/router topology. Claimed at 17:07Z. This is a bounded correlation of existing passive evidence;
no new Wi-Fi activity or router/host configuration changes were made.

## Incident timeline

Times are UTC. “Recovery” below means the first healthy sample after the reported interruption,
not a proven repair time.

| Report/window | Existing observation | Gap/recovery conclusion |
|---|---|---|
| 15:51:26–16:02:20 | Existing iMac watch: 649/649 replies from both `192.168.8.1` and `1.1.1.1`; no timeout. | No outage reproduced in this window. |
| About 16:11, operator reported another Wi-Fi interruption. | First follow-up at 16:11:55 found Wi-Fi associated to `GL-MT3000-765`; gateway and `1.1.1.1` each replied 5/5. The existing 16:12:33–16:15:04 watch recorded 75/75 for both, continuously associated. | Exact onset and recovery are unknown; path was healthy by 16:11:55 and remained healthy through 16:15:04. |
| About 16:26, operator clarified household-wide router internet loss. | At 16:26:15 the iMac had the GL SSID, gateway 4/4, public IP 4/4, and DNS resolution. | This was a healthy point sample after/around the report, not an outage boundary. No exact onset or recovery supplied. |
| 16:30:23–16:37:19 existing iMac watch; separate mesh reachability event at 16:33:37. | Parsed the retained watch artifact: 403 one-second samples, no inter-sample gap over 2 seconds; all show associated to `GL-MT3000-765`, gateway 0% loss, and `1.1.1.1` 0% loss. At 16:33:37, independent Tailscale ping/SSH checks from mesh nodes could not reach the iMac. | The mesh/Tailscale reachability gap is real, but the contemporaneous local Wi-Fi and public-IP samples stayed healthy through 16:37:19. It does not establish a household-router outage. Recovery time for Tailscale/SSH is not present in these artifacts. |

The incident note says the watch’s “last delivered sample” was 16:31:25 and that it was terminated before
16:37Z. The retained log itself contains samples through 16:37:19 (mtime 16:37:15Z); this receipt
reports the artifact’s contents and does not infer whether later lines were buffered or delivered live.

## Actuator correlation and path separation

- `mesh-router-phaedra-relay.service` is a **system** unit (not a user unit). Current read-only
  systemd/journal inspection confirms it is enabled and `active (exited)`, started successfully at
  11:36:04Z, with no later start/stop journal event through this check. Its script only installs
  mesh-home firewall forwarding for router WireGuard UDP/51820 traffic arriving on
  `wlxbcec43434a22`; it does not command router Wi-Fi, power, or WAN. That interface is absent from
  current `ip -br address`. The relay therefore has no execution-time match to the 16:11/16:26
  reports or the 16:33 reachability event. It remains an indirect VPN-path possibility that this
  evidence cannot rule out; no router-side event log is available to test it.
- The already-audited `mesh-link-heal` launch at 16:54:01Z reported no wireless station and zero
  radios; it acts on mesh-home only. `mesh-exit-node-lan-heal` at 16:54:01Z recorded `REFUSED` for
  `100.74.0.0/16` and `100.76.0.0/16`, applying no route. `mesh-router-watch` at 16:45:01Z is a
  read-only thermal/load probe, not a router actuator.
- mesh-home is on its distinct mobile/wired tether path: live address `100.76.218.30` on `enp42s0`,
  default gateway `100.76.0.1`, plus its own `tailscale0`. The household router is `192.168.8.1`
  observed from the iMac LAN. mesh-home’s continued egress therefore says nothing about household
  router availability.

## Result and next gate

No observed mesh actuator execution correlates with a roughly ten-minute household outage. The
available iMac samples do not reproduce the reported outage; one separate mesh-reachability gap is
not corroborated by gateway or public-IP loss. This is not evidence that the reports are false or
that the router is healthy: exact operator onset/recovery timestamps and router WAN/radio/system
logs are absent. GL-MT3000 router-admin access remains unavailable (Tailscale peer offline; prior
router SSH key rejected). The chain’s existing next step is
`wifi-router-periodic-outage-20260913/root-cause-access`; retry when operator-authenticated router
read-only access or an equivalent synchronized household-LAN vantage during a reported outage is
available. Do not infer cause or apply a repair from this correlation alone.

Evidence: `~/.mesh/wifi-incident-20260913.md`,
`~/.mesh/wifi-watch-20260913-155126-{gateway,internet}.log`,
`~/.mesh/wifi-watch-20260913-1612-followup.log`,
`~/.mesh/wifi-watch-20260913-1629-housewide-router.log`,
`task-receipts/audit-actuators-wifi-router-periodic-outage-20260913.md`, systemd status/journal for
`mesh-router-phaedra-relay.service`, live `ip -br address` and default route, and
`~/.mesh/{link-heal.cron.log,exit-node-lan-heal-applications.log,router-watch.log}`.
