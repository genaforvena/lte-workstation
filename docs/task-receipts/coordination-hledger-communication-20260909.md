# Communication receipts — 2026-09-09

Task: `coordination-hledger-plan-20260908/communication-receipts`
Owner: `tg`

## Verdict

**FAIL / unresolved**. The completed delivery-attempts correction is present in both source and
deployed `mesh-chat-deliver`, and its focused regression gates pass. The existing ask-answer funnel
dependency is now satisfied: `ask-answer-funnel-implementation-20260907` is `[complete]` (6/6),
including Unit 5 and final verification. However, the live delivery ledger still contains recent
terminal failures and a pending message, so the acceptance requirement “delivered answer or owned,
aged, actionable pending state” cannot be claimed for all sampled inbound messages.

## Verification

Run at 2026-09-09T19:10–19:12Z UTC, read-only except for the required board ACK:

| Check | Result |
|---|---|
| `scripts/mesh-chat-deliver --test` | PASS |
| `bash tests/test-mesh-chat-deliver.sh` | PASS; transient failures recover in 3 attempts; duplicate and terminal ACK controls pass |
| `python3 tests/test-mesh-chat-deliver-attempts.py` | PASS; grouped 0/1/2/3 attempt mapping and distinct age expiry |
| source/deployed SHA-256 | `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd` for both |
| cron wiring | `* * * * * $HOME/.local/bin/mesh-chat-deliver ...`; `cron=active` |
| funnel dependency | PASS; `ask-answer-funnel-implementation-20260907 [complete] (6/6)` |
| required receipt ACK | posted: `mesh-chat --to witness '[ack] ack:fdc09b74a0089cfc'` |

The focused tests prove the corrected per-message attempt evidence and do not rewrite historical
ledger rows. That preservation rule was respected.

## Live ledger evidence

At the audit snapshot, `~/.mesh/chat-deliver-ledger.json` contained 1,693 rows:

```text
status:   acked=1068 failed=582 pending=11 expired-preledger=31 awaiting-ack=1
attempts: 0=573 1=1038 2=58 3=24
terminal_reason: age-expiry=131 attempt-limit=3
```

For 219 non-control records addressed to `tg`, the current tail classification was:

```text
acked=153 failed=60 expired-preledger=4 awaiting-ack=1 pending=1
```

The recent tail included the successor message `fdc09b74a0089cfc` as `awaiting-ack` in the ledger
snapshot taken before the terminal ACK was reflected, plus four recent `failed` rows and one
`pending` row. The board ACK itself is a control receipt; it is not an answer and must not settle
the operator question by itself.

Snapshot hashes:

```text
chat.log:                 cf04e45571c5b85528770cdef0b65c021c40c6d48c324075aed472afe88ce8ae
chat-deliver-ledger.json: e250adfc7bb4b6a515e70790346e24255829bcc0287bb8516f77b83abeb22427
```

## Dependency and canary disposition

The Unit 5 registry and final-funnel receipt were re-read. Unit 4’s actual receipt and Unit 5’s
registry dependency are satisfied; no replacement funnel was created and no synthetic canary was
injected. The explicit operator-only canary rule remains intact.

## Unresolved next action

Reconcile the recent terminal-failure and pending rows against their exact inbound IDs, answer
artifacts, and delivery attempts; retain every historical row and failure reason. Then rerun the
live sample after the ACK has been materialized and produce a fresh receipt. Do not settle this step
until each sampled ask is either linked to a delivered answer artifact or has an owned, aged,
actionable pending record.

## Owner re-emission — 2026-09-09T23:57Z

The overdue owner receipt was re-emitted after witness reminder `msg:d3b47c977af39dbc`.
Required ACK was posted to witness as `ack:d3b47c977af39dbc`.

Fresh live checks at 2026-09-09T23:56–23:57Z UTC:

| Check | Result |
|---|---|
| `mesh-dash --once` | completed; live board still reports this task as overdue with FAIL/pending history |
| `scripts/mesh-chat-deliver --test` | PASS |
| `bash tests/test-mesh-chat-deliver.sh` | PASS; transient recovery, terminal ACK, spacing, duplicate suppression, fresh-id reopen |
| `python3 tests/test-mesh-chat-deliver-attempts.py` | PASS; grouped 0/1/2/3 mapping and distinct age expiry |
| live ledger total | 1,760 rows: acked=1,129, failed=600, expired-preledger=31; pending=0 at snapshot |
| target=`tg` sample | 224 rows: acked=160, failed=60, expired-preledger=4; 5 retained `failed` rows carry `terminal_reason=age-expiry` |
| current artifact state | **FAIL / unresolved**; no terminalization |

Fresh snapshot hashes:

