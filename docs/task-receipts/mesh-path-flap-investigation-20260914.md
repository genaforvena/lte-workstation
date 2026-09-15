# imac-rozalia path-flap investigation — 2026-09-14

Task: `mesh-path-flap-investigation-20260914/diagnose-imac-rozalia-path-flap`
Owner: genome

## Finding

The repeated direct↔relay changes are real changes in the local Tailscale status
snapshots, not duplicate alert text. `scripts/mesh-path-watch` classifies an
online peer as direct when `CurAddr` is non-empty and relay when it is empty;
it writes an edge only when that observed mode changes. Its five-minute cadence
means these records establish changes between sampled snapshots, not continuous
packet loss or the exact instant the path changed.

The retained `/home/mesh-home/.mesh/path-watch.log` records imac-rozalia
alternating at ten-minute intervals through the original 11:09–15:09Z window
and continuing later: 15:49 direct, 15:59 relay, 16:09 direct, 16:19 relay,
16:29 direct, 16:39 relay, 16:49 direct, 16:59 relay, and 17:09 direct
(lines 4092–4102). Netweather samples at 11:54, 12:54, 13:54, 14:54, 15:54,
and 16:54Z all report `udp=true`; these hourly samples do not coincide with
every transition and cannot establish the remote peer's NAT or radio cause.

Fresh reads on 2026-09-14:

- `mesh-path-watch --status` at 17:09:01Z: `OK`, 8 peers, 2 direct, 0 relay,
  6 offline; imac-rozalia was direct.
- `tailscale ping --c 3 imac-rozalia` at about 17:10Z: pong via
  `5.227.24.249:42772` in 4 ms (direct).
- `tailscale netcheck` at 17:10:01Z: UDP true, IPv4 available, nearest DERP
  Helsinki at 34.3 ms.
- `tailscale status` independently listed imac-rozalia active on that same
  direct endpoint.

These fresh observations show the peer recovered to a working direct path.
They do not explain why its sampled path keeps changing, and hourly healthy
UDP checks do not rule out peer-side or time-local network variation. The log
therefore supports genuine path churn, but not a demonstrated service outage
or a specific local routing/VPN/firewall fault.

## Safe disposition and retry condition

No routing, DNS, firewall, VPN, or Tailscale setting was changed. Continue
passive monitoring. Reopen diagnosis if either (a) two consecutive five-minute
path-watch snapshots show imac-rozalia relayed or offline, or (b) a direct
`tailscale ping imac-rozalia` fails. At that time collect the status snapshot,
ping result, and `tailscale netcheck` together with timestamps. If transitions
continue while ping succeeds and UDP remains true, request same-time Tailscale
path evidence from imac-rozalia before assigning cause or proposing a substrate
change.
