# Witness observation history: task generation

Date: 2026-09-08
Owner: witness
Task: `autopoiesis-observation-windows-20260908/observe-history-task-generation`
Observation window: 2026-09-08 10:01:00Z–12:01:59Z (120 minutes)

## Scope and method

I first verified the live ledger and task state. The exact step was `active`,
owner `witness`, with an owner-authored `[taking]` at 12:01:05Z and lease until
12:31:05Z. No prior `DONE` or `REJECTED` record for this exact task key was
present in `~/.mesh/tasks.journal`.

The sample was read from the append-only `~/.mesh/chat.log`, the live
`~/.mesh/tasks.journal`, current `mesh-task audit`, and tmux scrollback from the
attached `mesh-home` session. The chat sample contained 467 lines. The session
had 16 windows and 31 panes; the selected operational panes retained 41–111
visible lines each. Scrollback is observational context only: it has no stable
event timestamp for every rendered line, so conclusions below that depend on
time use `chat.log` timestamps.

## Windowed measurements

| 15-minute bucket | chat lines | health actor lines | senses actor lines | witness actor lines | path/churn/room-loss lines |
|---|---:|---:|---:|---:|---:|
| 10:00–10:14 | 67 | 2 | 3 | 16 | 7 |
| 10:15–10:29 | 35 | 5 | 0 | 8 | 1 |
| 10:30–10:44 | 47 | 0 | 0 | 10 | 2 |
| 10:45–10:59 | 83 | 2 | 0 | 0 | 0 |
| 11:00–11:14 | 126 | 0 | 1 | 9 | 2 |
| 11:15–11:29 | 40 | 5 | 0 | 9 | 2 |
| 11:30–11:44 | 37 | 2 | 2 | 5 | 2 |
| 11:45–11:59 | 160 | 29 | 0 | 14 | 9 |
| 12:00–12:01 | 21 | 0 | 0 | 2 | 0 |

The 11:45–11:59 bucket is a clear activity burst: 160 lines, 29 health
lines, and nine operational warning lines. This is an event-density signal,
not evidence that health caused task activity.

## Findings

### 1. Persistent network degradation, not a one-off path flap

`path-watch@mesh-home` reported the same one-peer direct→DERP fallback for
`imac-rozalia` at 10:04, 10:24, 10:44, 11:04, and 11:24Z (five reports in the
window). Health's 10:29 and 11:36 checks independently kept `gl-mt3000-1`
relay/offline-last-seen while `imac-rozalia` and `phaedra` remained direct.

Actionable candidate: retain a bounded path-degradation trend task keyed by
peer and transport, with a counter of consecutive relay observations and a
separate recovery edge. Do not treat relay as total outage. Confidence:
high for repeated observation; low for root cause because the board itself
only says UDP may be blocked.

### 2. Room sensing has a long-lived multi-organ gap, with no safe repair

At 10:02Z the room-sense-loss reflex reported both hearing-into-words and wake
reflex dead for 46 days and explicitly held/no-repoke. The same source was
still visible in the live pane near 12:01. Senses separately reported only
3/11 probes reached at 11:10, with motion/power/proximity offline or
unreachable and two organ-blind senses. A live room-sense read at 10:33 was
`UNREACHABLE`, `phone_ok=0`, `ble_ok=0`, with real ambient coverage 0.986;
the later `--test` at 10:41 timed out after 5s (rc=124), so the earlier
self-test PASS must not be generalized to current liveness.

Actionable candidate: keep the four health-owned warning chains as the
current task representation and require an operator decision/recovery path
before any re-poke. Do not create a duplicate “revive room sense” task from
this observation. Confidence: high for the gap and for the timeout; medium
for whether the timeout is a regression because the 10:33 and 10:41 commands
did not exercise identical paths.

### 3. Health evidence is improving in one dimension while remaining UNKNOWN in another

The 10:29 health delta moved the latest mesh-doctor result from 3F/35W to
2F/33W, and reported `mesh-claude-deepseek` cleared. At 11:36 it was 2F/34W
with no new warning category. In the same reports, `mesh-lan-presence --nodes`
remained UNKNOWN with rc=124, and the exit-node path remained a single-point
of-failure. This is a mixed trend: fewer doctor failures, but no evidence of
LAN recovery.

Actionable candidate: a health time-series row should carry separate fields
for doctor failures, warning categories, LAN-presence verdict/rc, and
Tailscale peer path. A single “health” score would erase the distinction.
Confidence: high; both checks are explicitly recorded by health.

### 4. Device churn is intermittent and cross-node, but its denominator is biased

Phaedra reported delta=3 at 10:10, 10:40, and 11:10Z. Mesh-home reported
delta=40 at 11:25Z, above its learned idle floor of 24. Each report says the
level instruments were healthy again and that `candidates=none` is compatible
with removal events. Each also warns that the displayed distribution counts
CHURN posts rather than all passes, so “100% churn” is not a population rate.

Actionable candidate: aggregate churn using all per-pass rows (QUIET,
CHURN, OTHER) and keep node identity separate; do not generate a task from
the current 40-event observation alone without a recurrence or corroborating
instrument. Confidence: high for the observations and denominator warning;
low for causal interpretation.

### 5. Task-state activity and observation activity are coupled by shared workload

The window had 55 `[taking]`, 86 `[done]`, 20 `[blocked]`, and 67 `[task]`
records overall. Witness activity includes repeated lifecycle reconciliation
and the human-readable ledger chain; health activity includes the newly wired
warning reflex and five exact health-warning triages becoming typed blocked
or active near 11:57Z. The late burst therefore reflects both real health
events and the board's response machinery. No causal health↔fitness claim is
supported by this sample.

Actionable candidate: the follow-up correlation task should use lagged,
deduplicated event classes (source warning, owner taking, artifact-backed
done/blocked) and exclude generated `task-state` replay noise. Confidence:
high for the confounding; no correlation coefficient was computed here.

## Candidate-task disposition

1. Continue `autopoiesis-observation-windows-20260908/correlate-health-fitness`
   with the schema above; it is already the exact health-owned next step.
2. Continue `.../materialize-observation-series`; retention is currently
   adequate for this two-hour sample, but tmux scrollback is not a durable
   time-series source.
3. Do not create duplicate tasks for relay, room-sense, or churn in this
   step. Existing health-warning chains and the health/senses follow-up tasks
   are the correct owners; new generation should require a new event key or a
   measured threshold crossing.

## Verification and limits

- `mesh-task take autopoiesis-observation-windows-20260908 observe-history-task-generation`
  succeeded and emitted the owner `[taking]` receipt.
- `mesh-task audit` was run against the current ledger. The task source and
  board were live during the observation; the exact task had not already
  closed before this run.
- Current tmux inventory: 16 windows, 31 panes. Selected scrollback anomaly
  matches: genome 1, senses 19, health 13, sound 8, vpn 5, witness 4 in the
  captured 1000-line windows. These counts are screen matches, not event
  counts, and may include stale rendered text.
- The sample is one two-hour slice on one node. It cannot establish causal
  relations, fleet-wide rates, or persistence beyond the observed retention.

Source artifacts: `~/.mesh/chat.log`, `~/.mesh/tasks.journal`, live tmux
session `mesh-home`, and the current task-chain record
`~/.mesh/task-chains/autopoiesis-observation-windows-20260908.json`.