```text
chat.log:                 8c781105b28f9bd3953752300cab192213cefb2b52d56097cfb19cda794c55a1
chat-deliver-ledger.json: d49e5e3768ea38e35bfc126ce4d05955dee773da6a350a22ebaa8d70e3a27e3a
```

The five retained target-`tg` age-expiry IDs are `4b71eceec13455e5`, `06b93f0b2256ccc3`,
`5d28348941116134`, `e9db0c3b3df68217`, and `67d9c53df054176d`. The current snapshot has no
pending row, but the historical terminal failures remain unresolved against the acceptance rule:
each sampled inbound must link to a delivered answer artifact or an owned, aged, actionable pending
record. Next action: reconcile those exact IDs and answer artifacts, then rerun the live sample;
retain all failure history and do not treat ACK as an answer.

## Exact-ID reconciliation — 2026-09-10T01:28Z

The five retained rows were matched against the source board line, the delivery ledger, and the
owner's later artifacts. This retrospective mapping does not rewrite a failed delivery into a
success.

| failed message ID | inbound question / task line | delivery row | later owner artifact or state | disposition |
|---|---|---|---|---|
| `4b71eceec13455e5` | 18:01:20Z witness asks to preserve and repair the Unit 5 minds/forage blocker | `failed`, `attempts=0`, `terminal_reason=age-expiry`, `failed_at=18:17:31Z` | `docs/ask-answer-funnel-unit-5-canary-reconciliation-20260909.md`; resolver `docs/task-receipts/unblock-tg-e482cf8ce268827e-resolve-20260909.md` | owner answered later on the board and produced artifacts; failure retained |
| `06b93f0b2256ccc3` | 18:06:07Z witness FYI about the HELD_REJECTED renderer edit | `failed`, `attempts=0`, `terminal_reason=age-expiry`, `failed_at=18:22:27Z` | owner answer `docs/task-receipts/resolve-06b93f0b2256ccc3-20260910.md` | resolved by one-to-one owner artifact; delivery failure retained |
| `5d28348941116134` | 18:11:27Z witness asks to continue exact resolver `unblock/tg/e482cf8ce268827e/resolve` | `failed`, `attempts=0`, `terminal_reason=age-expiry`, `failed_at=18:27:28Z` | `docs/task-receipts/unblock-tg-e482cf8ce268827e-resolve-20260909.md`; resolver DONE at 18:31:41Z | owner answered later and produced a terminal artifact; failure retained |
| `e9db0c3b3df68217` | 18:17:28Z witness repeats the active resolver instruction | `failed`, `attempts=0`, `terminal_reason=age-expiry`, `failed_at=18:33:21Z` | same resolver receipt; Unit 5 resumed and later reached DONE | owner answered later and produced a terminal artifact; failure retained |
| `67d9c53df054176d` | 18:37:03Z witness asks TG to take and close final-funnel verification | `failed`, `attempts=0`, `terminal_reason=age-expiry`, `failed_at=18:54:32Z` | `docs/task-receipts/final-funnel-verification-20260909.md`; later BLOCKED/DONE corrections remain in board history | owner answered later and produced artifacts; failure retained |

Current live re-scan at 2026-09-10T01:28Z: ledger `acked=1136`, `failed=600`, `pending=1`,
`expired-preledger=31`; target `tg`: `acked=162`, `failed=60`, `expired-preledger=4`,
`pending=0`. The five IDs remain in the 60 historical target-TG failures. Snapshot SHA-256:
`chat.log=caec980c319f3dbe58797841ad59b627fd7d445e99354d0d06368c6d7ccd9478`,
`chat-deliver-ledger.json=c51dd91e095122fd8ffaa1f40398a2e055ca0917706f381ddf2e900b9ea9f46d`.

Focused checks rerun: `bash tests/test-ask-answer-funnel-unit-2-remove-inference.sh` PASS,
`bash tests/test-mesh-dash-ask-resolution.sh` PASS, and `mesh-task --test` PASS. The communication
At the 01:28Z snapshot the step was **FAIL / unresolved** because ID
`06b93f0b2256ccc3` had no one-to-one owner answer. That historical verdict and
all delivery failures remain preserved; the resolution update below supersedes
the unresolved disposition.

## Resolution update — 2026-09-10T01:34Z

Owner `tg` answered exact ID `06b93f0b2256ccc3` with
`docs/task-receipts/resolve-06b93f0b2256ccc3-20260910.md`. The artifact
addresses the exact 18:06:07Z HELD_REJECTED renderer FYI, records acceptance and
independent verification, and does not rewrite the historical `age-expiry` row.

Fresh live `target=tg` sample: `rows=227`, `acked=162`, `failed=60`,
`pending=0`, `expired-preledger=4`, with all five retained age-expiry IDs still
present, including `06b93f0b2256ccc3`. The exact-ID acceptance gap is resolved;
the five historical delivery failures remain preserved as failure evidence.
