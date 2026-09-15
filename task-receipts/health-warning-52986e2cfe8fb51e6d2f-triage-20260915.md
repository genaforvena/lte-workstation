# Health warning triage: stale doctor cache

Date: 2026-09-15
Task: `health-warning/52986e2cfe8fb51e6d2f/triage`
Owner: `health`

## Finding

The 2026-09-14 roll-call warning is confirmed as a cache-freshness gap, not a
new egress-policy incident. At the 2026-09-15 check, `~/.mesh/.doctor-fails`
and `~/.mesh/doctor.log` were both timestamped `19:37:04Z`; the current check
was around `20:20Z`. The cached summary reported `FAIL=1 WARN=33`, including
the known `dispatch.log` error.

The completed egress-policy receipts
`task-receipts/mesh-doctor-egress-policy-20260914.md` and
`task-receipts/reconcile-live-egress-policy-20260914.md` establish that
mesh-home intentionally consumes phaedra's exit node and that the LAN-prefix
FIB guard was healthy. No routing, DNS, VPN, or firewall change is warranted.

## Live refresh attempt

`mesh-doctor --quiet` started a fresh read-only sweep and emitted current
warnings (microphone busy, untimed peer SSH to `mesh-load-audit`, six sole-path
bypasses, and five absence-as-negative sites), but did not complete within
the bounded observation window because of the untimed peer-SSH work. It was
stopped with exit 130; no substrate state was changed.

## Verification

- `mesh-task check dispatch health-warning/52986e2cfe8fb51e6d2f/triage health` — exit 0.
- `mesh-doctor --help` — completed; cache and supported modes confirmed.
- Current doctor cache timestamps and contents inspected.
- Prior egress-policy and live-FIB receipts inspected.
- Bounded `mesh-doctor --quiet` refresh attempted; incomplete state recorded honestly.

Disposition: confirmed stale doctor cache and existing bounded peer-SSH
limitation; leave network policy unchanged and allow the scheduled doctor
refresh to produce the next complete cache.
