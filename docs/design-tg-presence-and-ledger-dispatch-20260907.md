# TG presence and Ledger dispatch staffing policy

Version: `2026-09-09.2`  
Owner: `discover`  
Scope: the read-only census used before a non-TG task is offered to a worker.

## Contract

The census emits one record for every observed window. Each record has these fields:

```text
window role live protected open_promises open_holds active_promises active_holds
leaked_promises leaked_holds eligible reason observed_at
```

`observed_at` is one UTC RFC-3339 timestamp captured for the census run. It is not the
window's last activity time and must not be inferred from an idle-looking pane.

The census consumes three independent inputs:

1. `tmux list-windows` proves that the window is live.
2. The window charter supplies its role and protected status.
3. `mesh-promises --json` and `mesh-task status` supply open promises and holds. Total open
   counts remain visible, while obligations marked `leaked` are separated from active ownership.
   Leaks remain visible and require reconciliation, but do not permanently starve an otherwise
   idle mind from receiving new work.

If any required input cannot be read or parsed, the census fails closed: it exits non-zero
and produces no eligible worker. A missing row is not an idle row.

## Eligibility predicate

A row is `eligible=true` only when all of the following are true:

```text
live
AND window NOT IN {tg, tg-roz}
AND human-owned=false
AND protected=false
AND active_holds=0
AND active_promises=0
```

The first failed condition supplies the stable `reason` value. Rejected reasons are:
`not-live`, `communication-window`, `human-owned`, `protected-role-or-substrate`,
`open-hold`, and `already-owned-work`. Positive reasons are `eligible` and
`eligible-with-leaks` (idle, but with leaked obligations still visible).

`tg` and `tg-roz` remain communication windows even if their panes look free, their role
label is changed, or they have no Ledger liabilities. Human-owned work is never a staffing
candidate. Protected roles include substrate/single-writer lanes and any row explicitly
marked protected by its charter. An active hold or active promise means the window is already
carrying work and is not reassigned by inference. Leaked obligations are reported, but are not
current ownership for this admission decision; the leak-repair path remains responsible for them.

The policy is a proposal boundary, not an assignment. A later dispatcher must still emit an
explicit owner-tagged task and wait for the owner's visible receipt; this artifact does not
wire dispatch or mutate the Ledger.

## Frozen fixture and expected census

The focused fixture contains five rows:

| window | role | live | protected | open promises | open holds | human-owned | expected |
|---|---|---:|---:|---:|---:|---:|---|
| `tg` | communication | yes | no | 0 | 0 | no | reject: `communication-window` |
| `haunt` | research | yes | no | 0 | 0 | no | eligible |
| `genome` | substrate | yes | yes | 1 | 0 | no | reject: `protected-role-or-substrate` |
| `witness` | witness | no | no | 0 | 0 | no | reject: `not-live` |
| `human` | operator | yes | no | 1 | 0 | yes | reject: `human-owned` |

The expected eligible set is exactly `{haunt}`. The fixture is evaluated by
`tests/test-mesh-tg-dispatch-policy.sh`; it does not read or write live tmux, the live board,
or the Ledger.

## Mutation guard

The test mutates the `tg` row to appear free (`role=research`, no promises, no holds). The
expected result remains rejection with `communication-window`. If that mutation becomes
eligible, the policy has lost the operator-channel exclusion and the focused test must fail.

The same fail-closed rule applies to a missing census or Ledger input: an unavailable source
cannot be converted into a plausible free worker.
