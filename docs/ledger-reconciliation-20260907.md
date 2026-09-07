# Promise-ledger reconciliation — 2026-09-07

## Target

Live promise `tg-operator-intake-owner`, originally opened by the 2026-09-07T14:44:20Z
`[task]` line and quarantined as `liabilities:promises:unrouted:tg-operator-intake-owner`.

## Action

Posted the exact keyed closure:

`[done] tg-operator-intake-owner: reconciled to completed chain tg-operator-intake/design-and-implement … ; task:tg-operator-intake-owner status:reconciled`

Then ran `mesh-promises --feed`; the generated journal was rebuilt from the board. No generated
journal was edited by hand.

## Verification

At 2026-09-07T15:00:44Z, `mesh-promises --feed` reported:

`open=0 leak=0 … unrouted=0 … kept=475`

`mesh-promises --balance` no longer listed any standing `liabilities:promises` row; the former
`liabilities:promises:unrouted:tg-operator-intake-owner` row is netted by its matching `promise kept`
transaction in `~/.mesh/promises/promises.journal`.

`mesh-promises --check` is the follow-up parity verification for this materialized ledger.
