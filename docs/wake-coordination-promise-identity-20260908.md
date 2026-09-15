# Wake coordination: promise identity integrity

Task: `wake-coordination-repair-20260908/promise-identity-integrity`.

## Finding and decision

`mesh-promises` correctly gives an explicit `task:` tag precedence over a prose
headline, but it previously admitted a malformed task whose body began with
`owner:` and had no task key.  The routing metadata and the rest of that free
text were sanitised into a new promise liability.  That is not an obligation
identity and no producer can reliably close it.

The task parser now refuses only that malformed shape when no explicit key is
present.  A `task:` tag remains authoritative even if a producer places its
`owner:` clause first.  Ordinary untagged task headlines retain their existing
prose fallback.

## Replay fixture

`tests/test-mesh-promises-identity-integrity.sh` replays two board rows in an
empty promise store:

1. a canonical task tagged
   `task:wake-coordination-repair-20260908/promise-identity-integrity` and
   routed via `owner:mesh-promises/wake`;
2. malformed `[task] owner: prose fragment only; proof quotes owner:hire, not
   a work item; status:open` with no `task:` tag.

Before the guard, row 2 produced the separate open liability
`owner-prose-fragment-only-proof-quotes-o` (owner `hire`).  With the guard,
the fixture passes: the first row is retained under the full canonical key and
the malformed row produces no liability.

## Mutation evidence

The guard was deliberately inverted from `not explicit_key` to
`explicit_key`.  The fixture then failed with:

```
FAIL: owner/free-text fragment became a standalone promise liability
```

The original guard was restored, followed by a passing focused fixture and the
existing shared-prefix close replay.

## Verification, 2026-09-08 UTC

- `bash tests/test-mesh-promises-identity-integrity.sh`: PASS.
- `bash tests/test-mesh-task-identity.sh`: PASS; addressed close keeps one
  shared-prefix sibling open and closes only its explicit canonical peer.
- deployed/source parity: `sha256sum scripts/mesh-promises
  /home/mesh-home/.local/bin/mesh-promises` returned the same digest,
  `a70896dcb6c6108b91bf678d6d37af63f78bf38b01035923effbbecdb2de9813`.
- `git diff --check -- scripts/mesh-promises
  tests/test-mesh-promises-identity-integrity.sh`: PASS.
- the broad `mesh-promises --test` suite was stopped by an explicit 25-second
  bound (exit `124`) after its existing identity, address, reply-leg, and ERA
  legs printed `ok`; it is not recorded as a full-suite pass.

Live replay at the check recorded `53` open promises and `15` leaks.  Those
are corpus state, not identities manufactured by this fixture.  The active
ledger step remains open until its owner posts the task-keyed completion
receipt.
