# External revival and online-confirmation blockers — 2026-09-12

This receipt applies to these adint-owned resolver rows:

- `unblock/bash/272e6e3fe70b653a/resolve` → `unblock/adint/c114f99a12f3db5d/resolve`
- `unblock/bash/87d1500a4586c97f/resolve` → `unblock/adint/4cc57fbd6684b8a0/resolve`
- `unblock/bash/d4ac830189f7699e/resolve` → `unblock/adint/3dd6562eb2e7cc86/resolve`
- `unblock/bash/7549c9e510da843e/resolve` → `unblock/adint/b220e5409ffe15e0/resolve`

## Fresh evidence

The live Health-owned targets remain blocked on the same external events recorded in the prior
receipts: transcriber revival decision, wake-reflex revival decision, and camera revival decision.
Read-only service checks returned `mesh-transcribe.service: not-found/inactive` and
`mesh-room-reflex.service: disabled/inactive`. Their sources remain held; these resolver rows do
not authorize a re-poke, enable, or start. The fresh `mesh-health` sweep at 04:53:17Z reported `ilya`
offline. The Steward target remains blocked on confirmation that Ilya is online before any
`restore.env` push. No service, remote file, route, or substrate state was changed.

## Exact external conditions

- **Transcriber:** operator decision to revive it and a supported recovery path; only then recheck
  the source and service.
- **Room wake reflex:** explicit operator authorization for the supported user-service recovery
  path; only then enable/start and independently verify it.
- **Room camera:** the named operator revival decision/event; keep the source held until it arrives.
- **Ilya/restore.env:** steward/operator confirmation of an `ilya-online` event; then redo the
  liveness check before any push.

The existing evidence is in `docs/task-receipts/unblock-adint-c114f99a12f3db5d-resolve-20260911.md`,
`docs/task-receipts/unblock-adint-4cc57fbd6684b8a0-resolve-20260911.md`,
`docs/task-receipts/unblock-adint-3dd6562eb2e7cc86-resolve-20260911.md`, and
`docs/task-receipts/unblock-adint-b220e5409ffe15e0-resolve-20260911.md`. No external authorization
was inferred or requested here; these conditions remain owned by their respective operators.
