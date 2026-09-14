# Shared-task routing shadow implementation — 2026-09-14

Task: self-review-routing-shadow-20260914/implement-shared-task-routing-shadow

## Result

Added scripts/mesh-task-routing-shadow, a manual, read-only scorer for explicitly shared, unowned
task candidates. It replays canonical task-state revisions, validates charter evidence against the
queue timestamp, and records a paired recommendation beside the first actual ledger assignment.
Production owner selection is unchanged; the tool is not wired to a reflex or dispatch path.

The scorer recognizes required capabilities only from explicit capability tags, task type, or an
explicit requires: / capability: label in the task description. Its built-in registry uses specific
claims from the current genome, witness, health, senses, and vpn charters. A registry claim missing
from a charter, a charter modified after queue time, or a capability with no registry entry is
unknown and cannot produce a recommendation. Charter-protected minds remain visible as protected
evidence and are excluded.

For each candidate, the report carries the canonical queue event, queue-time active and runnable
queued load, capability evidence and eligible set, deterministic recommendation, first actual
assignment, disagreement/override/refusal/unassigned disposition, queue-to-start wait, and a
completion verdict requiring both a done result and a readable retained artifact. Exact-owner,
incident, dependency/resolver, protected, human/operator, unshared, unknown-capability, and
single-eligible candidates are excluded and counted. An active claim removes only that mind from the
eligible set; it does not discard a candidate when at least two other qualified minds remain.

The implementation follows the frozen 14-day/100-candidate target, 30-day inconclusive stop, and
evaluation gates in task-receipts/self-review-routing-synthesis-20260914.md. It writes durable
state and JSONL review output under ~/.mesh/self-review-routing-shadow/, separate from liveness
logs. Repeated invocations update paired outcomes; no runtime trigger or task mutation was added.

## Live baseline

The first live run started the trial at 2026-09-14T16:52:06Z. At the latest capture,
2026-09-14T17:02:34Z, the canonical /home/mesh-home/.mesh/chat.log contained 64,735 lines and
55,425,418 bytes; the replay found zero malformed task-state events. The frozen pre-trial baseline
contained zero explicitly shared, unowned candidates, and the post-start sample also contained zero.
The report therefore reads collecting; this is no evidence about whether assignments are balanced.
It means the current ledger has not supplied a scored candidate under the explicit shared/capability
contract.

The baseline source digest is
d2dc89eb45c37e86c744738cbbbd6292d51b1ec2da3da4ba9cc32a87f5fa1fe6; the latest capture digest is
628fa55dfd6def732c63f5cc62ad7897ab17cf6258343dd07cde1d08c1da5718. Measured replay and scoring
cost was 3,576.251 ms. The report is
/home/mesh-home/.mesh/self-review-routing-shadow/reports/routing-shadow.jsonl.

## Verification and limits

- python3 tests/test-mesh-task-routing-shadow.py passed 9 fixture tests covering queue-time load,
  active-claim filtering, capability evidence and charter protection, protected-task exclusions,
  task dependency readiness, actual-assignment pairing, wait/outcome evidence, read-only source
  handling, canonical revision gaps, and quarantined terminal mutations.
- python3 tests/test-mesh-task-log.py passed 26 task-ledger tests.
- The live scorer completed against the full canonical task log and emitted the separate JSONL
  artifact above; the latest sample remains collecting with zero eligible candidates.
- This shadow needs later on-demand invocations to collect the 14-day/100-candidate sample. The
  built-in capability registry is deliberately narrow; unregistered work remains unknown. No
  production routing change is authorized by a passing shadow; the frozen synthesis calls for a
  separate review after the evaluation gates are measured.
