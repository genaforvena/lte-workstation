# Triage historical peer-recovery check-stream notice

Task: `health-warning/2589280966ba3570cbd9/triage`  
Source: `check-stream` delta at 2026-09-13T12:43:10Z

The source recorded imac-rozalia and win-q6gl9fir3qi returning to active/direct
status after earlier unavailable snapshots, while LAN presence remained
unknown and the then-running doctor check had stopped before final totals.
Current status is different: `mesh-path-watch --status` at 20:44:01Z on Sep 14
reports imac-rozalia relayed and Phaedra direct. A targeted Tailscale sample
shows iMac online/active via relay Helsinki and Windows online but idle via
relay Helsinki. These are changing peer-path snapshots, not evidence that the
Sep 13 recovery observation was false or that either peer's remote physical
state is known.

The 20:47Z check pane reports egress OK with 0% loss and still reports zero
LAN peers. The doctor row is a 13-minute-old cache (FAIL=0, WARN=33), not a
fresh comprehensive run; the source's incomplete 2-FAIL result is superseded
as a cached snapshot but not independently re-run here. LAN/router visibility
and the cause of the path changes remain unresolved. No routing, DNS, VPN,
firewall, or Tailscale state was changed.

## Verification

- `rtk mesh-dash --once check` at 20:47:41Z: egress OK, zero LAN peers,
  reachability probes flagged unreliable under high load, doctor cache age
  13m.
- `rtk mesh-path-watch --status` at 20:44:01Z: imac-rozalia relay;
  Phaedra direct.
- `rtk tailscale status --json` at about 20:47Z: iMac online/active via
  `hel`; Windows peer online/inactive via `hel`.
- No new task, peer, or substrate state was created or changed.
