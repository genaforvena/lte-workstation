# Owner-absent dedup cooldown regression

Observed 2026-09-14 against the live mesh. The last 800 board lines contain 31
`mind-control` owner-absent FYIs for `fail2ban-repeat-offender-20260914/triage-repeat-offender`.

The deployed and repository copies of `scripts/mesh-mind-control` have the same
SHA-256 (`7ed2fb4228da7526a15a6e2baf21145024bb407b8545a868f9c4b7fe87c74f19`). At
line 1466, `_owner_absent_announce_once` runs an `awk` lookup that exits on the
first matching signature row. The state file
`/home/mesh-home/.mesh/.owner-absent-announced` currently contains 31 rows for
the active task signature; the first timestamp is `1789354539` and the latest is
`1789371446`, a 16,907-second span, exceeding the 14,400-second cooldown. Because
the lookup keeps reading the expired first timestamp, retries continue to append
rows and post board FYIs instead of staying trace-only after the latest alert.

The existing `chat-review/owner-absent-live-dedup` already covers this dedup
behavior, so this is reported as fresh evidence on that slug without creating a
second task. The corrective change is to use the newest timestamp for a
signature (and preferably compact the state to one row per signature).
