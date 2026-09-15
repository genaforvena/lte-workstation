# Witness health-warning reconciliation — 2026-09-08

## Result

The five exact health-warning triage keys were reconciled against the live
structured ledger and `~/.mesh/chat.log`. Each has an owner-authored
`[taking]` transition by `health@mesh-home`, followed by an owner-authored
`[blocked]` transition with a concrete need and retry edge. No substrate action
was taken.

Keys:

- `health-warning/25a35aa3f04ecad1655e/triage` — external event:
  `operator-revival-decision`
- `health-warning/0ac2476a343fdde6c790/triage` — dependency:
  `roll-call-delta`
- `health-warning/39b152384383b0fa73e9/triage` — external event:
  `operator-transcriber-revival-decision`
- `health-warning/10494c92497316a2185c/triage` — external event:
  `operator-wake-reflex-revival-decision`
- `health-warning/25d17bc908dbe3b61fe4/triage` — dependency:
  `new-health-delta-or-owner`

## Verification

- `~/.mesh/tasks.journal`: replay `PASS`, 274 rows, 152 unfinished, 17
  rejected, 105 done.
- `mesh-task audit`: exit code 0.
- `mesh-dash --once witness`: materialized-view age labelled `age=2s`; raw
  source tail labelled `showing 20/37525` and unfiltered.
- Chat evidence: `~/.mesh/chat.log` lines 37382–37399 contain the owner
  transitions and structured blocked records.
- Acknowledgement sent: `ack:a664161ae228665b`.

Next watch condition: on an unpredicted health delta or owner/operator
decision, re-read the exact key's live state and require a fresh artifact-backed
`[done]` (or a new concrete terminal disposition) before treating it as
settled.
