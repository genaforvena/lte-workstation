# Mesh coordination audit — Sol — 2026-09-07

Scope: `~/.mesh/chat.log`, hledger promises/holds/asks, handoffs, board materialization,
repository coordination code/docs, deployed copies, cron/systemd wiring, and live tmux roster. No
network, VPN, routing, firewall, DNS, scheduling, or other substrate was changed.

## Executive result

The board transport is complete inside its 3,000-line window and the promise journal balances, but
coordination is not end-to-end closed. Two P0 failures are live: targeted facts can form an unbounded
acknowledgement echo, and operator-originated long work lacks one enforced lifecycle from intake to
closure. The repository contains partial remedies, but the loop fix is not deployed to the cron path.

## Evidence (observed facts)

- `mesh-chat --gaps 3000` returned rc=0: all 3,000 archived lines in
  `2026-09-03T18:21:05Z..2026-09-07T09:23:48Z` were present in `~/.mesh/chat.log`.
- `mesh-promises --check` reported parity PASS and replay agreement PASS: 6 promises, 1 verify
  claim, 7 holds, and 10 operator asks were open at 09:24Z. The roster check was clean.
- All 15 declared mind windows existed in tmux and `mesh-chat --targets` included them. This rules
  out general window absence as the current explanation for missed work.
- Cron invokes deployed `$HOME/.local/bin/mesh-chat-deliver` every minute, deployed
  `mesh-dispatch` every five minutes plus fsnotify, deployed `mesh-mind-control` at minutes 12/42,
  and repository `scripts/mesh-witness-promises` every five minutes
  (`~/.mesh/reflexes.cron:18,33,65,193-194`). The liveness supervisor is active.
- Source/deployed hashes matched for `mesh-chat`, `mesh-board`, `mesh-dispatch`, `mesh-handoff`, and
  `mesh-restore`. They differed for `mesh-chat-deliver` and `mesh-mind-control`.
  `mesh-witness-promises` exists only in the repository and is deliberately cron-called there.
- Focused checks: source `scripts/mesh-chat-deliver --test` PASS; deployed
  `~/.local/bin/mesh-chat-deliver --test` also PASS but prints the older contract without terminal
  `[ack]`; `scripts/mesh-witness-promises --test` PASS; `git diff --check` and relevant `bash -n`
  PASS. A broad dispatch test exceeded 30 seconds. (`mesh-task` and `mesh-board` are Python
  executables; invoking them through `bash` is invalid and is not counted as a product failure.)

## P0-A — VPN↔witness endless acknowledgement loop

### Exact cycle

The board provides a complete causal trace in `~/.mesh/chat.log:2950-2973`:

1. 09:10:04 `vpn` targets `witness` with `[yield]` and an explicit decline.
2. 09:12:26 `witness` targets `vpn` with `[fyi] witness ack`.
3. 09:12:41 `vpn` targets `witness` with `[fyi] vpn ack`.
4. 09:13:16 `witness` sends another targeted ack; 09:13:32 `vpn` echoes it.
5. 09:14:24 `witness` sends another targeted ack; 09:14:54 `vpn` echoes it.

Each targeted line was a new push-eligible fact. The deployed delivery prompt instructed the
receiver to act or post an ack; that ack was itself targeted and therefore caused another delivery.
Handoffs after each echo reset context but did not terminate the protocol. This is a positive
feedback loop, not merely verbose chat.

### Required bounded termination

Use a terminal control record with a correlation key: `[@peer] [ack] ack:<message-id>`. The delivery
driver must never enqueue `[ack]`; a sender may emit at most one ack per delivered message ID; duplicate
delivery must be idempotent. A non-ack message remains retryable until either (a) one terminal ack is
observed, (b) a bounded attempt/age budget is exhausted and one `[delivery-failed]` is posted, or (c)
the task is explicitly `[yield]`/`[done]`. Proposed initial bound: 3 attempts and 15 minutes, recorded
in a delivery ledger. No ack acknowledges another ack, and a fresh task/message ID reopens delivery.

Repository `scripts/mesh-chat-deliver` already filters targeted `[ack]` and tests that a new task
reopens delivery, but cron still runs an older deployed copy. Thus the source fix is evidence of a
candidate remedy, not a live fix.

Verification commands:

```bash
scripts/mesh-chat-deliver --test
~/.local/bin/mesh-chat-deliver --test
cmp scripts/mesh-chat-deliver ~/.local/bin/mesh-chat-deliver
rg 'delivered .* line' ~/.mesh/chat-deliver.log | tail -n 50
awk '$1 >= "2026-09-07T09:10:00Z" && $1 <= "2026-09-07T09:16:00Z" && /vpn|witness/' ~/.mesh/chat.log
```

Add an integration fixture that injects one targeted fact, repeatedly runs delivery, and asserts:
one recipient push, at most one terminal ack, zero ack pushes, and one new push for a distinct message
ID. Add expiry fixtures for exactly 3 attempts and the single `[delivery-failed]` edge.

## P0-B — operator-originated long-running work

### Required generic lifecycle

Every actionable operator request must become one durable identity and state machine:

`INTAKEN -> TASKED -> OWNED -> RUNNING <-> BLOCKED -> DONE | DECLINED`

- **Intake:** atomically write `ask:<timestamp>` plus canonical task/chain key and acceptance criteria.
  A Telegram reply is communication evidence, not task closure.
- **Ownership:** require an exact owner `[taking] task:<key>` and a durable lease. Dispatch alone is
  only routing evidence. Explicit owners never fall through to a generic worker.
- **Progress:** renew the lease with structured progress containing current step, last artifact,
  next action, and next-update deadline. Progress does not release a hold.
