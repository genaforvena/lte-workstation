# Health warning triage: genome delivery age expiry (2026-09-13)

Investigated the live warning `health-warning/e40038be09cc5b171be1/triage` for
message `1e9e490a3eb985dc`, plus the immediately preceding open triage
`health-warning/29679e9968c6cff47d5b/triage` for message `60c7578acd32d20c`.

Both are real terminal delivery failures, not stale warning text. The live
ledger records `status=failed`, `terminal_reason=age-expiry`, `attempts=0`, and
`failure_emitted=true` for each. The first message was first seen at
`2026-09-13T12:02:14Z` and failed at `12:18:08Z` at age 949s; the second was
first seen at `12:06:17Z` and failed at `12:22:06Z` at age 947s. Both were
`witness` FYIs addressed to `genome`; their source bodies are in
`~/.mesh/chat.log` at those first-seen times. No successful-delivery log entry
exists for either ID.

Current evidence is consistent with the recipient remaining busy: `genome` is
a valid chat target, its tmux pane is live and currently running a Codex task,
and the deliverer's selected pane capture changed across a 3-second interval.
This does not prove what happened throughout each 15-minute age window.

The deployed deliverer and repository source have identical SHA-256
`dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae`, and the
live crontab runs it every minute. Current code uses a 900-second terminal age
limit and checks age before the idle-pane/send path. A successful `mesh-tell`
increments `attempts`; failed calls and rejected busy-pane checks do not. Thus
`attempts=0` cannot distinguish “never passed idle” from a failed `mesh-tell`
call (stderr is suppressed and no failure-attempt record is written). That is
the remaining diagnostic blindness; the warning correctly reports that these
messages were not delivered before expiry. The FYIs are historical and were not
manually retried.

No source, deployment, or substrate change was indicated by this triage. The
delivery-failed rows and ledger entries remain as the terminal evidence.
