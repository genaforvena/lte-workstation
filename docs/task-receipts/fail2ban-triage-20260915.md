# fail2ban repeat-offender triage — 2026-09-15 (read-only)

Closes (structured ledger, not prose):
- `fail2ban-repeat-offender-20260914/triage-repeat-offender` (ip 152.32.254.222)
- `fail2ban-repeat-offender-20260914-80-87-83-229/triage-repeat-offender` (ip 80.87.83.229)

## Evidence (all read-only, nothing changed)

Alert source `root@38.49.216.141:/root/.mesh/fail2ban-watch.log` (phaedra-direct ssh):
- `2026-09-14T02:50:02Z REPEAT ip=152.32.254.222 count=3`
- `2026-09-14T21:05:02Z REPEAT ip=80.87.83.229 count=3`

Each IP hit three sshd bans in six hours at alert time — that is the watch's
repeat-offender definition firing as designed, not a new failure mode.

Live jail state `fail2ban-client status sshd` (2026-09-15T~19:5xZ, same session):
- Currently failed: 1 · Total failed: 3957
- Currently banned: 1 · Total banned: 394
- Banned IP list: `147.50.231.135` only

## Verdict

Neither triaged IP is currently banned; both bans expired through the normal
ban/expiry cycle and neither IP has re-offended since its alert row. No current
access risk remains. The jail is functioning (banning others since). No firewall
or jail state was touched — read-only triage per the task constraints.

Disposition: DONE for both chains. No follow-up task needed; repeat alerts for
new IPs continue through the existing `mesh-fail2ban-watch` lane.
