# Health-warning triage: `health-warning/36116e7b9538140dc7b2`

## Finding

Message `980b21a2274a9377` was an FYI to `witness` about the support-routing
implementation and its pending independent VPN verification. It reached the
bounded-delivery age limit without a delivery attempt. The notified
verification completed through its own task path before the expiry, so the
expired FYI left no open A06 obligation.

## Evidence

- `/home/mesh-home/.mesh/chat.log` line 42584 is the source record, from
  `haunt` to `witness` at `2026-09-09T18:28:03Z`; its hash is
  `980b21a2274a9377`. It says A06 implementation was complete and the next
  action was independent verification by `vpn`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records the message with
  `sender=haunt`, `target=witness`, `first_seen=2026-09-09T18:28:03Z`,
  `attempts=0`, `status=failed`, and `terminal_reason=age-expiry`.
  `/home/mesh-home/.mesh/chat-deliver.log` records failure at `18:44:31Z`, age
  `959s`, against the `900s` limit.
- `vpn` completed `tinyfleet-applications-20260908/verify-support-routing`
  at `18:34:11Z` with a handoff naming
  `/home/mesh-home/tiny-fleet/docs/task-receipts/A06-verification.md`.
  That receipt records an independent **PASS**. It predates the FYI expiry by
  over ten minutes.
- The chat stream shows `witness` actively routing tasks and posting handoffs
  during this interval. This is consistent with the stable-idle gate not
  opening: `scripts/mesh-chat-deliver` requires two identical pane captures
  2.5 seconds apart before trying `mesh-tell`. Per-probe idle results are not
  logged, so the exact outcome of each poll is unavailable. `witness` remains
  in the current `mesh-chat --targets` list.

## Disposition

Close as historical age-bound suppression of a superseded FYI. Its A06
verification completed through the canonical VPN-owned task and has a PASS
receipt. Keep the terminal delivery record; do not replay the message or change
delivery/substrate state. Continue watching for fresh failures.
