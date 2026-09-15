# Health-warning triage: `health-warning/269667bdf10a8298e047/triage`

- Checked: 2026-09-12 14:11–14:13 UTC on `mesh-home`.
- Exact-owner dispatch check exited 0; `health` claimed the task.
- This is a read-only triage. No routing, DNS, firewall, WireGuard, or Tailscale settings changed.

## Findings

- `mesh-card --refresh` confirms default egress through `tailscale0`, exit node `phaedra`, and
  `100.76.0.1` swallowed through `tailscale0` in table 52. Its invariant check fails. The card
  names the unresolved LAN route exclusion; no route was installed during this triage.
- `ip route get 100.76.0.1` independently returns `dev tailscale0 table 52`.
- `tailscale status --json` reports `phaedra` online and active at `38.49.216.141:41641`; the
  configured exit-node dependency therefore remains present. `imac-rozalia` is online, but its
  current-address field is empty in that status sample.
- `mesh-lan-presence --nodes` exits 1: router unreachable, LAN visibility `UNKNOWN` (no local
  address in `192.168.8.0/24` and no known host answered ICMP).
- `mesh-fleet-health` exits 0 but warns `LOCAL LOAD HIGH`, says reachability probes are unreliable,
  and classifies most peer results as `UNKNOWN(load)`. Its path reading is degraded at 8 peers,
  1 direct, 1 relay, with 6 offline. These UNKNOWN readings are not evidence that those peers are
  down.
- `mesh-health` reports this node PASS, `phaedra` online, `imac-rozalia` skipped because SSH
  authentication was refused, and the other listed peers offline by long last-seen intervals.
- `mesh-egress-health` exits 0 without diagnostic text. The one-shot check pane at 14:11 reports
  current egress OK (0% loss, 134.433 ms average) while its 24-hour summary is marked BAD with
  0/440 bad and 37 unattributed samples. The successful current sample does not clear the
  route/exit-node SPOF finding.
- The pane's doctor result is cached from 13:35:58Z (`FAIL=3 WARN=34`), so it is not a fresh doctor
  run. The pane also shows all organs live, with listed Bluetooth and edge-gate alarms; no sensor
  or reflex was changed in this triage.

## Disposition

Known gaps remain: LAN visibility is unknown and the LAN gateway follows the Tailscale exit route;
egress depends on `phaedra`; fleet reachability is currently unreliable under the probe's local-load
warning; and the doctor total is stale. Current external egress has a passing sample. Recheck the
LAN and fleet probes after their local visibility/load limitations clear. Any route correction must
follow the charter's single-writer claim and `mesh-dms` procedure.

## Verification

- `mesh-task check dispatch health-warning/269667bdf10a8298e047/triage health` — exit 0.
- `mesh-task status health-warning/269667bdf10a8298e047` — task active and owned by `health`.
- `mesh-card --refresh` — produced refreshed card; exit 1 on the displayed invariant violation.
- `mesh-lan-presence --nodes` — exit 1 with router-unreachable `UNKNOWN`.
- `mesh-fleet-health` — exit 0 with local-load probe warning and degraded path.
- `ip route get 100.76.0.1` — confirmed `tailscale0`, table 52.
