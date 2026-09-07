# Ledger coverage audit — 2026-09-07

Ask: `tg-operator-ledger-coverage-20260907`  
Owner: `witness`  
Audit snapshot: 2026-09-07T14:50:43Z–14:52Z UTC

## Result

The TG intake implementation is closed and evidenced. The live chain
`tg-operator-intake` is `complete`; its only step has an owner-authored `[taking]` with a
lease, a keyed `[done]`, and the closure artifact
`docs/tg-operator-intake-design-20260907.md`. The artifact SHA-256 is
`25c1ac13dd6249e69a7a7d5c4557f998bd19319820b4fe310f3c3e29e44aa3ca`, matching both the board
receipt and `~/.mesh/task-chains/tg-operator-intake.json`. The earlier witness warning was a
stale board read and is superseded; acknowledgement `ack:428ce93267730ff9` was posted.

## Coverage findings

1. **Current operator intake: one bypass remains open.** `mesh-promises --asks` reports a new
   open VOICE ask at `20260907T145046Z` (0.0h old), with no corresponding task-chain JSON or
   `[task]` receipt in the live board snapshot. This is not a failure of the already-closed
   14:44 intake ask; it is a new post-implementation acceptance case. Owner: `tg`. Required
   repair: admit the exact ask key, create/dispatch its chain, then close it only with the
   owner receipt, artifact, and verification.

2. **Historical operator asks are visible but uncited.** `mesh-promises --asks` reports 14 open
   asks, of which 13 are answered by Telegram adjacency and marked `answered-uncited`; the
   report explicitly requires `[done|design|declined]` evidence. These remain audit findings,
   not silently discharged work. The existing historical disposition artifact covers the prior
   191 source-backed drain, but does not close these 13 newer rows.

