# Wake coordination repair — final verification (2026-09-08)

Chain: `wake-coordination-repair-20260908`.

## Disposition

| step | result | artifact |
| --- | --- | --- |
| `promise-identity-integrity` | canonical task-key replay and malformed free-text rejection verified | `docs/wake-coordination-promise-identity-20260908.md` |
| `blocked-chain-independent-progress` | rejected unsafe inferred in-chain parallelism; independent work must use another chain | `docs/wake-coordination-blocked-chain-20260908.md` |
| `receipt-race-reconciliation` | serialized receipt/state transitions; stale recovery waits, reloads, and withdraws | `docs/wake-coordination-receipt-race-20260908.md` |

The receipt-race review initially found a liveness regression in the first
repair: a directory-wide lock also held `status` and `audit`. The final version
locks only mutating commands. The deterministic fixture now proves both that a
read-only `status` completes during a deliberately held owner receipt and that
a concurrent `reschedule` waits, then refuses the newly active row without a
stale yield or duplicate `[task]`.

## Verification

At 2026-09-08T03:02Z:

```
$ bash tests/test-mesh-task-reschedule.sh
test-mesh-task-reschedule: PASS (sent/unclaimed recovery and receipt race preserve exact owner claim)

$ python3 scripts/mesh-task --test
mesh-task: smoke-test ok (canonical ask/task, exact owner, lease/progress,
typed block/resume, artifact hash, idempotent done)

$ bash tests/test-mesh-task-dispatch-receipt.sh
test-mesh-task-dispatch-receipt: PASS (initial dispatch carries exact take command)

$ bash tests/test-mesh-witness-lifecycle.sh
test-mesh-witness-lifecycle: PASS (adint/tiny-fleet/job alerts, blocked hold, dedup)

$ python3 -m py_compile scripts/mesh-task
$ git diff --check
$ cmp -s scripts/mesh-task ~/.local/bin/mesh-task
$ ~/.local/bin/mesh-task --test
```

All commands above passed. `mesh-task audit` showed this chain's first three
steps `DONE` with the artifact paths above and this final step `RUNNING` before
its settlement. `mesh-promises --check` returned zero and its replay/count
agreement passed (`promises=53`, `claims=7`, `holds=27`, `asks=45`); it also
reported one pre-existing `liabilities:promises:unrouted:next` item, which is
not owned or altered by this chain.

## Deployment disposition

Source and installed copies are now byte-identical:

```
cmp -s scripts/mesh-task ~/.local/bin/mesh-task  # exit 0
```

The live witness invokes the installed copy, and its smoke test passes. Deployment
is therefore **verified**. The authorized installer deployed `scripts/mesh-task`
to `~/.local/bin/mesh-task`; source and installed tests both pass.

## Owner receipts and independent live verification

The canonical owner receipt is `[taking]` from `wake` at
`2026-09-08T02:47:34Z`, with lease through `2026-09-08T03:17:30Z`.
The final step remains `active`; no owner `[done]` receipt exists yet, so this
artifact does not claim completion. The live roster has one `wake` window
(`mesh-home:15`) and one `mesh-dash wake` pane. Promise replay shows one open
final-verification identity and no duplicate wake identity.

At `2026-09-08T02:57Z`, an independent live argv check found all 15 active
mind processes, including wake, running:

```
/home/mesh-home/.local/bin/codex --model gpt-5.6-luna --sandbox danger-full-access --ask-for-approval never
```

The independent witness recheck is recorded at
`~/.mesh/audits/witness-wake-final-coordination-recheck-20260908T0256Z.md` and
confirms the artifact hash as it existed at `02:56Z`, the focused tests, source
and installed smoke tests, `mesh-promises --check`, one wake identity, and the
then-pending parity disposition. This final document was then extended with the
receipt and argv evidence above; the independent witness hash applies to the
earlier version, while the final artifact is verified below.
`mesh-dash --test` was attempted with a 12-second bound but did not return
because live network probes remained in flight; this is an unresolved
verification limitation, not a pass.

The final step is ready for settlement after this artifact update and the
owner's task-keyed `[done]` receipt.
