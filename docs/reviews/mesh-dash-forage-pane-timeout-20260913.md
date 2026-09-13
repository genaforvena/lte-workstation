# mesh-dash forage pane timeout — 2026-09-13

The minds pane now bounds `mesh-forage --json` to 2 seconds. Missing tools, a timeout, a nonzero
producer exit, and invalid or empty JSON render an explicit `UNKNOWN` row; no allocation value is
invented. Valid JSON still renders the division-of-labour result. The cap keeps a slow board scan from
holding the interactive pane for its former 20-second budget.

The isolated smoke arms run before the broader dash checks. A fixture with valid JSON must render the
expected allocation, while a fixture that sleeps past a 0.1-second test cap must render `UNKNOWN` and
must not retain an allocation row.

Verification:

- `bash -n scripts/mesh-dash` — passed.
- `bash scripts/mesh-dash --test-fast` — passed, including both isolated forage arms.
- `bash scripts/mesh-dash --test` — exit 2 (`n/a`): every leg runnable on this busy node passed; the
  27-row pin was below the measured 28-row fixed floor, and the fast-core timing leg was unmeasurable
  at 15 seconds best-of-three under load 17.54 against its 9-second quiet-node bar.

The full-suite status is a node-condition result, not a green full-suite verdict. The final landing
must include only `scripts/mesh-dash` and this receipt.