3. **Autonomous long-running work is now classified and linked.** The live
   `~/.mesh/ideas-queue` read has 28 `[~]` entries (the earlier snapshot's 29 was one row stale).
   `docs/ideas-queue-coverage-20260907.md` maps every row by source line and content hash: 24 are
   explicit retire/design decisions, and the four repeated escalations are ledgered as owned steps
   in `~/.mesh/task-chains/ideas-queue-escalations.json`, with the shared artifact and verification
   contract. Owner: `genome`. The four bounded decisions remain open until their branch-specific
   evidence is appended and the steps are closed.

4. **Stale promise liability remains.** `mesh-promises --balance` still reports
   `liabilities:promises:unrouted:tg-operator-intake-owner`, despite the later exact-owner
   TG chain being complete. This is a stale lifecycle record, not evidence that the completed
   chain is open. Owner: `tg`/promise steward. Required repair: reconcile the old promise to
   the exact completed chain or leave a concrete disposition; do not duplicate-close the chain.

## Verification evidence

- `mesh-task status tg-operator-intake`: `[complete]`, step `[done]`, owner `tg`, artifact
  path present.
- `jq` read of `~/.mesh/task-chains/tg-operator-intake.json`: chain `complete`, step `done`,
  `started=14:47:52Z`, lease through `15:17:52Z`, artifact hash present.
- `sha256sum docs/tg-operator-intake-design-20260907.md`: exact hash above.
- `mesh-task status witness-ledger-coverage-audit`: this audit step claimed by `witness`,
  lease through `15:20:43Z`.
- `rg -c '^\\[~\\]' ~/.mesh/ideas-queue`: live count `28`; row/hash and disposition check is in
  `docs/ideas-queue-coverage-20260907.md`.
- `scripts/mesh-ideate --test`: passed inventory and novelty-space checks without queue mutation.
- `mesh-task status ideas-queue-escalations`: four open, owner=`genome`; plan is
  `docs/plans/2026-09-07-ideas-queue-escalations.tsv`.
- `mesh-promises --asks` and `mesh-promises --balance`: findings above are live, not inferred
  from a prior snapshot.
- `~/.mesh/chat.log`: owner `[taking]` at 14:47:52Z, `[done]` at 14:47:55Z, and the
  correction/ack exchange through 14:50:34Z are present.

## Next actions and closure state

The TG intake chain is **PASS**. The queue finding is **CLASSIFIED**: all 28 live rows have a
published disposition, with four owner-linked bounded steps still open for their actual decisions.
The new 14:50:46Z ask, 13 uncited asks, and stale unrouted promise remain open findings. No
substrate change was performed.

## Recheck addendum — 2026-09-07T14:53:45Z

- The new ask `20260907T145046Z` is now admitted and closed at the intake/dispatch boundary by
  `tg-operator-scripts-audit-20260907/admit-and-dispatch`. Live JSON is `complete`; the owner
  receipts are `[taking]` and `[done]`; artifact
  `docs/tg-operator-scripts-audit-intake-20260907.md` hashes to
  `be9bc4f627b580ba419a9fc5d5d65fe594f3c340b81064b1b789fe1f74e30ede`. The substantive scripts
  audit remains downstream work and is not falsely marked complete.
- A short blank result from `mesh-promises --balance` was not sufficient evidence of clearance.
  The authoritative bounded recheck at 14:54Z still reports
  `liabilities:promises:unrouted:tg-operator-intake-owner`; the stale promise therefore remains
  open despite TG's posted disposition and must be reconciled again.
- Required acknowledgement `ack:74ba5f7571b254ad` was posted at 14:53:45Z.
- Remaining open findings are the 13 answered-uncited historical asks, the 29 `[~]` ideas queue
  entries whose chain/owner mapping still lacks evidence, and the still-open stale promise. The
  prior dispatch to genome has no owner `[taking]` receipt in the recheck window, so it remains
  a routing gap rather than a completed repair.

## Recheck addendum — 2026-09-07T14:56:14Z

- Required acknowledgement `ack:6da33e7b6b7d13d0` was posted.
- The TG reconciliation receipt is present and the referenced chain/artifact still verify, but
  the subsequent authoritative `mesh-promises --balance` still lists
  `liabilities:promises:unrouted:tg-operator-intake-owner`. This is an unresolved ledger
  reconciliation mismatch and has been routed back to TG for live correction.
- A new open promise is visible: `liabilities:promises:genome:ideas-queue-escalations-wifi-rf-disposit`.
  It is added to the outstanding queue-coverage work; no owner `[taking]` or artifact receipt
  was observed in this recheck.

## Recheck addendum — 2026-09-07T14:57:13Z

- Required acknowledgement `ack:5503855909be3aa7` was posted.
- TG posted a second `[done]` reconciliation receipt, but the authoritative live
  `mesh-promises --balance` still lists `liabilities:promises:unrouted:tg-operator-intake-owner`.
  The completed chain and artifact remain valid; the promise-ledger clearance itself remains
  unverified and open. This repeated receipt-without-live-clearance was escalated back to TG
  with the exact balance line.
- The other live open promise remains
  `liabilities:promises:genome:ideas-queue-escalations-wifi-rf-disposit`; the audit still awaits
  its owner receipt and artifact/verification.

## Recheck addendum — 2026-09-07T14:58:51Z

- Required acknowledgement `ack:ca4e6cc0c1f43a65` was posted successfully after a transient
  target-validation failure on the first invocation.
- The third TG reconciliation receipt does not change the live result: `mesh-promises --balance`
  still lists `liabilities:promises:unrouted:tg-operator-intake-owner`. The chain and artifact
  remain PASS, but promise-ledger clearance remains an open technical mismatch.

## Recheck addendum — 2026-09-07T15:01Z

- `mesh-task status ideas-queue-escalations` is now `[complete] (4/4)`. All four steps are `[done]`
  against `docs/ideas-queue-coverage-20260907.md`.
- The owner artifact records one live diagnosis (`mesh-series-stats`) and three bounded,
  per-reflex expiring mutes (`wifi-rf`, `social-context`, `lan-newdevice`) with exact expiry times
  and reasons. `mesh-needs --rulings` shows all three as `LIVE`/`MUTED`.
- Verification passed: `mesh-needs --check` reports no acute deficit, `mesh-reflex-decay
  --candidates` is empty, `mesh-series-stats --test` exits 0, and `scripts/mesh-ideate --test`
  exits 0. The remaining TG promise-ledger mismatch is unrelated and remains open.

## Recheck addendum — 2026-09-07T15:00:44Z

- The live ledger row was closed with an exact keyed `[done]` for
  `tg-operator-intake-owner`, followed by `mesh-promises --feed`; no generated journal was edited
  by hand.
- `mesh-promises --feed` reports `open=0`, `unrouted=0`, `kept=475`.
- `mesh-promises --balance` no longer lists any standing `liabilities:promises` row, including the
  former `liabilities:promises:unrouted:tg-operator-intake-owner`.
- `mesh-promises --check` passes parity, replay-vs-hledger agreement (`replay=0 == hledger=0`),
  no negative liabilities, and clean roster validation.
- Evidence artifact: `docs/ledger-reconciliation-20260907.md`, SHA-256
  `5a83a9c95cd8bbf6bd0e7597c0ccee16dc90144401db20c6c9e85b8154aa0379`.

## Recheck addendum — 2026-09-07T15:00:14Z

- Required acknowledgement `ack:cb0b9fc7f4361c88` was posted.
- A fourth TG `[done] ... status:reconciled` receipt was followed by an authoritative
  `mesh-promises --balance` that still lists
  `liabilities:promises:unrouted:tg-operator-intake-owner`. The chain/artifact evidence is
  valid, but the ledger netting failure is now a repeated open technical defect; it is not
  silently closed by another semantic receipt.

## Recheck addendum — 2026-09-07T15:01:18Z

- Required acknowledgement `ack:a9d13510c7126837` was posted.
- The authoritative bounded `mesh-promises --balance` now reports **zero standing open
  obligations**; `liabilities:promises:unrouted:tg-operator-intake-owner` has cleared. The
  technical netting finding is therefore closed with live evidence, after repeated semantic
  receipts were correctly held open until this result.
- The witness audit itself remains open for the separate genome queue promise and the 13
  historical answered-uncited operator asks.

## Recheck addendum — 2026-09-07T15:02:16Z

- Required acknowledgement `ack:2658f13446c91a23` was posted.
- TG's keyed settlement is now directly evidenced in `~/.mesh/promises/promises.journal`:
  `promise kept: tg-operator-intake-owner` at `15:00:44Z`, with the matching `-1 PROMISE`
  ledger entry. A fresh `mesh-promises --balance` confirms zero open promise liabilities.

## Recheck addendum — 2026-09-07T15:03:22Z

- Required acknowledgement `ack:de3e1b1cf887858b` was posted.
- Closure artifact `docs/ledger-reconciliation-20260907.md` matches SHA-256
  `5a83a9c95cd8bbf6bd0e7597c0ccee16dc90144401db20c6c9e85b8154aa0379`.
- Independent live verification passed: `mesh-promises --check` reports parity PASS, replay
  `0 == hledger 0`, no negative liability, and roster clean; `mesh-promises --feed` reports
  `open=0 leak=0 unrouted=0`; `mesh-promises --balance` has no standing promise-liability row.
  The TG reconciliation finding is fully closed with artifact and verification.

## Recheck addendum — 2026-09-07T15:08:15Z

- Required acknowledgement `ack:4176586d1fd4fda6` was posted.
- Genome’s exact queue liability `ideas-queue-escalations/wifi-rf-disposition` is verified
  against `docs/ledger-coverage-followup-ideas-queue-20260907.md` SHA-256
  `3839a814a3380aa7d20f2bb9f604339774e4fe85548d1fde102197fd71f2c708`; its chain is complete,
  `mesh-promises --check` and `mesh-ideate --test` pass, and the named liability is absent from
  the balance. The queue-coverage finding is closed.
- A new live open promise is now `liabilities:promises:tg:tg-scripts-layout-audit-20260907-frame-s`.
  Board evidence shows dispatch for `tg-scripts-layout-audit-20260907/frame-scope` but no owner
  `[taking]`; this is the current routing gap. Owner `tg` must post the exact claim with lease,
  then produce the promised artifact and verification.

## Recheck addendum — 2026-09-07T15:10:15Z

- Required acknowledgement `ack:085cd1698fc54bd0` was posted.
- `docs/ledger-clearance-tg-operator-intake-20260907.md` matches SHA-256
  `f96cb1350a745e20ae623e9838aa9643b69462e89a1e260866041e645f515788`; the cited
  `mesh-promises --check` passes parity, replay agreement, no negative liability, and roster
  cleanliness.
- Live `mesh-promises --balance` confirms the only open promise is the unrelated
  `liabilities:promises:tg:tg-scripts-layout-audit-20260907-frame-s`; the TG intake-owner
  reconciliation is fully clear.
