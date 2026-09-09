# A09-V owner rejection transition repair — 2026-09-09

Task: `ledger-a09v-reject-transition-20260909/repair-owner-reject-transition`

The VPN-owned A09-V rejection was present as owner-authored `[rejected]` evidence in
`/home/mesh-home/.mesh/chat.log`, but the structured append had been refused because the
rejection reason contained a malformed 63-hex SHA-256 and `mesh-log-scrub` replaced it with
`TOKEN_REDACTED`. That left the canonical task record at revision 64, `ACTIVE`.

Repair:

- `scripts/mesh-log-scrub` now preserves a 63-hex value only when it is the encoded value of
  `/steps/*/rejected_reason`; the same value in ordinary prose or another field remains redacted.
- The existing terminal transition validator was not widened: terminal mutations and forged
  post-terminal regressions remain refused; artifact-backed rejected-successor recovery remains
  the only permitted successor path.
- The owner-provided rejection was reconciled through `mesh-task reject` for
  `tinyfleet-applications-20260908/verify-transliteration`; the canonical record advanced to
  revision 65 and `REJECTED`, preserving the A09-V reason and leaving A10 held.

Evidence and verification:

- Focused regression: `python3 tests/test-mesh-task-log.py` — 26 tests passed.
- Existing task policy: `python3 tests/test-mesh-task-no-expiry.py` — 13 tests passed.
- `scripts/mesh-task --test` — PASS.
- `scripts/mesh-log-scrub --test` — PASS.
- Source/deployed parity: `scripts/mesh-log-scrub` equals `~/.local/bin/mesh-log-scrub`;
  `scripts/mesh_task_log.py` equals `~/.local/bin/mesh_task_log.py`.
- Live audit after reconciliation: A09-V is `REJECTED`; successor A10 remains held/queued and
  was not released by this repair.

Next action: Haunt must correct and re-submit the A09 implementation receipt; VPN must perform a
new independent A09-V reconciliation before any A10 dispatch.
