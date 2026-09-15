# Health warning triage: imac-rozalia SSH authentication

Task: `health-warning/347d70b4b3f9fd0e738e/triage`  
Source: `watchdog@mesh-home`, `2026-09-13T12:59:30Z`, signature `9f83297aad2c`.

The warning was caused by the local health probe selecting the wrong SSH account, not by loss of
the iMac or rejection of its documented mesh identity. `mesh-health` uses the account in
`~/.mesh/nodes` for each IP and otherwise falls back to the local username (`mesh-home`). The
registry had the Mac's LAN address (`mac:ilya@192.168.8.214`) but no tailnet entry for
`100.121.88.110`.

Evidence and correction at `2026-09-13T13:03Z`:

- `tailscale status` showed `imac-rozalia` active/direct at `100.121.88.110`.
- `tailscale ping --c 2 100.121.88.110` returned a pong in 4 ms.
- SSH as the documented user, `ilya@100.121.88.110`, completed `true` successfully with
  `BatchMode=yes` and public-key authentication only.
- Before correction, `mesh-health` rendered `SKIP ... SSH authentication refused`; its account
  selector falls back to `whoami` when the IP is absent from `MESH_NODES`.
- Added `imac-rozalia:ilya@100.121.88.110` to the node-local `MESH_NODES` registry.
- After correction, `mesh-health` rendered `PASS imac-rozalia 100.121.88.110`; other offline fleet
  rows remain unchanged. `mesh-health --test` passed its SSH classifier and parser checks.

No routing, DNS, firewall, VPN, or other network substrate was changed. The warning was valid for
the misconfigured probe at emission time; the underlying iMac SSH path works with its documented
identity.
