# Live coordination and hledger audit — 2026-09-08

## Scope

Read the live board (`~/.mesh/chat.log`), task ledger, health output, and both hledger
axes from `mesh-home` at 2026-09-08 22:28 UTC.

## Verified healthy

- `mesh-promises --check`: parity PASS; board replay agrees with hledger for promises (81),
  claims (135), holds (58), and asks (63).
- `mesh-ledger --check`: parity PASS; 607 feed windows, zero overlaps and zero gaps.
- `mesh-labor --check`: parity OK; 5,635 TURN booked versus 6,009 TURN in `spend.log`,
  therefore no over-book.
- `mesh-labor --budget`: 212 TURN in the rolling five-hour window and $1,066.4570
  imputed inference spend. The USD and per-window caps are deliberately unarmed
  (`MESH_LABOR_BUDGET_USD=0`), so this is report-only rather than a hidden gate.
- Live task execution is advancing: the sound chain closed `fabricated-beat-picker` with
  a receipt and moved to `min-beats-material-cost`; the witness FYI/hledger experiment
  completed with a 952-row scratch journal passing `hledger check`.

## Open issues found on the board

- Three open promises are routed to non-roster owners: `ilya-back-online-push-restore-env`,
  `phone-authorized-keys-recheck`, and the parked-autostash repair promise.
- Dispatch queue still contains the parked-autostash repair, the active sound follow-up,
  two chat-review edges, and two tg-owned design/funnel tasks. They are visible in the task
  ledger; they are not silently treated as complete.
- `mesh-health --once`: only `mesh-home` and `phaedra` PASS; GL-MT3000, Redmi 10, ilya,
  imozerov (2), and rip are OFFLINE, and imac-rozalia is SSH-unreachable.
- The latest completed doctor run remains `2 FAIL / 33 WARN` (16:23 UTC); newer invocations
  were lock-skipped, so this is stale evidence, not a fresh clean verdict.
- The board's known current substrate concern is egress FAIL (`tailscale0 + exit-node`)
  and should remain owned by health/substrate stewards; this window does not alter routing.
- `mesh-labor --propose-cap` reports a measured median $237.0503, p95 $2,394.0950, and
  max $8,365.2150 over historical five-hour windows; it proposes `$10,039`, but arming it
  requires the operator's explicit decision and is intentionally not done here.

## Next action

Keep the current sound task and parked-autostash repair visible until their owners produce
receipts; route the three non-roster promises to a live owner or retire them; have the health
steward rerun `mesh-doctor` after the lock clears and investigate egress ownership. The hledger
axes are currently useful as integrity/replay evidence and budget observation; the next useful
expansion is the already-dispatched separate FYI commodity view, not inventing a cap.
