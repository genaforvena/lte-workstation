# Health-warning triage: `health-warning/48086a40f47c0f2cbb1a`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/48086a40f47c0f2cbb1a/triage`

## Finding

The Sep 9 watchdog warning is a historical reachability failure that is
currently recovered. Its snapshot said mesh-home had not been seen on the
tailnet for 21 minutes and phaedra had no LAN fallback. The current health pane
reports `mesh-home(LOCAL vitals=OK up=ok)` and `phaedra(yes vitals=OK up=ok)`.
The pane also reports high local load and explicitly warns that reachability
probes are unreliable, so this confirms the current reported state without
proving the original cause or every path.

## Evidence

- `/home/mesh-home/.mesh/chat.log:41919` records the source warning at
  `2026-09-09T13:41:51Z`:
  `watchdog@phaedra :: [health-fail] mesh-home — UNREACHABLE (100.81.222.19
  (tailnet: last-seen 21m ago, active=True) — not on tailnet + no LAN fallback,
  worse than no-internet)`.
- `/home/mesh-home/.mesh/chat.log:41916-41917` records phaedra's own mesh
  status changing down at 13:23:49Z and back up at 13:26:52Z, before the
  watchdog warning. This is consistent with transient connectivity, but does
  not establish the exact path failure at 13:41.
- `mesh-dash --once check` at `2026-09-12T04:19:32Z` reports mesh-home and
  phaedra up in the fleet pane. It also reports
  `PROBE-WARNING: LOCAL LOAD HIGH — reachability probe UNRELIABLE`.

## Disposition and limit

Classified as recovered historical reachability loss with cause unresolved.
The current pane supports recovery; it cannot reconstruct the Sep 9 path or
distinguish a tailnet outage from a watchdog probe/observation gap. No routing,
DNS, firewall, VPN, or Tailscale state was changed. No additional reachability
probe was treated as reliable under the pane's current load warning.

## Verification

```text
mesh-dash --once check
mesh-task check dispatch health-warning/48086a40f47c0f2cbb1a/triage health  # exit 0
MESH_TASK_ACTOR=health mesh-task take health-warning/48086a40f47c0f2cbb1a triage
```
