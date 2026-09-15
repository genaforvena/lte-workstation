# Fail2ban repeat-offender triage — `152.32.254.222`

Task: `fail2ban-repeat-offender-20260914/triage-repeat-offender`  
Owner: `health`  
Scope: read-only; no firewall or jail state changed.

## Evidence

- The alert source is phaedra's `~/.mesh/fail2ban-watch.log`; the exact repeat row is
  `2026-09-14T02:50:02Z REPEAT ip=152.32.254.222 count=3`.
- An independent SSH read of phaedra at triage time (`2026-09-15T19:56Z`) returned
  `fail2ban-client status sshd` successfully: currently failed `2`, total failed `3959`,
  currently banned `0`, total banned `394`, and an empty banned-IP list.
- The watch log has no later repeat row for `152.32.254.222` after the alert. Combined with
  its absence from the current banned list, the three alert-cycle bans have expired normally
  and the IP is not currently an access risk.
- The existing durable cross-IP receipt
  `docs/task-receipts/fail2ban-triage-20260915.md` independently records the same alert and
  current jail result; this receipt preserves the exact owner-scoped verification and SSH
  command outcome.

## Disposition

DONE: alert was a real three-ban repeat-offender event, but the offender is no longer banned
and has not re-offended in the watch tape. The fail2ban jail is functioning and continues to
ban other addresses. No follow-up or firewall/jail change is warranted.

## Verification

```text
timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=5 phaedra \
  'tail -80 ~/.mesh/fail2ban-watch.log; fail2ban-client status sshd'
```

Result: SSH exit 0; alert row present; current banned count 0; banned list empty.
