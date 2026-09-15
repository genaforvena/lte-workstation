# Task artifact durability receipt

`mesh-task done` previously checked that a receipt existed and passed repository-scope validation,
but it accepted paths under temporary storage. That allowed a task to become terminal while its
evidence disappeared when the temporary directory was cleaned.

`scripts/mesh-task` now resolves the requested path and rejects it when it is the temporary root or
below `/tmp`, `/dev/shm`, or the configured `TMPDIR` (falling back to Python's temporary directory).
The check runs before scope validation and before any completion ledger, board, or handoff writes.
The error names both the resolved artifact and matched temporary root. Durable paths continue through
the existing existence, scope, digest, and completion flow.

The built-in regression now exercises a live `/tmp` fixture, a `/dev/shm` fixture, and a custom
`TMPDIR`, and uses the source file as a durable positive completion artifact. Before the guard was
added, its `/tmp` case completed successfully; after the guard, all three ephemeral cases are refused
and the durable completion path passes. Integration fixtures that intentionally complete tasks now
use durable repository files rather than temporary artifacts.

Verification performed:

- `python3 scripts/mesh-task --test` — PASS.
- Origin-envelope, TG-intake acceptance, independent-pickup, optional-owner, and blocked-self-unblock
  integrations — PASS.
- The three completion-related no-expiry tests — PASS.
- Ledger-sync, autoland-task, and handoff-reset integrations — PASS.
- Workspace-scope integration — PASS.

A broader `tests/test-mesh-task-*` sweep also exposed two failures in pre-existing priority-order
assertions in the locally modified no-expiry test and one failure in the unrelated identity test. The
priority failures concern queue ordering and are not touched by this change; the identity failure
comes from the promises fixture. The artifact-durability and completion-flow tests listed above pass.

The source and receipt are ready for the steward. No install or landing was run because the operator
has an active hold on deploy changes on mesh-home.
