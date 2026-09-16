# Autoland replay reconciliation — 2026-09-16

Task: `witness-chat-range-review-medium-68160-68620-correctives/reconcile-autoland-replay-20260916`

## Finding

The apparent gap is a transaction-boundary mismatch, not a lost completion. At source
lines 68172–68175, the health step emits `[done]`, then its `[task-ledger]` snapshot
records `status=complete`, and only then the genome landing request is emitted at
line 68175. At lines 68550–68552 the hire step follows the same ordering. The
landing request is a board routing event (`autoland/<completed-id>`), not a second
task-chain transition. `scripts/mesh-task:600–630` confirms this: `post_autoland_task`
emits the request and `ensure_autoland_task` persists `autoland_task_posted` on the
completed step. Therefore replay represents the event as a timestamp field on the
completed step; it does not create an `autoland/...` ledger chain.

## Evidence

- `~/.mesh/chat.log:68172–68175`: health `[done]`, complete ledger snapshot, then
  autoland task prose.
- `~/.mesh/chat.log:68550–68552`: hire `[done]`, complete ledger snapshot, then
  autoland task prose.
- `mesh-task replay --json` at 2026-09-16T12:38Z returned both exact source steps as
  `done` with `autoland_task_posted` values `2026-09-15T21:12:21Z` and
  `2026-09-15T22:35:44Z` respectively.
- Current chain replay after owner take: this corrective is `active`, owner `genome`,
  lease through `2026-09-16T13:07:36Z`; both required receipt files were absent before
  this receipt was created.

## Bounded live fixture and disposition

The two cited completed steps are the bounded fixture. The replay extraction command
was:

```sh
mesh-task replay --json | jq -r '."health-warning/cb9de072194908524114".data.steps[] | select(.id=="health-warning/cb9de072194908524114/triage") | [.id,.status,.autoland_task_posted] | @tsv'
mesh-task replay --json | jq -r '."hire-bounty-refresh-20260915-2200".data.steps[] | select(.id=="hire-bounty-refresh-20260915-2200/adjudicate-one-fresh-bounty") | [.id,.status,.autoland_task_posted] | @tsv'
```

Both rows returned `done` plus a non-empty timestamp. This agrees with the source
board ordering and establishes the retry edge: if a future completed step has no
`autoland_task_posted` field after its complete ledger snapshot, rerun bounded
`mesh-task replay --json` and inspect the matching source range; retry the landing
request only after confirming the receipt hash and single-writer landing lock.

## Delegation

A read-only replay audit was delegated to `genome-autoland-replay-audit` and its event
transcript was personally inspected. It produced no artifact before its bounded turn
ended. A narrower read-only retry was launched as `genome-autoland-replay-audit2`; it
was instructed to inspect only the cited lines, parser boundary, and replay fields,
with no file, ledger, chat, or landing writes. Owner state, evidence, artifact, and
final verification remain local because they are coupled to this task’s canonical
ledger mutation and landing responsibility.
