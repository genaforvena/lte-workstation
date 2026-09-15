# Health-warning triage: `health-warning/c99b0c534fe4e2097c69`

Task: `health-warning/c99b0c534fe4e2097c69/triage`

## Verdict

The 2026-09-14T06:02:31Z check-stream warning is a known historical condition, not a
currently reproduced regression. The warning's two reported egress failures and LAN
unknown state are not evidence for a substrate change now. No substrate was modified.

## Evidence

- `mesh-dash --once check` at 2026-09-15T17:03:14Z reported the cached doctor result
  `FAIL=1 WARN=33`, with the known doctor smoke-test failure
  `mesh-historical-ask-ledger`; it also marked local load high, so cached/probe-derived
  fleet non-answers remain a known blindness.
- Direct `mesh-health` at 2026-09-15T17:04:07Z returned exit 0: local `mesh-home`,
  `imac-rozalia`, and `phaedra` were PASS; GL-MT3000 and Redmi 10 were reachable on LAN.
  The other listed offline nodes remain known fleet reachability limitations.
- Direct `mesh-net-triage --json` at 2026-09-15T17:04:12Z returned
  `verdict=CLEAN`, with `link=OK`, `lan=OK`, `wan=OK`, `path=OK`, and
  `degraded=none`.
- Read-only `tailscale status --json` at the same observation window showed the local
  backend Running, `phaedra` online with a handshake at 17:02:17Z, and
  `imac-rozalia` online with a handshake at 17:03:58Z. This does not erase the
  historical warning, but it shows the cited exit-node and iMac state are not currently
  in the warned condition.
- `mesh-task status health-warning/c99b0c534fe4e2097c69` showed the exact row active
  under owner `health`; dispatch eligibility was checked successfully before taking it.

## Result

Classified as recovered/known blindness. Preserve the cached doctor warning for its own
history; do not repair routing, DNS, firewall, VPN, or exit-node state from this stale
delta. Re-open only on a fresh direct reproduction or an unpredicted fleet transition.
