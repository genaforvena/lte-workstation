# Operator request follow-through repair — 2026-09-16

## Findings and changes

This audit joined local operator input, `chat.log`, canonical task replay, dispatch
logs, and the real receiver instructions. Private message contents are omitted.

- The Telegram request at `~/.mesh/voice-in.log:1293` appears in composer-wedge
  diagnostics at `chat.log:62921,62944`; associated health triages at lines
  62928/62946 have null ask keys. `chat.log:65988` records answering another request
  with no new task dispatch. A handoff or reply did not guarantee durable ownership.
- At the initial replay, 1,328 chains contained 1,307 done, 168 rejected, 60 blocked,
  103 open and three active steps. Only 45 chains had ask keys; three ask-linked
  chains had creation dates since September 14, including this repair. These are
  coverage measurements, not a verdict that every unlinked message was unanswered.
- The live dispatch tape at 00:12Z stamped unrelated witness tasks with
  `task:mesh-owned`, derived from boilerplate prose. Queue rendering now preserves
  the canonical ID before arbitrary descriptions. Production prompts give exact
  `mesh-task take/done/reject` instructions; board prose is explicitly insufficient.
- The delivered-signature filter permanently hid canonically open work even when a
  receiver never took it. Only human-owned refusals remain permanently excluded;
  canonical state and the receiver's existing cooldown govern redelivery.
- `mesh-codex-context` crashed with unset `MESH_WHO`, and swallowed reader/parser
  failures. It now permits handoff window discovery and reports restore failures.
- Telegram frames now carry an immutable `ask:tg-<24 hex SHA256>` source key and
  durable intake/delivery instructions. Identical source replay has the same key;
  distinct messages within the same second have different keys.

## Autonomous observation and repair

`mesh-operator-intake` reads the local Telegram inbox and canonical task ledger on
inbox changes and boot catch-up. Unlinked complete TEXT/VOICE/DOCUMENT records
become bounded reconciliation tasks owned by `tg`, with deterministic chain IDs.
The initial scope is the previous 48 hours; its persisted bootstrap floor prevents
later downtime from aging unseen messages out. Each pass attempts at most three
creates, including failed attempts. It never sends or repeats external actions.

The reconciliation owner checks original source, prior work and actual destination/
delivery receipts. Answered or non-actionable messages settle with private evidence;
unresolved work must have an exact owned chain before reconciliation closes. Existing
canonical ask links, including reasoned terminal dispositions, prevent duplicates.
The observer measures ledger coverage, not semantic correctness of every completion;
existing witness review and artifact verification retain that responsibility.

Every evaluation records health/counts in `~/.mesh/operator-intake/status.json` and
`run.log`. Read failures are UNKNOWN and create failures DEGRADED. In event mode,
unchanged input stays quiet/healthy regardless of age; changed input not evaluated for
15 minutes is STALE (PENDING before that). Remaining coverage gaps say GAPS. The witness
heading shows this status without another ledger replay or losing its required 20
task rows and 20 raw chat lines. A dead observer therefore becomes visible to the
existing pane-consume and witness workflow.

The dry-run before installation found nine recent messages without matching source
keys. These are recovery candidates, not nine proven unfulfilled requests. This pass
does not claim to audit pre-bootstrap history or operator conversations that never
entered a durable source. Direct pane requests still use the intake skill and ledger;
board review remains the separate cross-channel audit.

## Workflow skills and subagents

Three repository skills cover window turns, operator follow-through and task recovery.
Every chartered window receives their paths through `mesh-handoff --restore`, preserving
node-local charter precedence. Missing deployed skill files are explicitly reported.
The restore text, dispatch prompt and window-turn skill prefer subagents for independent
pieces, isolated worktrees for edits, and parent-owned coordination/verification. The
obsolete one-active-task wording in the lifecycle document now matches configured
capacity (default three).

Two Codex workers were delegated intake and dispatch audits through the session relay;
the intake worker also produced an isolated observer prototype. Parent inspection
confirmed the source lines above and rejected two unsupported audit leads: `check`
does not take the mutation lock, and `audit` exists despite incomplete help text.
The prototype's claimed tests were insufficient: parent lifecycle tests exposed false
healthy status, unbounded failed attempts, incomplete-source intake and silent errors.
The integrated implementation was corrected and verified against the real task ledger.
Independent review checked the final dispatch/restore changes and observer.

Design choice: immutable source bytes identify an event; semantic text normalization
could merge distinct operator requests. Failure-only retries of internal,
idempotent task creation remain enabled; a retry ceiling would abandon the request.
Reasoned DONE/REJECTED records are not automatically reopened by the intake observer.

## Verification

Observed red then green: context restoration, canonical dispatch IDs/lifecycle prompt,
delivered-without-take retry, Telegram source keys, workflow restore pointers, witness
status rendering, and nine real-ledger observer lifecycle cases. Source-era dispatch
tests were corrected to exercise the current task queue rather than retired promises.

