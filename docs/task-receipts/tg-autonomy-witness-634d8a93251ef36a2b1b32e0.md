# Operator autonomy witness receipt

- Source ask: `ask:tg-634d8a93251ef36a2b1b32e0`
- Date: 2026-09-16
- Scope: operator-authorized autonomous work on all declared mesh nodes, explicitly including Note3 and hh.
- Durable artifact: `charter/witness.md`, with the live witness goal line and an explicit rule to route mesh-internal blockers to minds for complete machine-side action.
- Delivery: operator text sent at 2026-09-16T03:59Z with `mesh-tg`; the command returned `sent to operator TG` (the transport receipt), and the autonomy instruction was relayed to witness at 2026-09-16T04:00:55Z in `/home/mesh-home/.mesh/chat.log`.
- Verification: `mesh-handoff --goal witness --oneline` must render the autonomy-aware goal; inspect the charter text and board tail after relay.

The rule preserves evidence, credential/privacy boundaries, substrate single-writer discipline,
and typed external blockers. It removes approval-seeking for work already inside the mesh's
declared node scope.
