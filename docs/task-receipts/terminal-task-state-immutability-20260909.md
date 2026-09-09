# Terminal task-state immutability receipt — 2026-09-09

## Incident and safe recovery

The authoritative `/home/mesh-home/.mesh/chat.log` chain
`ask-answer-funnel-implementation-20260907` contains the original immutable terminal
receipt at revisions 14 and 15:

- status `complete`, current step `final-funnel-verification`, step status `done`
- finished `2026-09-09T19:06:35Z`
- artifact `docs/task-receipts/final-funnel-verification-20260909.md`
- artifact SHA-256 `3c329e169d4b47553d28a18e57cc5b04041f84b24ba9439ff7f4d4a36005db06`

Revision 16, appended at 19:08 by TG, attempted to replace that receipt with
`status=blocked`, `step.status=blocked`, and the stale terminal artifact reference.
Revision 17 restored the exact DONE terminal snapshot. Chat history was not rewritten.

Replay now treats a postterminal regression or mutation in historical append-only data as
quarantined evidence: it keeps the last valid terminal snapshot, allows unrelated chains to
replay, and accepts a later identical terminal receipt. A fresh append of such a regression is
still rejected before writing. Rebuild materializes only the canonical valid snapshot and does
not overwrite an equal existing cache; the invalid historical bytes remain preserved in chat.log.

## Implementation and verification

- `scripts/mesh_task_log.py`: terminal transition validator at replay and append boundaries;
  historical invalid terminal successors are skipped from the canonical projection.
- `scripts/mesh-task`: rebuild/cache save preserves bytes when the derived JSON is unchanged.
- Regression coverage: `tests/test-mesh-task-log.py` and
  `tests/test-mesh-task-no-expiry.py`.

Observed verification:

| command | result |
|---|---|
| `python3 tests/test-mesh-task-log.py` | PASS, 19 tests |
| `python3 -m unittest tests/test-mesh-task-no-expiry.py` | PASS, 13 tests |
| `python3 scripts/mesh-task replay --json` against live chat.log | PASS; canonical replay available |
| isolated r1 DONE → r2 BLOCKED rebuild fixture | PASS; cache bytes preserved |
| fresh append DONE → BLOCKED fixture | PASS; append rejected and bytes preserved |

## Witness correction: successor recovery

The first validator revision was too strict: it quarantined TinyFleet's legitimate transition
from revision 7 (`REJECTED`, current `verify-ticket-extraction`) to revision 8 (`BLOCKED`, current
`support-routing`) even though that successor carried `recovery_artifact` and
`recovery_artifact_sha256`. The validator now permits that explicit artifact-backed advance to a
different successor step, while still freezing mutations/regressions of the same terminal step.

After correction, deployed replay returned TinyFleet revision 47 at
`verify-redaction-assistance` (`open`/`open`); it no longer froze at r7. The live chain advanced
during verification, so this is a current observation rather than a fixed expected revision.

Final source/deployed parity:

- `mesh_task_log.py`: `8dc0c39d9b2fd590368c4a00aa716cb77ea844c18debca306acfbdb417996788`
- `mesh-task`: `2ad95bdd55de1932ac0c74e3ebc915e484e663561d8b1c0b1cabc49792dcf669`

Final verification: `test-mesh-task-log.py` 20 tests PASS; `test-mesh-task-no-expiry.py` 12
tests PASS; deployed `mesh-task --test` PASS; deployed live replay PASS.
