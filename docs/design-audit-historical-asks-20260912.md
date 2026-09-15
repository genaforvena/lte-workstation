# Historical ask audit — 2026-09-12

Task: `design-audit-task-sweep-20260907/design-audit-historical-asks` (owner `tg`; dispatch check exited 0 and owner-authored take succeeded).
Sources: `docs/historical-ask-adfox-research-design-20260906.md` and `docs/historical-ask-record-button-design-20260906.md`.

## Dispositions

| Ask | Current evidence and disposition | Durable follow-up |
|---|---|---|
| `20260821T004729Z`, AdFox research | The 2026-09-06 design correctly describes a research contract, not completed work. Existing `self-adint` material substantially answers the auction question, but does not establish that each private observation has the requested URL, retrieval time, query/profile, field list, and raw-response hash. Do not repeat collection while this is reconciled. | `adfox-research-reconciliation-20260912`: `adint` owns a read-only inventory and redacted completeness manifest; `tg` owns the later gap disposition. See `docs/design-audit-adfox-20260912.md` and `docs/plans/2026-09-12-adfox-research-reconciliation.tsv`. No collection is dispatched or authorized by these tasks. |
| `20260821T004511Z`, Granny Keln record button | The 2026-09-06 design note is stale: the phone recording pult and recording path were implemented in `/home/mesh-home/grainneukeln`, pushed, and reported. Treat the original ask as delivered. The phone PWA remains LAN-only; the README says no TLS/rate limiting and forbids port forwarding. | `grainneukeln-phone-apk-deferral-20260912/reopen-native-apk-only-on-operator-ask` is blocked on a fresh explicit operator request. Preserve the delivered PWA; do not build, sign, or distribute an APK or expose the service remotely before that request. See `docs/design-audit-record-button-20260912.md`, `docs/plans/2026-09-12-record-button-deferred-decision.tsv`, and the task chain. |

## Verification

- `mesh-task check dispatch design-audit-task-sweep-20260907/design-audit-historical-asks tg` exited 0; owner-authored take succeeded.
- Read both source designs, their dedicated audits, the follow-up plans, and task status. The AdFox inventory step is assigned to `adint`; the Granny Keln native-APK step is blocked on operator input.
- This reconciliation adds no new collection, product change, APK work, or network exposure. Its dispositions are grounded in the linked audit artifacts; it does not claim to rerun the external app's tests.
