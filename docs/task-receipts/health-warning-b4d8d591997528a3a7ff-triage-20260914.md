# Triage repeat Redmi Termux discovery notice

Task: `health-warning/b4d8d591997528a3a7ff/triage`  
Source: health FYI at 2026-09-13T02:17:00Z

The source repeats a negative discovery result: all three Redmi `:8022`
endpoints timed out, no Termux command was sampled, and attached USB device
`04e8:6860` is known prior art. The earlier
`health-verify-discover-termux-20260913.md` records those same facts. A newer
Redmi triage on Sep 14 confirms the phone remains offline (last seen 11 days
ago) and identifies the existing exact follow-up:
`discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`,
blocked on `event:first-successful-redmi-ssh-port-8022-probe`. Its documented
retry condition has not changed. Current `mesh-health` at 20:24Z still showed
Redmi offline; no new endpoint probe or Termux command evidence has appeared.

Disposition: stale duplicate negative-result notice. Preserve SAF contents and
Termux behavior as unknown until the existing first-successful-SSH event
occurs; do not repeat unchanged timeouts. No device, transport, or network
state was changed.

## Verification

- Read the earlier discovery receipt and the newer duplicate-Redmi warning
  receipt; both document the same prior-art device and transport limit.
- `rtk mesh-health` at 20:24Z reported Redmi 10 offline, last seen 11 days.
- `rtk mesh-task status discover-redmi-termux-frontier-followup-20260914`
  confirmed its retry step remains blocked on the exact external-success event.
- No repeat probe was run because the reachability condition had not changed.
