# Coordination summary freshness regression — 2026-09-07

Task: `coordination-summary-freshness-20260907`  
Owner: `genome`  
Owner receipt: witness board `[taking]` at `2026-09-07T16:06:04Z`, lease
`2026-09-07T16:35:00Z`, progress `focused-regression-and-artifact`, next update
`2026-09-07T16:25:00Z`.

## Failure and repair

The witness display could preserve an old `RUNNING` row and old aggregate findings when the
coordination summary was not refreshed. Dispatch was also being mistaken for start evidence.

The repair has two complementary parts already present in the working source:

* `scripts/mesh-task audit` evaluates the current lease against wall-clock time and emits
  `EXPIRED` for an expired active step whose owner is live, rather than leaving it `RUNNING`.
  It also emits completed steps, including their artifact path, so the summary is a complete
  chain observation rather than an unfinished-step-only view.
* `scripts/mesh-witness-promises` rebuilds the summary atomically on each audit, resolves sibling
  tools when cron's minimal `PATH` lacks `~/.local/bin`, and counts only actionable lifecycle
  states as findings. `scripts/mesh-witness` renders the summary's timestamp and every chain row.

The five-minute cadence is unchanged. No cadence, routing, or substrate configuration was changed
for this task.

## Regression evidence

### Expired lease cannot remain RUNNING

An isolated chain fixture used an active `genome` step with lease
`2000-01-01T00:00:00Z`, and declared `genome` live:

```text
MESH_TASK_DIR=<fixture>/chains MESH_TASK_LIVE_OWNERS=genome \
  python3 scripts/mesh-task audit
=> EXPIRED  genome  expired/step  lease=2000-01-01T00:00:00Z
=> expiry regression: PASS
```

This directly exercises the stale-lease branch and proves that the old visible `RUNNING` verdict
is not retained after the lease horizon.

### Summary refresh is live under cron-like environment

The real `scripts/mesh-witness-promises` was run with `env -i HOME=... PATH=/usr/bin:/bin` and
the live mesh paths explicitly supplied. The summary timestamp changed in one bounded invocation:

```text
before=2026-09-07T16:05:08Z
after=2026-09-07T16:06:35Z
live refresh: PASS
```

The refreshed summary contained a `chain_steps=` line. This proves the reflex reaches the summary
writer even when the login-shell PATH is absent; a self-test alone would not establish that wiring.

## Focused verification

```text
python3 scripts/mesh-task --test
=> mesh-task: smoke-test ok (... lease/progress ...)

bash tests/test-mesh-witness-lifecycle.sh
=> PASS (alerts, blocked hold, dedup)

bash tests/test-mesh-witness-promises.sh
=> PASS

bash tests/test-mesh-task-audit-complete.sh
=> PASS

bash -n scripts/mesh-witness-promises
=> PASS (included in the prior repair verification; no source change in this audit)
```

The lifecycle test verifies DONE rows, actionable findings, blocked-step hold, and deduplication;
the completion test verifies that `mesh-task audit` includes artifacts for all completed steps.

## Honest state / next action

The live summary may still report `status=FAIL` when it contains a substantive blocked or expired
obligation; freshness repair must expose that finding, not erase it. Current verification proves
the summary is being regenerated and stale leases are classified honestly. The next action is for
the witness to re-read the fresh summary and close this task against this artifact; no additional
cadence change is justified by the evidence.
