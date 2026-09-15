# Health-warning triage: `health-warning/d7572f8bce50299dfe38/triage`

- Checked: 2026-09-12 14:17–14:19 UTC on `mesh-home`.
- The exact-owner dispatch check exited 0 and `health` claimed the task.
- Read-only triage; no route, DNS, firewall, WireGuard, or Tailscale settings changed.

## Findings

- `mesh-dash --once check` returned no visible stdout in this session. The pane itself did not
  provide a readable state payload in this invocation.
- `mesh-card --refresh` refreshed at 14:18:33Z and exited 2 on invariant violations. It reports
  default egress through `tailscale0`, exit node `phaedra`, and the LAN route exclusion still
  missing: `100.74.0.1` routes through `tailscale0` table 52. The card gives the candidate FIB
  exclusion (`throw 100.74.0.0/16 table 52`); it was not applied.
- `ip route get 100.76.0.1` independently returns `dev tailscale0 table 52`. The card's current
  LAN gateway is `100.74.0.1`; both readings show the same exit-node table swallowing the LAN
  range.
- `mesh-lan-presence --help` was not a help mode; it ran the live read and exited 1 with
  `router unreachable — UNKNOWN`, no local address in `192.168.8.0/24`, and no known host answering
  ICMP. This remains an explicit LAN-visibility blindness, not proof the router is down.
- `mesh-fleet-health --help` likewise ran the live probe and exited 0. Its local row was healthy
  at 14:17:51Z; its PATH summary, timestamped 14:14:01Z, says `OK`, 8 peers, 2 direct, 0 relay,
  6 offline. The prior `LOCAL LOAD HIGH` warning was absent in this run. Peer offline labels are
  still bounded probe observations, not a claim that every peer is physically down.
- `mesh-health` at 14:18:33Z reports `mesh-home` and `phaedra` PASS, `imac-rozalia` SKIP because
  SSH authentication was refused, and the remaining listed peers OFFLINE by last-seen age.
- `mesh-egress-health` exited 0 without diagnostic text. The refreshed card reports upstream OK
  and public IP `38.49.216.141`; that outward egress does not clear the separate LAN route
  invariant failure.
- The card also reports identity-coherence CONFLICTED (26) and an `imac-notify` organ probe that
  exceeded 8 seconds. These are visible additional warnings; no identity or organ configuration
  was changed.

## Disposition

Current outward egress and the local node are healthy, while LAN presence remains UNKNOWN and the
LAN range is still swallowed by table 52. Fleet path state improved from the earlier load-limited
sample, but the summary timestamp precedes the local row and should be treated as a bounded sample.
The route invariant remains a known alarm. Any correction still requires a fresh substrate claim,
operator coordination, and a `mesh-dms` rollback before applying the FIB exclusion; no such claim or
change was made during this read-only triage.

## Verification

- `mesh-task check dispatch health-warning/d7572f8bce50299dfe38/triage health` — exit 0.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/d7572f8bce50299dfe38 triage` — claimed.
- `mesh-card --refresh` — live card refreshed; exit 2 with the swallowed-route invariant.
- `ip route get 100.76.0.1` — `tailscale0`, table 52.
- `mesh-lan-presence --help` — actually performed a read; exit 1, LAN UNKNOWN.
- `mesh-fleet-health --help` — actually performed a read; exit 0, PATH OK, 2 direct / 0 relay / 6 offline.
- `mesh-health` — local node and `phaedra` PASS; peer observations as listed above.
- `mesh-egress-health` — exit 0, no diagnostic text.
