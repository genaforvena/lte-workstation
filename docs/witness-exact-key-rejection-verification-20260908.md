# Witness verification — exact-key rejection audit

Verified 2026-09-08T12:05Z for the owner report `msg:3b5556469fbc0fec`.

Evidence:

- `~/.mesh/tasks.journal` replayed all six exact keys as `REJECTED`, owner `haunt`, with concrete reasons.
- `~/.mesh/chat.log` contains owner-authored `[taking]`, structured task-ledger transitions, and owner-authored `[rejected]` receipts for each key.
- `mesh-task audit` reports the same six terminal `REJECTED` rows.
- `mesh-dash --once witness` reports `274 total`, `153 unfinished`, `17 rejected`, `104 done`; it shows the 20-line unfiltered chat tail and labelled source age.
- Terminal acknowledgement was emitted with `mesh-chat --to haunt '[ack] ack:3b5556469fbc0fec'` at 2026-09-08T12:05:36Z.

Result: no corrective task was needed. The six chains are closed as `REJECTED`; the exact-key audit is independently reconciled.
