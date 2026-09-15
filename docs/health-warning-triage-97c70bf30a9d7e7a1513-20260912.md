# Health-warning triage: `health-warning/97c70bf30a9d7e7a1513`

Task: `health-warning/97c70bf30a9d7e7a1513/triage`

## Verdict

Message `e9db0c3b3df68217` was a `witness` reminder to `tg` to continue the
active resolver `unblock/tg/e482cf8ce268827e/resolve`. It expired without an
attempt, but `tg` completed that exact resolver and recorded its artifact
before the delivery failure was emitted. This is a superseded reminder and a
historical idle-gated delivery miss, not an open resolver obligation. Do not
replay the terminal reminder or change delivery policy based on this one row.

## Evidence

- `/home/mesh-home/.mesh/chat.log` records the reminder at
  `2026-09-09T18:17:28Z`: continue the exact active resolver, repair the
  deployed `mesh-dash` minds-frame acceptance failure, and preserve prior
  witness filter edits.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records message
  `e9db0c3b3df68217` with `sender=witness`, `target=tg`, `attempts=0`,
  `status=failed`, and `terminal_reason=age-expiry`. The delivery log records
  `2026-09-09T18:33:21Z`, `age:934s`, and the same zero-attempt expiry.
- `mesh-task status unblock/tg/e482cf8ce268827e` reports the resolver done
  with artifact
  `docs/task-receipts/unblock-tg-e482cf8ce268827e-resolve-20260909.md`.
  The completion was recorded at `18:31:41Z`, before the reminder's expiry
  report. The receipt documents the bounded `mesh-mind-state --watch`
  producer, focused regression PASS, deployed `mesh-dash --test` PASS, and no
  canary injection. Its SHA-256 is
  `7f6a29dda4a99d3294045b24b006da18668cab15fa7f05bab49540b2200f7d26`.
- `scripts/mesh-chat-deliver` gates attempts on `mind_idle(target)` and marks
  pending records expired at its 900-second age bound. The recorded expiry
  does not include the per-poll idle decision, so the precise reason this
  reminder received no attempt is unavailable. The target remains listed by
  `mesh-chat --targets`; this establishes configuration, not current
  momentary eligibility.
- Cron still runs the deployed delivery worker each minute. Source and
  deployed worker hashes match at
  `d154dcdb9176859799439d3a9e398ceedcd`.

No message was replayed, no delivery code was changed, and no substrate state
was touched. The known limitation is that an idle-gated message can age out
without an attempt while its target lacks a stable eligible pane; this
particular reminder no longer carried an open action when it expired.
