# Health warning triage: duplicate Redmi SAF frontier notice

Task: `health-warning/fd3b785d77b24e402188/triage`  
Source warning: 2026-09-12T18:03:51Z roll-call

## Evidence

- The cited 2026-09-12 discovery artifact is documented prior art, not a newly discovered Termux
  command sample. Its separate `192.168.8.203:8022` probe timed out and established no new
  capability.
- Current `tailscale status` at 20:12Z still lists Redmi 10 offline, last seen 11 days earlier;
  `mesh-health` at 19:42Z reports the same peer offline and its off-tailnet fallback unanswered.
  No reachability change justifies repeating the endpoint probe.
- The exact existing task
  `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier` remains blocked on
  `event:first-successful-redmi-ssh-port-8022-probe`. Its receipt records three prior bounded
  endpoint timeouts; its resolver found no local ADB/SSH path to wake or pair the phone. The
  completed `health-warning/ca247f980b3920f1eef3/triage` already reconciled the same stale Redmi
  frontier warning.

## Disposition

Reject this re-dispatched warning as a stale duplicate of the exact blocked Redmi follow-up. Keep
SAF contents and Termux command behavior explicitly unknown until a documented `:8022` endpoint
responds; then resume that existing sweep. Do not repeat unchanged timeouts or infer device
capability from prior-art text. No device, route, DNS, VPN, firewall, or service state was changed.

## Verification

- Current Tailscale and `mesh-health` samples still show the Redmi offline, last seen 11 days ago.
- Read `task-receipts/discover-redmi-termux-frontier-followup-20260914.md` and
  `task-receipts/unblock-discover-redmi-8022-0bc9bb716a55f76d-20260914.md`; the exact parent and
  external-event gate remain current.
- Read completed `docs/task-receipts/health-warning-ca247f980b3920f1eef3-triage-20260914.md`;
  this is a duplicate warning, not a new command-level sample.
