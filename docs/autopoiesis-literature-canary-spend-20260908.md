# Task-attributed spend

Task: `autopoiesis-task-ledger-20260908/run-literature-canary`
Command: `mesh-labor --branch autopoiesis-task-ledger-20260908/run-literature-canary`

Observed after the task's `[done]` close:

```text
branch: autopoiesis-task-ledger-20260908/run-literature-canary
owner-window : discover
opened       : 2026-09-08T11:07:33Z
closed       : 2026-09-08T11:12:02Z
labour cost  : 0 TURN
```

The report explicitly labels this as first-order interval attribution, not
per-turn proof. The result is **0 TURN observed in the owner-window interval**;
no synthetic spend was invented. The live rolling labour meter at the run was
350 TURN total, 27 TURN for discover, with no task-tagged turn attributable to
this closed interval.
