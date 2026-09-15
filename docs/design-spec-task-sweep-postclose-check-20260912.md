# Design/spec sweep — post-close ledger check, 2026-09-12

This is the fresh post-close supplement to
[`design-spec-task-sweep-final-20260912.md`](design-spec-task-sweep-final-20260912.md). The main
matrix was written before its final row was terminalized; this receipt captures the later live state.

- `mesh-task status design-audit-task-sweep-20260907`: complete, 18/18.
- `mesh-task status design-spec-task-sweep-20260907`: complete, 25/25. The final row is DONE under
  owner `tg`, has tags `design_audit,final_verification,disposition_matrix`, and points to the main
  matrix as its design artifact and completion artifact.
- A fresh `mesh-task audit` exited 0 and its filtered output contained all 43 rows from the two
  chains; every row was DONE with an owner and a completion artifact.
- Post-close `mesh-promises --feed` exited 0 (`open=203`, `kept=1984`). The subsequent
  `mesh-promises --check` exited 0: parity passed and replay/balance agreed at promises 203/203,
  claims 149/149, holds 62/62, and asks 66/66.
- The promise check still reported 5 unrouted promises, 142 unrouted claims, and 5 unrouted holds.
  All 43 sweep rows have owners `tg` or `wake`, both on the declared/live roster; these diagnostics
  are separate existing obligations.
- Immediately after the final check, the working `~/.mesh/promises/promises.journal` read as 0 bytes,
  while the latest feed commit still contains a 1,633,953-byte snapshot. Two concurrent
  `mesh-promises --balance` processes were visible during an earlier zero-byte observation; the
  cause of the later empty working file is unresolved. The check's own replay/parity verdict passed,
  but the durable working-file state needs a separate follow-up.

The post-close checks are ledger snapshots. Underlying design work stays at the per-row PASS, OPEN,
BLOCKED, DECLINED, or SUPERSEDED disposition documented in each completion artifact.
