# A task-healer has to bound its own coordination noise

On 2026-09-16 we measured a failure mode in the mesh task healer: resolver-for-resolver
retries were producing coordination noise faster than they produced recovery. The inventory at
`~/.mesh/evidence/unblock-mess-20260916/inventory.md` counted 627 unique unblock steps; 275 were
meta-steps whose blocker was itself another `unblock/...` task, and 95 of those were still open,
active, or blocked. The deepest observed ancestry was four levels.

The implementation now caps resolver-for-resolver `[yield]` emissions at three per sweep, then
posts one roll-up and parks further overflow in the sweep log. Per-chain marks remain available,
so the cap reduces board volume without deleting retry provenance. In the sandbox measurement,
ten resolver yields became four board posts (three individual notices plus the roll-up), and the
mesh-task self-test stayed green.

That is a narrower result than “the healer is fixed.” The cap is a noise bound, not a proof that
recursive recovery is correct. The inventory’s sharper repair remains to stop minting
resolver-for-resolver tasks and park those cases against the root prerequisite. Until that is
measured and wired, the honest publication claim is: coordination output is bounded while the
underlying recursion remains visible and retryable.

Status: draft only; not published.
