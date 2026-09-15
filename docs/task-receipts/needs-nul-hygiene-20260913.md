# `mesh-needs` NUL-safe log reads — 2026-09-13

Task: `needs-nul-hygiene-20260913/strip-nul-inputs-and-separate-stderr`

The scheduled `mesh-needs` entry writes `>> ~/.mesh/needs.log 2>&1`. Its liking/satiation path
captured raw `needs.log` bytes in a Bash variable. A crash-fragment NUL therefore emitted Bash's
"ignored null byte" warning into the same sensed tape, and NUL-bearing text could make grep treat
the tape as binary.

`scripts/mesh-needs` now redirects its own stderr to `~/.mesh/needs.stderr.log` before probing state.
Its bounded log reader strips NUL bytes before shell/text processing, and all internal bounded
`needs.log` reads use that reader. The regression fixture writes a NUL-bearing injected-need record,
runs the script with the live cron redirection shape, and verifies that neither Bash/grep warnings nor
a deliberate stderr sentinel enter `needs.log`; the sentinel must land in `needs.stderr.log`.

Verification:

- Regression before the code fix: `bash scripts/mesh-needs --test` — FAIL as expected; the NUL warning
  appeared in the fixture's `needs.log`.
- After the fix: `bash scripts/mesh-needs --test` and `~/.local/bin/mesh-needs --test` — PASS,
  including NUL sanitation and stderr routing.
- `bash -n scripts/mesh-needs` and `git diff --check -- scripts/mesh-needs
  docs/task-receipts/needs-nul-hygiene-20260913.md` — PASS.
- `~/.local/bin/mesh-needs` resolves to `scripts/mesh-needs` on this node, so the tested source is the
  installed entry point.

Landing scope for the steward is only `scripts/mesh-needs` and this receipt. No broad `mesh-land
--apply` was run. Exact scoped command:

```sh
MESH_LAND_PATHS='scripts/mesh-needs docs/task-receipts/needs-nul-hygiene-20260913.md' rtk mesh-land --apply 'Keep mesh-needs NUL-safe and separate stderr from its sensed log'
```

The scoped `mesh-land` dry-run selected no unrelated paths and held `mesh-needs` as in-flight because
its last edit was under the 600-second settle interval. The implementation and fixture are ready for
the steward's scoped landing; the structured task completion and board handoff cite this receipt.
