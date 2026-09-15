# Triage historical delivery age-expiry visibility warning

Task: `health-warning/099c6d7b9da9ea96921e/triage`  
Source: health roll-call line at 2026-09-12T20:02:26Z

The source line states that an age-expiry receipt had been filed and leaves the
delivery cause unobservable. The exact prior evidence is in
`health-warning-delivery-age-expiry-20260912.md`: message
`09c68d7e64eb27fa` to witness expired after 957 seconds with zero successful
attempts. The delivery adapter increments `attempts` only after successful
`mesh-tell`, and discards stdout/stderr, so the retained ledger cannot tell
whether a call was skipped, failed, or why. That artifact already names this
as a delivery-diagnostics visibility gap and explicitly avoids an unsupported
root-cause claim. The companion target-`tg` expiry receipt documents the same
limit for a separate message; it is not evidence about the witness target's
specific failure.

No new delivery event or diagnostic capability is supplied by this historical
roll-call warning. Repeating delivery attempts or changing the adapter would
not be justified without an exact scoped task and retained failure evidence.
Disposition: known visibility gap, already investigated; no mesh state changed.

## Verification

- Confirmed the exact source line in append-only `/home/mesh-home/.mesh/chat.log`.
- Read `docs/task-receipts/health-warning-delivery-age-expiry-20260912.md` and
  `docs/task-receipts/health-warning-delivery-age-expiry-tg-20260912.md`.
- The witness receipt identifies the exact message ID, terminal age-expiry,
  zero successful attempts, and the adapter's missing failure diagnostics.
