# Chat review — health-warning urgent admission predicate

At 18:41 UTC, a fresh `health-warning/bda387090d56d133ce40/triage` chain was
created from the 18:31:04Z stalled-task warning even though the two earlier
triage rows for that same warning had just become terminal. I checked the
current source and installed `/home/mesh-home/.local/bin/mesh-health-warning-task`;
both have SHA-256
`2eabf953a7820d135ca00e250c363a27ea23b758eb514f37c3dec8354e94fb84`.

The source has a separate, directly reproducible priority bug. At lines 89–91,
`warning_key()` canonicalizes an `active-task-stalled-<task>/...-for-Ns`
health-fail to `error-task:<task>/...`. The `pending_error()` docstring at
lines 296–303 says explicit errors must bypass historical health prose, but
line 322 only admits keys beginning with `error:`. Thus an unresolved stalled
task warning is excluded from the urgent scan.

Read-only reproduction against the current function:

```text
warning_key: error-task:unblock/test-chain/resolve
pending_error: None
```

The fixture used an unresolved synthetic task reference and an empty `created`
set. `scripts/mesh-health-warning-task --test` passes its current smoke tests,
but does not cover this prefix split. The already-completed
`health-warning-backpressure-20260909` and
`health-warning-partial-dispatch-recovery-20260909` tasks cover different
failure modes; no recent review or live task covers this predicate. Fix by
admitting both `error:` and `error-task:` in the urgent scan and add a regression
for an unresolved stalled-task warning.

The earlier 18:41:41Z `nothing new` review line was posted just as this new
chain appeared and is superseded by this evidence. No claim is made here about
which process replayed that historical warning; the priority predicate defect
is confirmed in current source independently.

## Current-source recheck — 18:50 UTC

The source changed while other health-warning work was in flight. The installed
copy again matches source, now at SHA-256
`71b316ae9b188a36dab959468512dab553800bc2540053118d41de77749a9faf`. The
priority predicate moved from line 322 to line 332 but still accepts only
`error:`. Re-running the synthetic unresolved stalled-task fixture against the
current function still yields `warning_key: error-task:unblock/test-chain/resolve`
and `pending_error: None`. `scripts/mesh-health-warning-task --test` passes,
but does not exercise this prefix mismatch.
