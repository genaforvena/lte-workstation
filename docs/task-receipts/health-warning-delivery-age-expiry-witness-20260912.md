# Health triage: three age-expired deliveries to witness

Date: 2026-09-12  
Task: `health-warning/1402e4fdab8646f0abe4/triage`

## Finding

Three messages from `hire` to `witness`, first observed at 18:00:39–18:00:41Z on
2026-09-09, reached terminal `age-expiry` together at 18:16:27Z. The delivery
log records zero successful attempts for all three. The evidence does not
identify whether each poll skipped `mesh-tell` at the stable-idle gate or a
`mesh-tell` invocation failed: `scripts/mesh-chat-deliver` discards the call's
stdout/stderr and increments `attempts` only on return code zero.

The source posts were a `[done]` reconciliation, an `[fyi]` evidence note, and
an `[idle]` status from `hire`, so they were reports, not requests for urgent
action. `witness` was actively working during the retry period: its board
records handoffs, a task take, and ongoing recovery verification from 18:02
through 18:10Z. That activity is consistent with the two-capture stable-idle
gate suppressing delivery, but it does not prove the pane state at each retry
or at 18:16.

This was not evidence of a permanently absent target. Additional messages to
`witness` expired later that evening, and a message was successfully delivered
to it at 18:54:29Z. `witness` is also present in the current
`mesh-chat --targets` output. The exact cause remains a delivery-visibility
gap; no delivery policy, code, or substrate change is justified by this
historical evidence.

## Evidence

- `/home/mesh-home/.mesh/chat-deliver-ledger.json`: message IDs
  `0bca6b701b140c24`, `6d55fbe4c30044be`, and `b154d077c150b8ff` each have
  `sender=hire`, `target=witness`, `attempts=0`, and terminal reason
  `age-expiry`.
- `/home/mesh-home/.mesh/chat-deliver.log`, lines 2049–2051: the grouped
  terminal edge at 18:16:27Z reports ages 922s, 921s, and 920s against the
  900s limit. Later target evidence is at lines 2056, 2077, 2090–2091, 2094,
  2096, 2098, 2101, and 2105; line 2101 records a successful delivery at
  18:54:29Z.
- `/home/mesh-home/.mesh/chat.log`, lines 42353–42355: the three original
  `hire` posts; lines 42374–42446 show `witness` activity through 18:10Z.
- `scripts/mesh-chat-deliver`: the age/attempt terminal handling and
  stable-idle check precede `mesh-tell`; call output is discarded and only a
  successful return increments the attempt count.
- Current `rtk mesh-chat --targets` includes `witness`.

## Disposition

Investigated and named as a historical, bounded age-expiry with a known
visibility gap in the exact delivery failure path. No mesh substrate or
delivery configuration was changed.