Passing checks include the focused regression scripts, task-query failure and final
eligibility gates, unassigned routing, `mesh-dispatch --test`, `mesh-handoff --test`,
`mesh-tg-filter --test`, workflow skill validation, manifest validation, and witness
viewport checks. Self-tests use isolated state and do not stamp live intake liveness.

## Event-driven communication rollout

Operator steering applies to both `tg` and `tg-roz`. Their generic pane consumer now
rejects telemetry-only/self-pick wakes while retaining exact-owner task admission.
Node-local wake rules suppress dashboard drift in already-running drivers too.
`systemd/mesh-operator-intake.{path,service}` watches `voice-in.log`;
`systemd/mesh-roz-channel.{path,service}` watches `tg-strangers.log`.
Both paths are enabled and active/waiting; boot oneshots catch downtime. Failed or
incomplete passes retry after 60 seconds; successful idle lanes have no periodic run.
Exactly the two old intake polling cron entries were removed from desired/live cron.
The already-desired chat-range-review 15-minute cadence was reconciled into live cron
(it had still been running every minute); unrelated cron entries were preserved.

The delegated Rozalia delivery fix was inspected and integrated by the parent. It
serializes consumers, matches sender IDs exactly, and advances the cursor only after
successful dispatch. Failed/missing-window delivery stays pending and returns failure.
Partial source lines are ignored until committed. Stable ask keys and follow-through
instructions accompany delivery; an inbound receipt is not a Telegram send receipt.
Eight isolated delivery cases and the shared communication wake gate pass. Twelve real
ledger intake tests include event-backlog retry, zero-grace new events, and quiet/stale
status distinction. Unit syntax validation passes; live Rozalia boot catch-up exited 0.

Initial live intake encountered task-lock contention and honestly recorded DEGRADED;
the subsequent pass created three canonical recovery tasks, leaving six of nine gaps.
Live tg has begun claiming the first reconciliation. Final event backlog state is
recorded separately below; a task being queued is not proof its operator work is done.
Full mesh-dash self-test exited 2 (N/A): all runnable functional legs passed, but the
9-second performance budget was unmeasurable at load 77.58 on 16 cores (best 19s).

The independent review identified the crash window between pane dispatch and cursor
commit. This is explicitly at-least-once, not exactly-once: stable ask keys and receipt
reconciliation prevent repeated external effects. Receipt-open failure is now detected
before dispatch. The append-only source contract is documented, truncated Rozalia input
fails loudly, and same-size/same-mtime inode replacement is detected by intake status.

## Additional operator requests

The delegated tg-pane implementation was inspected against `mesh-tg`'s successful-send
log path. Parent integration uses a six-row chronological conversation (last three IN
and three verified OUT receipts), not another seven-row section that could overflow.
Only `voice-in.log` and `tg-sent.log` are read; Rozalia's private log is excluded. The
fixture checks ordering, row budget, both directions and privacy. Installed mesh-dash
was updated and only the tg/witness data renderers were reloaded; no mind was reset.

Deployment audit caught regular installed copies of mesh-pane-consume and mesh-dash
lagging source; exact reviewed hunks were deployed. Both communication driver processes
now report the deployed/source SHA a9f05e7ff5ec15858f8a44809a464d16b8ebe5ccf3ac1798a599bf6305f485e6.
The live tg pane was captured displaying the new conversation heading and mesh receipts.

The evidence-led skill expansion plan is `docs/task-plans/mesh-reusable-workflows-20260916.md`.
Canonical replay verified `mesh-reusable-workflows-20260916/adopt` OPEN, owner genome,
revision 2. It ranks recurring workflows and adds at most three justified skills, with
behavioral/adoption evidence instead of duplicating charters or adding periodic wakes.
Operator clarification is incorporated: all three shared skills and every restored
window explicitly treat skills as adjustable living procedures. Minds may improve them
within authorized scope, recording rationale, shared-source updates, tests and handoff.
Authorization, privacy, coordination and verification cannot be waived by a skill edit.
Restore regression was observed red then green for that explicit guidance.

## Handoff state (2026-09-16 00:47 UTC)

Root repair chain completed with this artifact. The last finished live intake pass
created three more recovery tasks with no errors; eight of nine initial source events
now have canonical coverage, one gap remains queued for failure-only retry. This is
coverage, not proof all historical requests have been fulfilled. Exact next check:
`mesh-operator-intake --status`; if retry stops progressing, inspect
`journalctl --user -u mesh-operator-intake.service -n 30` and task-lock contention.
`tg` owns reconciliation; genome owns the posted skill-adoption follow-up.

Final focused checks: 12 intake lifecycle tests, 8 Rozalia delivery tests, conversation
ordering/budget/privacy test, communication event-gate test, complete pane-consume
self-test, all-charter workflow restore test, skill validators and systemd unit syntax
passed. Installed tg pane capture confirms both IN and OUT; witness capture confirms
intake status. Unrelated staged whitespace issues were left untouched. No broad commit
or reset was performed in this shared, concurrently edited worktree.