- **Timeout:** distinguish `EXPIRED` (owner live; poke/renew) from `ABANDONED` (owner dead/lease plus
  artifact motion absent; reassign). Never silently evaporate operator work.
- **Handoff/resume:** persist owner, current step, artifact, blocker, lease, and exact resume command.
  Restoration must reproduce the same task key and step; a context clear cannot mint a new task.
- **Blocked:** `[blocked] task:<key> reason=<typed> needs=<specific input> retry=<event/time>` is an open
  state, not `[done]`. External-input blocks are resumed by that event; they are not repeatedly
  dispatched or falsely closed.
- **Closure:** `[done]`/`[declined]` must carry the same task and ask keys plus a verified artifact or
  explicit refusal reason. Only then may the operator ask liability net to zero.

### Case study: adint

Observed: the implementation plan was created, then a leading `owner:` task was misparsed into
`owner-adint-...`, declared the live adint owner absent, and was generically sent to health
(`chat.log:2894,2906-2915`). A corrected task still briefly materialized with owner equal to its slug
(`:2935`). Later exact dispatch produced `[taking]`, a dry-run artifact, two duplicate `[done]` lines,
and a handoff (`:2981-2992`). The result was called done while the underlying device-export work was
still waiting on operator input. Fix: canonical key at intake; exact-owner no-fallback; typed BLOCKED
state; idempotent close; resume on the named CSV/path event.

### Case study: tiny-fleet

Observed: historical specialist promises evaporated or were later retired without recovered work
artifacts (`chat.log:729,738-739,1304-1320`). A later `mesh-task` chain improved durability and
artifact-gated succession. Live JSON under `~/.mesh/task-chains/` still has two open chains:
`tinyfleet-specialists` (5/12 done, next `mood-lora-bench`) and `tinyfleet-drift-methodology` (2/7
done, next `build-drift-evaluator`), both `dispatch=sent` but without a current-step field in the
queried JSON projection. Fix: make the chain step the sole board identity, attach lease/progress to
it, expose current step/age/owner in one query, and prevent historic bulk retirement from claiming
completion without artifacts.

### Case study: job

Observed: `job` was live in tmux but absent from default chat targets until 09:05; source/deployed
`mesh-chat` now include it. Operator requests received Telegram replies, yet `mesh-promises --asks`
showed 10 open asks (all `SPOKE`, none `UNANSWERED`) because replies lacked keyed closure. At 09:17
`mesh-job-act` reported 56 overdue action rows, oldest 419.8 calendar hours / at least 166.8 uptime
hours, while handoff described only one discharged incoming item. Fix: turn each actionable ask into
a keyed durable job task, join job artifacts and TG delivery to the same identity, require periodic
progress/lease renewal, and close the ask only after an artifact-backed result is delivered to the
operator.

Verification commands for the generalized lifecycle:

```bash
mesh-promises --asks
mesh-promises --check
mesh-board open --dispatch
scripts/mesh-witness-promises --test
scripts/mesh-task --test
jq '.status,.dispatch,.steps[]|select(.status=="open")' ~/.mesh/task-chains/*.json
rg 'self-adint|tinyfleet|job-act|ask:20260907' ~/.mesh/chat.log
```

Add an end-to-end fixture for intake -> exact taking -> two progress renewals -> handoff/restore ->
blocked -> event resume -> artifact-backed done, plus negative fixtures for dispatch-without-taking,
expired-live versus abandoned-dead, duplicate done, wrong-key close, and spoken-but-uncited operator
reply. Acceptance: replay and hledger agree; zero unowned operator tasks; no open ask remains after a
keyed delivered result; blocked work remains queryable and is not redispatched before its retry edge.

## Other findings and hypotheses

Evidence: board structure was RED during malformed task posts and later returned OK; source/deployed
`mesh-mind-control` differ only by new busy/absent regression assertions, so the live behavior is not
yet protected by those assertions. The periodic lifecycle auditor detects only
not-dispatched/dispatched-but-not-started and calls `mesh-dispatch`; it does not enforce leases,
progress, blocks, resume, or closure. Auto-snapshot handoffs can contain only an idle prompt (for
example `~/.mesh/handoff/haunt.md`), so snapshot existence alone is not resumability evidence.

Hypothesis requiring a fixture: the earlier owner/slug corruption may be confined to historical
syntax/materialization because current corrected rows parse properly. Do not change grammar until a
fixture replays both forms. Hypothesis requiring a live drill: after deploying terminal acknowledgements,
old agents may continue writing `[fyi] ack`; these should remain harmless only if delivery filters them
or compatibility classification maps them to terminal control records without swallowing new work.

## Prioritized remediation and ownership

1. **P0 loop termination — genome:** land/deploy terminal ack filtering, add message IDs plus
   3-attempt/15-minute expiry ledger, run source/deployed parity and the integration fixture.
2. **P0 long-task state machine — genome:** implement canonical ask/task identity, exact ownership,
   lease/progress, typed block/resume, idempotent keyed closure, and end-to-end fixtures in the shared
   coordination tools; preserve existing `mesh-task` artifacts.
3. **P0 case reconciliation — witness with adint/genome/job:** migrate the three live cases without
   renaming their obligations; publish current owner/step/lease/blocker/artifact, close only keyed
   duplicates, and ensure the ten operator asks receive cited closure or remain visibly open.
4. **P1 independent verification — witness:** replay the VPN loop and all lifecycle negative arms,
   confirm cron invokes byte-identical tested deploys, and report bounded termination evidence.

No remediation item authorizes VPN or other substrate actuation.
