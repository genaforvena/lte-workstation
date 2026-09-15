# Duplicate Haunt dictionary-input resolver dispatches — 2026-09-12

This evidence applies to these adint-owned rows that still label the broader Haunt dictionary
question as missing operator inputs:

- `unblock/adint/dd9fdfc8547d03c0/resolve`
- `unblock/adint/589ec67373ea4f8e/resolve`

The current Haunt row is `unblock/haunt/fd5d75268b44e1cc/resolve`, blocked as
`experiment-contract`. Its frozen manifest and corpus exist; the A08-only result does not prove
BbyWVY dictionary behavior, and the six-case BbyWVY runtime smoke has no dictionary arm. The exact
remaining prerequisite is Haunt's owner-authored choice to narrow the parent claim to A08 while
preserving `INCONCLUSIVE`, or to implement and measure a compatible BbyWVY dictionary arm. Do not
ask the operator to resend inputs and do not use `scripts/bbywvy_test.py` as dictionary evidence.

Evidence: `docs/task-receipts/unblock-adint-19da47a3a387df26-resolve-20260912.md` records the
frozen-input finding and exact scope alternatives; `docs/task-receipts/haunt-dictionary-experiment-
contract-20260912.md` records the current blocker and retry gate. Both rows must have their own
owner-scoped dispatch check exit 0 before settlement against this shared finding. No Haunt-owned
claim or study was changed.
