# Health warning triage: `imac-rozalia` unreachable

Task: `health-warning/2ca0e1c7ec6377531951/triage`

The watchdog report at 08:33:57Z says `imac-rozalia` (`100.121.88.110`) is unreachable,
with no configured off-tailnet fallback. I inspected repository context, the task ledger, and
current mesh state before deciding whether any local recovery is safe.

Fresh evidence, 08:36–08:38Z:

- `mesh-dash --once check` reports the peer unreachable and warns that high local load makes
  reachability probes unreliable.
- `tailscale status --json` reports `Online=false`, `Active=true`, `CurAddr=""`,
  `LastSeen=2026-09-14T08:17:22.1Z`, and no successful handshake for this Mac.
- The one SSH check to `imac-rozalia` timed out. The dashboard's probe warning and local load
  averages of 24.49/43.33/36.93 on 16 cores mean that timeout is corroborating evidence, not a
  diagnosis of the Mac's power or root cause.
- `~/.mesh/nodes` configures LAN fallback only for `GL-MT3000` and `router`; there is none for
  `imac-rozalia`.
- The ledger already contains the same unresolved reachability obligation,
  `health-warning/0ac2476a343fdde6c790/triage`, blocked on a reachable owner/path with retry
  `event:roll-call-delta`, plus prior attempts for the same fault. The current live state still
  shows no alternate path and no new roll-call event.

Disposition: the reachability fault remains active; the Mac's physical state and cause remain
unknown. There is no safe mesh-home correction while the Mac is offline and has no LAN fallback.
Keep this warning queued/typed-blocked on the exact missing prerequisite: a reachable owner/path
to the Mac or an independently available LAN path. Retry on `event:roll-call-delta`. No routing,
DNS, firewall, VPN, Tailscale, or remote-node state was changed.

Verification: `mesh-dash --once check`; `tailscale status --json` filtered to the peer;
`ssh -o BatchMode=yes -o ConnectTimeout=5 imac-rozalia 'hostname; uptime'` (timed out);
`mesh-task status health-warning/0ac2476a343fdde6c790`; `~/.mesh/nodes`; and `uptime`.
