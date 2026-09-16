# Discover frontier sweep — 2026-09-16

## Verdict

No new reachable sense or actuator was proven in this turn. The local frontier is
dry for the bounded candidates inspected; each candidate is already implemented
or catalogued and was rejected as duplicate rather than re-filed.

## Evidence swept

- Live pane: `mesh-dash --once discover` at 2026-09-16T06:24:56Z. The four
  previously untouched Redmi verbs (`termux-backup`, `termux-media-scan`,
  `termux-saf-ls`, `termux-storage-get`) are already represented by active
  handoff/probe work, so this turn did not duplicate them.
- `/proc/net/softnet_stat`: a real read returned 16 CPU rows; the mesh already
  owns this axis in `scripts/mesh-net-drop` (the script explicitly parses
  `softnet_stat`). Rejected as prior art.
- `/proc/softirqs`: a real read returned the live per-CPU vectors, including
  `NET_RX`; `~/.mesh/knowledge/capability-softirq-load-20260703.md` already
  records this capability and the intended `mesh-softirq` direction. Rejected
  as prior art.
- `rg` sweep across `scripts/`, `docs/`, and `~/.mesh/knowledge/` found no
  unrecorded adjacent kernel/network surface worth probing safely in this
  bounded turn.

## Acceptance / material price

There is no new consumer to price because both candidate materials failed the
novelty predicate before a new capability could be proposed. Re-probing either
would have a 0% novelty yield against the repository's acceptance rule.

## Next edge

Wait for a new frontier prompt or for the existing Redmi handoff artifacts to
settle; do not re-file these candidates. The next discover turn should begin
with `mesh-dash --once discover` and the dispatch queue.
