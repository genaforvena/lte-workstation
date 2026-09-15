# Health warning triage: September 9 check-stream delta

Chain: `health-warning/c236a08d9259317eef53/triage`  
Checked: 2026-09-12 09:05 UTC on `mesh-home`  
Source: the 2026-09-09 10:43Z report recorded 2 FAIL/34 WARN versus 4/33, cleared transient stress/USB/Wi-Fi test failures, and a new `mesh-card --test` “too slow to assess” warning.

## Current evidence

- The next historical check-stream delta at 11:42Z reported 3 FAIL/33 WARN, including a new `mesh-claude-deepseek` smoke-test FAIL. The September 9 improvement was not a durable all-clear.
- The consumed `mesh-dash --once check` pane at 08:56Z showed a cached doctor summary of 3 FAIL/33 WARN. Its displayed failures were egress via `tailscale0`, the configured exit-node SPOF, and `tinyfleet_split_audit.py` not executable. The pane did not expose a current `mesh-card --test` result, so the old “too slow” warning cannot be declared fixed from this evidence.
- The same pane showed the fleet degraded, `mesh-lan-presence`-type router state still unknown in prior receipts, phaedra online, and local egress/latency currently OK on the displayed interface. These readings do not justify route or VPN changes.
- The earlier 09:44Z triage receipt records current USB/Wi-Fi smoke failures and an incomplete comprehensive doctor run as of 05:58Z; see [health-warning-560b3316cab3f81a1182-triage-20260912.md](health-warning-560b3316cab3f81a1182-triage-20260912.md). No fresh comprehensive scan or `mesh-card --test` was started because the check pane warned that local load makes reachability probes unreliable.

## Disposition

The 10:43Z delta is historical, and its temporary clearing of several checks did not persist. Current known egress/exit-node failures and fleet/LAN visibility gaps remain. The old `mesh-card --test` timeout status is unresolved from the current pane; it is a known blind rather than a verified current failure. No substrate state was changed.
