# Autopoiesis origin continuity verification

Date: 2026-09-08
Chain: `autopoiesis-task-ledger-20260908`
Step: `verify-origin-continuity`
Owner: `witness`

## Live-state gate

Before verification, the live task ledger reported:

```text
autopoiesis-task-ledger-20260908 [active] (2/5)
verify-origin-continuity [active] owner=witness priority=95
```

The step was open before `mesh-task take ...`; it was not stale or already
settled. The predecessor `implement-origin-envelope` was done with
`docs/autopoiesis-origin-envelope-verification-20260908.md`.

## Commands and observed results

All commands were run from `/home/mesh-home/lte-workstation` on the current
working tree.

```text
python3 tests/test-mesh-task-origin-envelope.py
PASS: origin envelope, refusal, duplicate status, legacy replay, and cache rebuild
```

This isolated fixture exercised create and replay, all six missing-field
refusals, blank-field refusal, unknown and duplicate origin headers, duplicate
`origin.source` while open and after settlement, canonical rebuild, malformed
canonical origin rejection, and the concurrent duplicate-source race. The
expected refusal status was exit code 2 in each refusal case.

```text
python3 -m unittest tests/test-mesh-task-log.py tests/test-mesh-task-no-expiry.py
.....................
----------------------------------------------------------------------
Ran 21 tests in 5.540s

OK
```

The replay suite observed refusal for duplicate paths, sparse paths, invalid
typed values, revision gaps/conflicts, truncated records, malformed readable
payloads, damaged structured records, and conflicting duplicate revisions. It
also verified mixed legacy `[task-state]` plus readable `[task-ledger]` replay,
idempotent append, and durable replay after append.

```text
bash tests/test-mesh-task-restart-continuity.sh
test-mesh-task-restart-continuity: PASS (restart take->progress, canonical owner, stale/wrong-owner, bounded concurrency)
```

The restart fixture restored the active task from canonical state despite a
stale task-context pointer, refused a second owner claim, refused a foreign
owner's fabricated progress, and accepted the canonical owner's post-restart
progress. The observed refusal states were non-zero command exits with
`already has active task demo/work` and `exact owner required`.

```text
python3 scripts/mesh-task --test
mesh-task: smoke-test ok (canonical ask/task, exact owner, lease/progress, typed block/resume, artifact hash, idempotent done)
```

The smoke test covered successor handoff ordering: the handoff is written
before successor board dispatch, and a failed handoff/dispatch remains a loud
retryable failure rather than falsely advancing the chain.

## Wiring and live evidence

```text
sha256sum scripts/mesh-task ~/.local/bin/mesh-task
4d5f0c97dd7765e906864ab684779f7cfa25184bfb0107e3ad2ff42cae0e25bc  both files

sha256sum scripts/mesh_task_log.py ~/.local/bin/mesh_task_log.py
4c47f31e69090b65dcd693526608441a1e55d39dfe026d9b7caeb9103e18f839  both files
```

The live `mesh-task audit` then showed:

```text
RUNNING  witness  autopoiesis-task-ledger-20260908/verify-origin-continuity
```

The readable ledger implementation is therefore both tested and deployed, and
the current task remains attributable to this verification step until its
artifact is committed through the required board completion transition.

Verdict: **verified**. No code change was required.
