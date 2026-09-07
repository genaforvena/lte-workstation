# Job communication repair — 2026-09-07

## Reproduction

The live board recorded the operator request as `[task] ... owner: job` at
`2026-09-07T08:38:13Z` (board evidence: `~/.mesh/chat.log`, line 2970). At
08:39:08Z `mesh-mind-control` reported `owner window ABSENT ... falling through to generic pick`,
then dispatched it to `genome` at 08:39:15Z. Job did not receive the task; its adjacent status
posts were audits and handoffs. This is a concrete request → board → dispatch → wrong owner break.

The same evidence includes an operator interview-list ask and several follow-up acknowledgements.
The promise ledger correctly keeps uncited asks open: `SPOKE`/TG adjacency is explicitly not
completion; only a citation such as `ask:<arrival-id>` discharges an ask.

## Change

`scripts/mesh-mind-control`: an explicit owner that resolves ABSENT is now a visible retryable
hold (`rc=3`). It never enters `_pick_agentic`, so a neighbouring mind cannot inherit Job’s exact
key or have an adjacent `[done]` mistaken for completion. The task remains open until the named
owner/channel is available.

`tests/test-job-dispatch-ownership.sh` is a deterministic wiring gate. It asserts the no-generic-
fall-through branch, runs the resolver suite and the promise suite, and checks Job’s concrete
assignment contract: confirmed-only, employer/role/time/participants/link-or-place/source, proposed
rows excluded, and machine-owned `needs-human` handling.

## Verification

`bash tests/test-job-dispatch-ownership.sh` — PASS.

Also independently run: `bash scripts/mesh-mind-control --test` — PASS; `bash scripts/mesh-promises
--test` — PASS; `python3 job/mesh-job-cal --test` — PASS.

## Remaining limitations

The currently live `owner: job` request still needs a healthy Job channel/dispatch target; this fix
holds it rather than silently substituting another mind. The end-to-end employer-mail/browser
organs remain outside this narrow routing change. A true unavailable organ must continue to be
recorded as durable `needs-human`/degraded evidence, while independent branches continue.
