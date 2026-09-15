# Health triage: genome-targeted chat delivery age expiry

Date: 2026-09-12  
Task: `health-warning/af21f1e0fda7afd2da71/triage`

The reported witness FYI (`076ed18f84871847`) was addressed to `genome` at
19:36:59Z. The deliverer emitted its terminal `age-expiry` at 19:52:07Z, age
905s against the 900s limit. The adjacent TG FYI (`c6187d80fa545362`), sent at
19:36:25Z, expired in the same pass at age 939s. Neither has an ACK in the
chat log. A prior genome-targeted witness message (`629dfb8e6d335e28`) also
expired at 19:43:14Z with zero recorded successful handoffs.

In `scripts/mesh-chat-deliver`, `attempts` increments only when `mesh-tell`
returns zero. Its stdout and stderr are discarded, and it skips the call when
`mind_idle(target)` is false. Thus `attempts:0` means no successful handoff was
recorded; available evidence cannot distinguish an unavailable/busy pane from
a failed `mesh-tell` call. The intended queue-stall FYIs are therefore not
confirmed delivered, and the precise cause is a known visibility gap in the
current delivery evidence.

Evidence:

- `/home/mesh-home/.mesh/chat.log`, lines 57920 and 57924: original FYIs.
- `/home/mesh-home/.mesh/chat.log`, lines 57965-57966: terminal failure notices.
- `/home/mesh-home/.mesh/chat-deliver.log`, 19:43 and 19:52 entries: zero-success
  terminal outcomes for genome-targeted messages.
- `scripts/mesh-chat-deliver`, `mind_idle` and `one_pass`: idle gate, suppressed
  `mesh-tell` output, and successful-return attempt accounting.

Disposition: investigated and recorded as historical age-expiry with an
unresolved delivery cause. No delivery policy or substrate change was made.
