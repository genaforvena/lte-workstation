# Unattended warning sweep — mesh-chat-deliver — 2026-09-08

Task: `witness-mesh-chat-deliver-sweep-20260908/unattended-warning-sweep`
Owner: `witness`
Audited: 2026-09-08T15:31Z (UTC), `mesh-home`

## Live-task and instruction check

The task was live and correctly specified at the start of this sweep. The
ledger showed it `QUEUED`, then owner-authored `taking` changed it to active
with a lease through 2026-09-08T16:01:53Z. The predecessor delivery audit was
done with artifact
`docs/witness-mesh-chat-delivery-audit-20260908.md`; its recorded discrepancy
was independently reproducible from current files, so this task was not stale
and was not rejected.

## Signals and dispositions

| signal | current evidence | disposition |
|---|---|---|
| Misleading delivery-failure attempts count | 405 current `[delivery-failed]` board lines say `attempts:3`; live ledger has 447 failed rows distributed as attempts `0:405`, `1:25`, `2:5`, `3:12` | Actionable. Routed exact corrective implementation task to `genome`: preserve actual attempted-delivery counts and distinguish them from age/idle expiry; do not close until a per-message or otherwise unambiguous failure artifact and regression test exist. |
| Delivery reflex coverage | `crontab -l` has `* * * * * $HOME/.local/bin/mesh-chat-deliver >> $HOME/.mesh/chat-deliver.log 2>&1`; cron is active; source and deployed SHA-256 both equal `aa18b68f654f6e91a85eb801c20636da75d906d6caba682bc739161e129b4907` | Covered; no duplicate reflex added. |
| Health/warning-to-task coverage | `crontab -l` has the live `mesh-health-warning-task` entry; its existing reconciliation artifact records five exact health-warning keys with owner taking/blocked evidence | Covered and previously reconciled; no duplicate task created. |
| Unattended raw `[warning]`/`[alarm]`/`[error]` records | Fresh `chat.log` scan found 0 raw `[warning]`, 0 `[alarm]`, and 0 `[error]` markers outside the existing structured delivery/health records | No additional task. |

The delivery-failure signal is not silently closed: it remains open under the
owner-routed corrective task below. The age limit is 900 seconds and the
configured maximum is 3, but a terminal record saying `attempts:3` is false
for the 405 zero-attempt rows and ambiguous for grouped rows.

## Exact owner-routed corrective task

Created and dispatched:

`witness-mesh-chat-deliver-attempts-correction-20260908/fix-attempts-field`

Owner: `genome`.

Required acceptance: update `scripts/mesh-chat-deliver` and its deployed copy
through the normal land/deploy path so terminal delivery-failure evidence
reports actual attempts per message (or an explicitly per-message mapping),
keeps age/idle expiry distinct from attempted delivery, adds a regression for
zero-, one-, two-, and three-attempt rows plus grouped failures, and verifies
source/deployed identity and the live cron path. Existing historical ledger
rows must not be rewritten as if they had attempts.

## Verification performed

The following current-state checks passed:

```text
scripts/mesh-chat-deliver --test
mesh-chat-deliver smoke-test ok (stable message id, terminal controls, bounded ledger contract)
bash tests/test-mesh-chat-deliver.sh
PASS (3 attempts, one failure edge, terminal ack, spaced terminal ack, duplicate suppression, fresh id reopen)
python3 tests/test-mesh-health-warning-task.py
PASS
systemctl is-active cron
active
```

Fresh evidence inputs:

```text
chat.log lines: 38868
chat.log sha256: c1f2ba59800c70b07a7fc90eccb6cb34ec432faf82101984d189712148cccc45
ledger messages: 1359
ledger status counts: acked=852 failed=447 expired-preledger=31 pending=27 awaiting-ack=2
failed-attempt counts: 0=405 1=25 2=5 3=12
```

Conclusion: reflex wiring is covered and healthy; one actionable evidence
defect was converted into the exact owner-routed task above. No raw warning or
error signal was left without a disposition.
