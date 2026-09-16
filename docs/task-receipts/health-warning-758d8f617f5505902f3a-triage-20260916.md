# Health warning triage: adint mind-holding / UNATTRIBUTABLE

- Task: `health-warning/758d8f617f5505902f3a/triage`
- Source: `~/.mesh/chat.log:72038`, `2026-09-16T05:19:06Z`
- Warning: `channel-keepalive@mesh-home` reported that `mesh-home:adint` held
  `› /clear` for 10 minutes with no matching `mesh-tell` delivery and classified
  it `UNATTRIBUTABLE`.

## Evidence

1. The keepalive implementation at `scripts/mesh-channel-keepalive:724-757`
   deliberately returns `UNATTRIBUTABLE` when the WAL has no usable payload or
   cannot answer the attribution query. Its actuator at `:860-872` leaves the
   composer untouched and emits `[mind-holding]`; it does not submit keys or
   relaunch the mind. This is the intended fail-closed behavior for an
   attribution blind spot.
2. The warning left the durable marker
   `~/.mesh/.strand-held-adint` at `2026-09-16T05:19:06Z`; the marker is empty,
   so it records the held-warning arm without preserving private composer text.
3. Fresh independent recheck at `2026-09-16T06:48Z`: the live adint tmux pane
   exists at `mesh-home:12.1`, is actively processing, and
   `mesh-mind-state adint` returned `WORKING`. No later `[mind-holding]` or
   `[mind-stranded]` entry for adint appears after source line 72038.
4. The live `tell-wal.log` is present and receiving current rows, but the
   original warning's classification remains `UNATTRIBUTABLE`; no evidence
   justifies replaying `› /clear` or touching the operator's composer.

## Disposition

Resolved as a stale, known instrumentation blindness: the warning was a
fail-closed attribution result, not evidence that adint was idle or stranded.
The mind is currently working and the composer was preserved. No substrate or
operator state was changed.

Retry edge: if a new `[mind-holding]` for adint is emitted and the pane remains
`IDLE`/`WEDGED-INPUT`, run a fresh `mesh-dash --once adint`, inspect the current
WAL and pane, and open a new exact warning task; do not reuse this settled claim.

Delegation: none; this was a tightly coupled, read-only health triage and the
claim owner retained the required board/ledger voice. Artifact personally
inspected before settlement.
