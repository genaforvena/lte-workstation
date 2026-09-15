# Witness live unattended-signal follow-up — 2026-09-08

Sweep window: 2026-09-08T15:31:53Z through 2026-09-08T15:39Z UTC, after the
completed sweep `docs/witness-mesh-chat-delivery-unattended-warning-sweep-20260908.md`.
The original user dispatch receipt is `ack:e0194e490d9d5547`.

## Actionable signals routed

The following post-cutoff signals had no exact current ledger row and were
created in `witness-live-unattended-followup-20260908` from
`docs/witness-live-unattended-followup-plan-20260908.tsv`:

| signal | owner-routed ledger step | evidence / acceptance |
|---|---|---|
| HH applications reader remains blind/nav-failed; selector/parser returns 0 rows; dry reply timed out | `.../repair-hh-parser-selector` → `job` | 15:28:11Z board task and 15:28:16Z handoff; repair plus live zero-row regression and scheduled-route proof |
| autoland refused rebase because two parked autostashes are older than the safety horizon | `.../repair-parked-autostash-strand` → `land` | 15:18:08Z `[strand] priority:incident`; inspect and preserve both stashes, then prove refusal detection/routing |
| ideas queue has 27 aged `[~]` items, oldest handoff 22d, and no declared queue-tend owner | `.../repair-ideas-queue-duty-routing` → `genome` | 13:59:02Z mesh-ideate `[task]`; assign/charter ownership, discharge the queue safely, and test the floor guard |
| health-warning reflex cannot create a new task because deterministic chain `health-warning/25d17bc908dbe3b61fe4` already exists blocked; repeated cron failures leave cursor work unrouted | `.../repair-health-warning-reflex-idempotency` → `genome` | `~/.mesh/health-warning-task.log` and direct live invocation returned rc=1; add existing-blocked-chain idempotency regression and verify cron |

The chain was created and its first dispatch was emitted by `mesh-task create`.
`mesh-task dispatch` correctly refused a second dispatch because the current
step was already dispatched; owner-authored `[taking]` remains required before
any step is considered started.

The `land` service is not a valid `mesh-chat --to` target on this node. To keep
the incident routable, a corrected genome-owned one-step task
`witness-live-autoland-followup-20260908/repair-parked-autostash-strand` was
also created and dispatched; it is the authoritative owner route for this
signal. The original umbrella row remains open as a routing-audit record and
must not be treated as started.

Direct owner task posts were emitted to `job` for HH parser drift and to
`genome` for the corrected autoland route, ideas-queue duty, and health-reflex
idempotency. The corresponding ledger rows remain open until those owners post
recognized taking transitions.

## Coverage and dispositions

Existing reflexes verified in the live crontab:

* `mesh-chat-deliver` runs every minute.
* `mesh-health-warning-task` runs every minute and is intended to turn health
  source warnings into health-owned tasks.
* `mesh-land --autoland` runs every 15 minutes and emits the parked-stash
  refusal.
* `mesh-job-reply --tg` runs every two minutes.
* `mesh-ideate` runs every 15 minutes; its own capacity post detected the
  queue-duty incident, but no owner-routing reflex closed the loop.

The health reflex is not healthy: `~/.local/bin/mesh-health-warning-task`
reproduced `mesh-task create failed (2): chain ... already exists` and exited
1. This is why a separate genome repair task is routed instead of calling the
warning already covered.

The repeated `mesh-chat-deliver [delivery-failed] attempts:3` lines remain
covered by the active genome task
`witness-mesh-chat-delivery-attempts-correction-20260908/fix-attempts-field`;
they are not duplicated here. Known health egress/exit-node/fleet alarms and
the 15:35 FAIL-count change remain covered by existing health-owned blocked
warning chains and the minute health-warning reflex; the new reflex failure is
the separately actionable gap above. Hire's missing credential is an explicit
operator gate with a durable artifact and no unattended technical action.
Senses' partial/unknown fusion, udev unattributed events, sound REFUTED/MIXTURE,
and discover's NVMe permission denial are explicitly reported with UNKNOWN or
rejection semantics and had no new owner-routable fault in this window.

## Verification

* `mesh-task status witness-live-unattended-followup-20260908` shows 4 open
  owner-specific steps; no closure is inferred from dispatch.
* `systemctl is-active cron` returned `active`.
* Live crontab entries above were present.
* `mesh-task --test` and the existing focused tests were already recorded by
  the predecessor sweep; the new direct `mesh-health-warning-task` run exposed
  the rc=1 idempotency defect rather than masking it.
* `mesh-card --refresh` was bounded at 8s and produced no output before timeout;
  this is recorded as an observation limitation, not as a healthy-board claim.

Unresolved obligations: each of the four owner steps needs an owner-authored
`[taking]`, then an artifact-backed `[done]` or concrete `[blocked]/[rejected]`.
