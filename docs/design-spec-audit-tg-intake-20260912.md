# TG intake and scripts-audit coverage review

Task: `design-spec-task-sweep-20260907/audit-tg-intake`  
Audited: 2026-09-12

## Finding

The intake design states the right general rule: actionable work gets an ask key and an owner chain,
larger work is decomposed before execution, and closure requires an artifact. The specific scripts
receipt does not itself cover that substantive work. Its only step is `admit-and-dispatch`; the
chain `tg-operator-scripts-audit-20260907` is complete 1/1 with that intake receipt as its artifact.
The scripts/layout work lives in separate chains and is not linked from that receipt by task ID.

The later layout chain produced a broad inventory/map and reversible migration plan. Those artifacts
enumerate possible duplicates and dead code but explicitly say they are candidates, not verdicts.
They do not provide the requested evidence-backed duplicate/dead-code decisions, risk/priority
assessment, or a task/disposition for each candidate. The layout migration chain handles future
directory moves and does not close this semantic audit gap.

The intake design also defines acceptance as an isolated synthetic TG ask that propagates its ask
key, dispatches one owner, and refuses closure without an artifact. The located intake receipt and
ledger audit establish durable chain/artifact behavior for real work, but I found no evidence of that
acceptance gate being exercised. The exact ask's later scripts/layout chain does not prove the TG
synthetic-intake path.

## Evidence inspected

- `docs/tg-operator-intake-design-20260907.md`: decomposition and artifact-closure contract; the
  synthetic TG ask acceptance condition.
- `docs/tg-operator-scripts-audit-intake-20260907.md` and
  `docs/plans/2026-09-07-tg-operator-scripts-audit.tsv`: the admitted ask and its sole
  `admit-and-dispatch` step.
- `~/.mesh/task-chains/tg-operator-scripts-audit-20260907.json`: complete 1/1, artifact is the
  intake receipt.
- `docs/tg-scripts-layout-audit-map-20260907.md`: duplicate/dead candidates explicitly left
  unresolved pending caller and deployed-copy review.
- `docs/tg-scripts-layout-audit-result-20260907.md`: reversible layout/migration slices; no
  semantic duplicate/dead-code verdicts.
- `docs/tg-scripts-layout-migration-audit-20260912.md`: current manifest foundation and ordered
  migration work, without claiming the semantic audit is complete.
- `docs/design-audit-current-coordination-20260912.md`: records the intake and layout chains as
  complete while keeping migration work open; it does not close the two gaps above.

## Disposition and follow-up

Intake/dispatch is closed; substantive coverage is **partial**, not complete. A new exact-owner
follow-up chain under the original ask key records both missing acceptance obligations:

- `tg-intake-coverage-followup-20260912/scripts-semantic-coverage`: resolve and prioritize the
  semantic duplicate/dead-code candidates and ledger each resulting task or disposition.
- `tg-intake-coverage-followup-20260912/tg-intake-synthetic-acceptance`: exercise the synthetic
  lifecycle in isolation, including the artifact-required closure refusal.

Neither follow-up authorizes file moves/deletions or synthetic writes to live operator intake.

## Verification

Read-only review of the cited design documents, plans, task-chain JSON, and dated coordination
audit. The follow-up chain records these as open work; this review does not claim either acceptance
gate or semantic audit is already verified.
