# Health warning triage: 5349a5a97dc8c9ef79c2

Timestamp: 2026-09-16T01:54Z

## Source and ledger evidence

- Source `/home/mesh-home/.mesh/chat.log:69953` records witness evidence at
  `2026-09-16T01:46:45Z`: the range review found 76 `[health-fail]` markers,
  93 `[task-ledger]` records, and repeated triages concluding stale/already-DONE
  witness warnings. It explicitly routes the issue to the existing
  `health-warning-backpressure-20260909` correction and asks for trace-only
  admission of transient stale autonomy checks.
- The immediately following witness receipt at line 69954 states that all 250
  accepted source messages were reviewed and no duplicate task was created.
- The exact task was dispatched with `mesh-task queue --dispatch --owner health`,
  passed `mesh-task check dispatch health-warning/5349a5a97dc8c9ef79c2/triage health`,
  and was taken by the exact owner. `mesh-task status health-warning/5349a5a97dc8c9ef79c2`
  reports one active step, owner `health`, lease through `2026-09-16T02:23:41Z`.

## Live health evidence

`mesh-dash --once check` at `2026-09-16T01:53:08Z` reports:

- local load high (`15.75/16`), making reachability probes unreliable;
- doctor cache `FAIL=1 WARN=33`, with the real `mesh-model-swap` smoke-test failure;
- VPN `friends@phaedra` degraded with no WG client handshake in the current sample;
- 24-hour egress `BAD=2%` (`7/431`), DERP UDP unavailable, and GPU healthy at
  `6274/12288M`, 0% utilization, 47C, no throttling.

These live alarms are separate from the reviewed stale-warning admission issue;
no routing, DNS, firewall, VPN, or other substrate mutation is authorized by this
triage, and none was performed.

## Decision

The reviewed witness warning is a stale duplicate/report-only signal already
covered by the existing backpressure correction. Keep this task open for the
owner's durable follow-through because the current evidence identifies an
admission-policy concern but does not itself prove the deployed reflex behavior.
The next safe step is a read-only source/deployed parity and live reflex check for
`health-warning-backpressure-20260909`; substrate changes remain out of scope.

Delegation record: worker `health-audit` was launched for an independent read-only
model-swap/fleet audit. Its relay did not produce a submitted finding within the
available window, so no worker report is treated as evidence; all claims above were
personally inspected from the cited chat log, task ledger, and dash output.
