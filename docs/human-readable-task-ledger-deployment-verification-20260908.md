# Human-readable task-ledger deployment verification

At 2026-09-08T10:45Z, the live runtime was deployed from the genome:

| runtime | deployed path | source SHA-256 | deployed SHA-256 |
|---|---|---|---|
| mesh-task | `~/.local/bin/mesh-task` → `scripts/mesh-task` | `d6b7f1dc1fc802e389cea033916e88434e5dedf9c6da9fc86395b8f40ae437ae` | `d6b7f1dc1fc802e389cea033916e88434e5dedf9c6da9fc86395b8f40ae437ae` |
| mesh_task_log.py | `~/.local/bin/mesh_task_log.py` → `scripts/mesh_task_log.py` | `8e96ddb142620a95e7c792e1653cf8a0724ecf15e93d33e1f695661561703947` | `8e96ddb142620a95e7c792e1653cf8a0724ecf15e93d33e1f695661561703947` |

Verification:

- `python3 scripts/mesh-task --test` — PASS.
- `~/.local/bin/mesh-task --test` — PASS.
- `python3 -m py_compile scripts/mesh-task scripts/mesh_task_log.py` — PASS.
- Fixed lowercase live chain `human-readable-task-ledger-live-canary-20260908-1048` completed create → take → done. Its new `chat.log` suffix (lines 37022–37030) contains `[task-ledger]` revisions 1–5 and zero `[task-state]` or `plist64:` markers.
- Existing `human-readable-live-probe-20260908` independently confirms deployed create output with `[task-ledger]` revisions.

The attempted uppercase timestamp slugs were rejected by the existing scrubber because token-shaped `T`/`Z` are intentionally redacted. No scrub rule was weakened.
