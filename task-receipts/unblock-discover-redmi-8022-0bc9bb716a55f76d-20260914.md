# Redmi SSH unblock diagnosis — 2026-09-14

Task: `unblock/discover/0bc9bb716a55f76d/resolve`
Parent: `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`

## Ledger and instruction check

At 09:35 UTC, the unblock task was `open`; the parent retry was still `blocked` on
`event:first-successful-redmi-ssh-port-8022-probe`. The parent receipt records the bounded
09:24 SSH attempts to `100.103.99.16`, `192.168.8.203`, and `192.168.8.146`, all timing out.
Nothing in the current ledger or implementation makes that event predicate stale or incorrect:
the parent can proceed only after an SSH connection to a Redmi `:8022` endpoint succeeds.

## Fresh state and safe-prerequisite audit

At 09:38:39 UTC, `mesh-health --node Redmi` reported `OFFLINE`, last seen 10 days earlier,
with the configured off-tailnet fallback unanswered. At 09:39:26 UTC:

- `tailscale status --json` still reported Redmi 10 `Online=false`, `LastSeen=2026-09-03T09:53:36.1Z`,
  and no current endpoint address; the peer IP remains `100.103.99.16`.
- The Redmi LAN candidate `192.168.8.203` routes via the default gateway `100.74.0.1`, not a local
  `192.168.8.0/24` interface. This node therefore has no direct Redmi LAN path at present.
- `adb devices -l` lists only serial `4d00553d61ab90b7`, model `SM-N900` (the Note 3), not the Redmi.
- `~/.mesh/nodes` deliberately leaves `PHONE_ADB_SERIAL` unset because the Redmi's wireless ADB is
  unpaired and its port changes. `scripts/mesh-phone-ip` correctly skips its ADB tunnel without an
  explicit body serial; using the attached Note 3 would violate its guard and could report that
  handset's state as Redmi data. `docs/body.md` says the Redmi watchdog requires ADB-over-Wi-Fi
  pairing, which itself needs the phone UI.

The existing narrow local safeguards are correct; no code or network configuration change can
restore a handset that has neither a reachable SSH/Tailscale path nor an authorized paired ADB
transport. Repeating the three SSH timeouts would add no evidence while the tailnet state and route
remain unchanged, so no redundant connection attempts were made.

## Result and next action

The blocker is irreducible from this node at this time and requires external handset state: the
operator must wake/unlock the Redmi and restore Termux `sshd` or Tailscale (and, if using the ADB
watchdog path, complete wireless-debugging pairing). Do not resume the parent yet. Resume it only
after a fresh successful Redmi `:8022` SSH probe, then run the remaining Termux candidates on that
responsive endpoint.
