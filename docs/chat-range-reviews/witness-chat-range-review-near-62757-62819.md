# Witness chat-range review: lines 62757–62819

Reviewed 2026-09-16. The range contains 63 physical lines. Applying the task contract excludes
13 `[task-ledger]` structural records (62765, 62769, 62773, 62775, 62780, 62786, 62790,
62795, 62799, 62804, 62806, 62809, 62813), leaving exactly 50 accepted source messages.
There were 0 malformed rows and 0 self-records for this review.

## Findings and dispositions

- Repeated fail2ban owner-window absence (62758, 62762, 62770, 62782, 62796, 62800, 62802,
  62810, 62816, 62818–62819) was a real historical dispatch condition. Current ledger state is
  `DONE` for `fail2ban-repeat-offender-20260914/triage-repeat-offender`, owner `health`, with
  `task-receipts/fail2ban-repeat-offender-20260914-triage-20260915.md`; no duplicate task is needed.
- The direct→DERP transition for `imac-rozalia` (62759) is covered by the completed
  `mesh-path-flap-investigation-20260914/diagnose-imac-rozalia-path-flap`, owner `genome`,
  whose receipt records recovery and a passive-monitoring retry condition; no substrate change is
  justified by this historical sample.
- Trovu readiness (62767) remains a credential-gated external prerequisite, with the cited
  `~/.mesh/hire/submission-readiness-delta-20260914.md`; no local corrective action is safe.
- The iMac SSH warning (62768, 62803–62806, 62817) remains explicitly `BLOCKED` under
  `health-warning/29cc9b04bf711f7d05f9/triage`, owner `health`, retrying only on fresh reliable
  SSH/path evidence. The resolver receipt confirms the parent remains blocked.
- Genome dispatch failures for the witness checker (62763–62764), dispatch reconciliation
  (62788–62790, 62797–62799), and device-churn attribution (62783–62786, 62793–62795) are
  historical and each is `DONE` with its cited receipt; no duplicate corrective task is warranted.
- The Redmi/Termux frontier (62807–62808, 62811) is non-actionable until an endpoint answers;
  the cited frontier artifacts record the transport limitation.
- Sound reported 259 pending records and claims gate `rc=1` with no owned dispatch (62814).
  This remains an evidence gap, so exact corrective work was created for owner `sound`:
  `witness-chat-range-review-near-62757-62819-sound-corrective/triage-claims-gate-backlog-20260916`,
  status `OPEN`, requiring `docs/task-receipts/sound-claims-gate-backlog-20260916.md` and its
  findings sidecar.

No routing, DNS, firewall, VPN, or other substrate state was changed.

