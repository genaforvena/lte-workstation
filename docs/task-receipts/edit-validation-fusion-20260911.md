# Edit-validation fusion — 2026-09-11

## Result

`scripts/mesh-edit-validate` applies one explicit byte replacement atomically, records the before
and after SHA-256 values plus a unified diff and recoverable original bytes, then invokes the
specified validator with `{file}` bound to the resulting file. Its JSON receipt is written before
validation and updated with validator argv, return code, stdout/stderr and hashes.

The real pass receipt is `artifacts/edit-validation-fusion-20260911/pass.json`; the real forced-fail
receipt is `artifacts/edit-validation-fusion-20260911/fail.json`. A failed validator exits 1 and
sets `status=validation-failed` and `success=false`; it never claims success. An unavailable
validator is recorded as `status=validator-unavailable`, also with `success=false`.

## Recovery semantics

Validation failure intentionally leaves the edited file in place so the failed state is inspectable.
Run `scripts/mesh-edit-validate --recover <receipt>` to restore the exact original bytes. Recovery
is hash-guarded: it refuses to overwrite the file if its current hash is no longer the recorded
post-edit hash, preventing a later edit from being silently destroyed. Successful validation keeps
the same recovery option for deliberate rollback.

## Verification

`tests/test-mesh-edit-validate.sh` passes locally. It proves exact edit count, before/after hashes,
diff and validator file binding; a validator pass; a forced failure with non-success receipt; and
hash-guarded recovery to the original bytes.
