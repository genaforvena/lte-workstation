# Witness A09 reconciliation dispatch — 2026-09-09

At 2026-09-09T19:48:48Z, the corrected A09 implementation receipt was inspected and
the pinned raw artifact claim was recorded as the exact 64-hex SHA-256
`bf7b5e768d07dbb7bad309226d6dcced00fe8bc1833ac08b1a62c521bcb16b5c`.

The original canonical chain remains terminally `REJECTED` at
`tinyfleet-applications-20260908/verify-transliteration` (revision 65), with its
dependent A10 and A10-V rows held. A fresh owner-scoped chain was created and
dispatched:

`tinyfleet-a09-v-reconcile-20260909/reconcile-a09-v`, owner `vpn`, ask
`tg-tinyfleet-review-20260908`.

Live verification after dispatch:

- `mesh-task status tinyfleet-a09-v-reconcile-20260909`: `open`, 1/1, owner `vpn`.
- `tasks.journal`: `QUEUED ... dispatch=sent`.
- No owner-authored `[taking]` exists yet for the fresh task; this is intentionally
  still open and not treated as started.
- `mesh-task audit` still reports the historical rejected A09-V and does not show a
  false PASS. A10 remains undispatched.

The correction source receipt is
`/home/mesh-home/tiny-fleet/docs/task-receipts/A09-receipt-hash-correction.md`;
its reported correction commit is `fa6a61f`.
