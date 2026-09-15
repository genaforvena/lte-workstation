# Unblock check — Redmi Termux frontier — 2026-09-14

Task: `unblock/discover/65a11a6caeb97350/resolve`

## Live evidence

At 2026-09-14 09:30 UTC:

- `mesh-health`: mesh-home and phaedra PASS; Redmi 10 OFFLINE, last seen 10 days ago; configured
  off-tailnet fallback unanswered.
- `tailscale status --json`: Redmi peer `Online=false`, `LastSeen=2026-09-03T09:53:36Z`, no current
  endpoint address or handshake.
- `tailscale ping -c 1 100.103.99.16`: no reply; timed out.
- `ip route get 100.103.99.16`: `dev tailscale0 table 52`, so a local route exists.
- At 09:24 UTC, one bounded SSH/Termux attempt timed out on each of the three documented
  `:8022` endpoints (100.103.99.16, 192.168.8.203, 192.168.8.146); all returned SSH exit 255.

The working tailnet path to phaedra and the local route rule out a general mesh-home network outage.
All available evidence points to the handset being offline, rather than a missing local route or a
reachable sshd refusal. No remote repair path is available while the phone is offline, and this
window has no independent physical path to wake it.

## Decision

No in-scope prerequisite can restore the handset from this node. Keep the parent retry step blocked
with `unblock=pending`; retry only on the event that a Redmi `:8022` SSH connection succeeds. Do not
reclassify the Termux verbs as absent and do not repeat unchanged timeouts.
