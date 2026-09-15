# Triage historical mesh-heavy scope-start failure

Task: `health-warning/c6d3b3c34895c7ec558d/triage`  
Source: `mesh-journal-watch` FYI at 2026-09-13T00:30:02Z

The alert reports failure to start
`mesh-heavy-959407-1b419bcf.scope` for a 48 MiB Python allocation probe.
The source event is retained in boot `76234e1e4abc41a18095827b8070f37f` at
00:25:27Z. Systemd logged that process 962139 no longer existed when it tried
to move it into the requested user-service cgroup, then reported `Failed to
add PIDs to scope's control group: No such process` and result `resources`.
This identifies a short-lived-process/scope-start race; it does not show a
memory-cgroup OOM or prove why the process exited before attachment.

That boot ended at 03:55Z; the current boot began at 11:35Z on Sep 13. A fresh
`mesh-journal-watch --once` at about 20:40Z shows no recurrence of the same
48 MiB probe signature. Its current-boot journal contains three separate
`mesh-heavy` scope-start failures for `/usr/bin/sleep 1` at Sep 13 19:05Z,
Sep 14 03:19Z, and 04:05Z. Each records `No such process` during cgroup
attachment and result `resources`; the first also records `Permission denied`
when adding PIDs. These repeated short-command failures point to a scope
launcher timing/attachment weakness, but do not establish a broad host memory
failure. The most recent matching current-boot event is over sixteen hours old.

Disposition: the original warning was valid for its then-current boot and is
now historical. The underlying fast-process scope-start race is visible in
three later events, with no safe health-only repair justified by this
triage. Do not classify it as an OOM. No service, memory, or privilege state
was changed.

## Verification

- `rtk journalctl -b -1 --since '2026-09-13 00:25:00 UTC' --until
  '2026-09-13 00:26:00 UTC'` matched the exact original scope failure and
  systemd's `No such process` / `resources` messages.
- `rtk journalctl --list-boots` verified the source event is in the prior boot
  and the current boot began at 2026-09-13 11:35:50Z.
- `rtk mesh-journal-watch --once` completed read-only and returned normalized
  current-boot signatures.
- The current-boot journal entries for the three one-second sleep scopes were
  read at 19:05Z, 03:19Z, and 04:05Z; each shows a cgroup-attachment failure.
