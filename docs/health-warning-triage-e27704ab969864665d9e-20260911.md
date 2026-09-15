# Health warning triage: e27704ab969864665d9e

- Source event: `2026-09-10T21:21:17Z`, watchdog reported `imac-rozalia` unreachable and absent from the tailnet.
- Current verification: `tailscale status --json` at `2026-09-11T20:46:xxZ` reports `HostName=imac-rozalia`, `Online=true`, `Active=true`, with tailnet IP `100.121.88.110`.
- Verdict: stale historical reachability warning; the node is currently on the tailnet. No network/substrate mutation warranted.
