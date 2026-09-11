# Idle-turn correction pre-landing review — 2026-09-11

Verdict: **still failing the live-loop expiry case**

The correction revision added this condition to `task_aware_gate_decision`:

```bash
if [ -z "$candidate" ] && [ "$prev" = "$cur" ]; then
  echo HOLD:no-eligible
fi
```

That condition is not a live-loop proof. The caller enters the decision only when the pane signature
or candidate signature changed. With no candidate and unchanged task eligibility, live entry therefore
requires the pane signature to have changed, so `prev != cur`. If both are unchanged, the loop skips the
gate entirely. The focused test's same-frame invocation reaches a branch the daemon does not reach for
the observed periodic board-tail churn.

Required regression shape:

1. Expired expectation, no candidate, and a pane delta fully matching the stored prediction must hold
   without a mind turn.
2. The same expired expectation with an unpredicted real pane line must wake.
3. Empty-to-eligible task transition must wake; eligible-to-empty after take must not buy a follow-up
   owner turn unless the pane delta is independently unpredicted.

This finding was routed to the exact owner at `2026-09-11T13:59:54Z`. The corrective task remained
QUEUED rather than owner-taken at the observation cutoff, so no completion claim is valid yet.
