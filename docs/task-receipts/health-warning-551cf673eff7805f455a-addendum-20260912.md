# Addendum: route-table clarification for `health-warning/551cf673eff7805f455a`

The original receipt said the pane's `tailscale0` egress label conflicted with the local default
route via `enp42s0`. A later targeted route lookup shows that inference was too broad:

```
ip route get 100.76.0.1
100.76.0.1 dev tailscale0 table 52 src 100.81.222.19
```

`ip rule` includes a priority-5270 lookup of table 52 before the main table. The physical default
route therefore does not establish a contradiction with the Tailscale route used for the mesh
gateway. Keep the exit-node/SPOF and LAN-UNKNOWN findings; withdraw the claimed egress/route
discrepancy unless a target-specific probe shows one. No route or VPN setting was changed.
