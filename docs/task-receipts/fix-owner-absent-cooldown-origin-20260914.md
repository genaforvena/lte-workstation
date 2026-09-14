# Owner-absent cooldown origin fix

Verified 2026-09-14 on `mesh-home` for
`chat-review-owner-absent-live-dedup-recurrence-20260914/fix-owner-absent-cooldown-origin`.

## Change

`scripts/mesh-mind-control::_owner_absent_announce_once` now compacts the announcement ledger to
one newest numeric timestamp per signature while holding its existing separate `.lock` flock, then
uses that timestamp as the cooldown origin. The atomic state replacement preserves the existing
state file mode. Explicit-owner hold and routing paths were not changed. A deterministic self-test
fixture seeds an expired first row and a newer expired row, then proves that the first call posts
once, the immediate repeat is trace-only, and only one signature row remains.

## Verification

- Before implementation, `scripts/mesh-mind-control --test` failed the new regression's three
  assertions: it posted twice, did not trace-suppress the repeat, and retained duplicate rows.
- After implementation, `scripts/mesh-mind-control --test` exited 0. The installed
  `~/.local/bin/mesh-mind-control --test` also exited 0 with the same full self-test summary.
- `mesh-land` landed and deployed the scoped script as commit `dd2b1d03` with subject
  `Use newest owner-absent cooldown timestamp`.
- Repository and installed-copy SHA-256 both equal
  `b521b4aa362713099bfcf927802b06520b925db2048cdcace9503fc361887c79`.
- Live board evidence showed owner-absent FYIs through `2026-09-14T15:12:07Z`, immediately before
  deploy at `15:12:13Z`. After deploy, the board had no matching FYI; `~/.mesh/traces.log` recorded
  trace-only suppressions at `15:12:27Z` and `15:12:44Z` for
  `fail2ban-repeat-offender-20260914/triage-repeat-offender`.
- The live `~/.mesh/.owner-absent-announced` ledger compacted from 654 rows to 55 rows on the next
  real retry, had zero duplicate signatures, and retained mode `664`.

No unresolved implementation or verification obligations remain.
