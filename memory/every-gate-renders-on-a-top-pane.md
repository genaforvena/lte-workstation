# Every gate renders on a top pane, or it is a blind change

2026-09-16. The operator asked whether the receipts culture should be forbidden
(minds writing proof-of-work files instead of working artifacts), then asked
where else deterministic gates were missing, then ordered all of them built and
landed — and added the binding constraint: in the end everything must be
OBSERVABLE on one of the top panes, otherwise it is a blind change; presence
in chat.log does not count.

What was built (genome, landed 2026-09-16): mesh-receipt-gate,
mesh-board-lint, mesh-substrate-lint, mesh-tmux-lint, mesh-test-quality-gate,
mesh-claim-freshness, mesh-receipt-peer-vantage, mesh-relay-lint,
mesh-doctrine-lint, mesh-pane-check — each with --test fixtures, each
red-then-green verified. mesh-land holds proof-of-work receipts and unbound
new-tool writes at land time (tracked files grandfathered).

The observability half: every gate is wired into a new mesh-doctor section
("deterministic gates"), whose verdicts land in ~/.mesh/.doctor-fails — which
the health pane DOCTOR section already renders, and which raises [doctor] on
state change. So a gate's state is visible on the check top pane within one
doctor tick. Board lines are correspondence, never the artifact: no arm passes
on "it was posted".

Two traps measured during the build:

- A doctor arm over UNCOMMITTED work must WARN, never FAIL. The first draft
  failed on 13 in-flight receipts other minds were still writing — doctor
  would have gone red on ordinary mid-work state. Enforcement lives at land
  time (mesh-land HOLDs); the doctor arm surfaces.
- `mesh-dash <role> --once` re-probes and takes minutes per role (all six
  roles timed out at 60–90s even with MESH_DASH_FAST=1). A pane-ownership
  check built on re-render can never fit a doctor tick. mesh-pane-check reads
  the LIVE tmux data panes with capture-pane instead — seconds for all 16
  channels, and it asserts exactly what the rule asks: what the pane shows,
  not what a fresh probe says.
