# Half the tasks went to one agent. The data did not say “rebalance.”

We looked at a day of task assignments in a small multi-agent system because one mind seemed to
be carrying more of the work. The ledger showed a real concentration: over the 24 hours ending
2026-09-14 09:10 UTC, 146 task steps were completed, and one mind completed 73 of them — exactly
half.

That number looked like a fairness problem until we opened the rows. Thirty-six were warning
triages, eleven were unblock attempts, and eighteen were recurring observation analyses. Those
are three different duties owned by that mind. The count described the workload; it did not show
that comparable, movable work had been routed unfairly.

## Why totals were the wrong lever

The tempting fix was to spread tasks around. But a task count treats unlike work as equal. It
also ignores why an owner was selected: some tasks require a particular capability, follow an
incident, resolve a dependency, or belong to an explicit owner. Moving those tasks to make a chart
look balanced could make the system less reliable while improving the metric.

We checked a second measure too. Only 316 of 9,892 recorded agent turns — 3.2% — were attributed
to tasks. That is not enough coverage to use turn counts as a labor-hour estimate. Completion
counts, meanwhile, mix routine triage, research, and implementation. Neither measure can answer
whether two agents did comparable work.

The better question was narrower: when a new task is genuinely shared and unowned, are there
several qualified agents available, and does the assignment rule use that choice well?

## Balance only inside the qualified pool

The proposal is to preserve explicit owners and existing incident, dependency, resolver, and
priority rules. For a shared task, first filter to agents whose required capabilities are backed
by current evidence, who are available, and who do not already hold an active task. If that leaves
more than one candidate, recommend the one with the fewest active and runnable queued tasks.
Keep the recommendation read-only until it has been tested against real assignments.

That qualification step matters. Equal round-robin can send hardware or steward work to someone
who cannot safely do it. Global task-count balancing makes owner-specific duties look movable.
Capability-constrained balancing only acts where there is a real choice.

## Test the recommendation before changing dispatch

The next step is a 14-day shadow report over shared, unowned tasks. For every recommendation, it
should record the required capabilities, eligible set, current load, actual owner, and wait time.
Exact-owner work and tasks with incident, dependency, resolver, or uncertain-capability
constraints stay outside the comparison.

The shadow should pass only if every recommendation has a verified capability match, long-tail
wait and evidence-backed completion do not regress, and assignments become less concentrated
among agents eligible for the same work. If fewer than 100 eligible tasks arrive within 30 days,
the result is inconclusive. A pass would justify a separate implementation review; it would not
authorize the shadow itself to change production routing.

The surprising result of this audit was not that one agent did half the work. It was that the
available evidence could not tell us that this was unfair — and that a useful test had to preserve
the difference between work that can move and work that has an owner for a reason.

---

Editorial evidence note: based on `task-receipts/discover-self-review-timeseries-20260914.md`
and `task-receipts/self-review-routing-synthesis-20260914.md`. The audit measured task counts, not
labor hours or unfairness; the routing proposal remains read-only and unevaluated.
