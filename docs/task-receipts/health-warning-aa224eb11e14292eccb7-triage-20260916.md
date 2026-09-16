# Health warning triage: senses delivery age expiry

Task: `health-warning/aa224eb11e14292eccb7/triage`
Checked: 2026-09-16T08:33Z UTC on `mesh-home`

## Finding

The Telegram-originated message `24f4b46d1ed098db` for target `senses` expired in
the delivery queue before any send attempt. The canonical delivery ledger records
`first_seen=2026-09-16T07:07:36Z`, `failed_at=2026-09-16T07:23:04Z`,
`attempts=0`, `failure_window=5965144`, `status=failed`, and
`terminal_reason=age-expiry`. The delivery log independently records age `928s`
against the `900s` limit at failure.

## Conclusion and boundary

This alarm is an age-expiry / stale-consumer event: the message remained pending
longer than the delivery SLA and was never handed to transport. The evidence does
not identify why the senses consumer failed to consume it, so no narrower cause is
claimed. A fresh `mesh-dash --once senses` produced no visible output in this pane,
which is recorded as unavailable evidence rather than a health verdict.

No routing, DNS, firewall, VPN, service, or other substrate state was changed.
