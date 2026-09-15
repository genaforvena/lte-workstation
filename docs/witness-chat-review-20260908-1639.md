# Witness chat review — 2026-09-08 16:39Z

## Finding

The new `scripts/mesh-chaos-consumer` is described by its own lines 4–7 as an
explicit, on-demand acceptance path, but it has no `# orphan-ok:` declaration.
The current file begins with that description at lines 1–8 and contains no
orphan declaration. It is also absent from `~/.mesh/reflexes.cron`, so it is
not a scheduled reflex. `mesh-land` reported at 16:38:54Z that the landed
unit was “unwired” and would surface as a doctor orphan. This is a real
declaration/wiring mismatch, not a request to cron-wire the consumer.

## Action

Add a truthful `# orphan-ok:` on-demand declaration to
`scripts/mesh-chaos-consumer`, deploy it byte-identically, and run the narrow
doctor/orphan and consumer checks. Owner: `mesh-chaos-consumer/genome`.

## Checks performed

- Read current source with line numbers: `scripts/mesh-chaos-consumer:1–8`.
- Confirmed no cron/units caller with `rg`; no `mesh-chaos-consumer` entry is
  present in `~/.mesh/reflexes.cron`.
- Confirmed the latest board landing line at
  `2026-09-08T16:38:54Z` names the missing declaration and predicted orphan.
- Searched recent `[chat-review]` lines and the task ledger; no existing
  review/task for this exact consumer declaration gap was found.
