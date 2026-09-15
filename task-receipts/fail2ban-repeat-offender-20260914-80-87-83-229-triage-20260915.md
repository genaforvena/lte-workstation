# Fail2ban repeat-offender triage — `80.87.83.229`

Task: `fail2ban-repeat-offender-20260914-80-87-83-229/triage-repeat-offender`  
Owner: `health`  
Scope: read-only; no firewall or jail state changed.

## Evidence

- Independent SSH read of phaedra found the exact watch row:
  `2026-09-14T21:05:02Z REPEAT ip=80.87.83.229 count=3`.
- The same read ran `fail2ban-client status sshd` successfully at triage time
  (`2026-09-15T~20:00Z`): currently failed `2`, total failed `3960`, currently banned `0`,
  total banned `394`, and an empty banned-IP list.
- There is no later repeat row for `80.87.83.229` in the watch tape, and the IP is absent
  from the current banned list. The three alert-cycle bans expired normally; no current
  access risk remains for this address.

## Disposition

DONE: real three-ban repeat-offender alert, now resolved by normal expiry with no re-offense.
The sshd jail remains functioning and no firewall or jail change is warranted. New repeat
alerts remain covered by the existing `mesh-fail2ban-watch` lane.

## Verification

```text
timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=5 phaedra \
  'grep -n "80.87.83.229" ~/.mesh/fail2ban-watch.log; fail2ban-client status sshd'
```

Result: SSH exit 0; exact alert row present; current banned count 0; banned list empty.
