# Telegram delivery receipt — chat.log last 12 hours

- Source ask key: `tg-c6745afaa7a6fa2b892ce1ef`
- Task: `operator-intake/c6745afaa7a6fa2b892ce1ef/reconcile`
- Source message: `/home/mesh-home/.mesh/voice-in.log:1302`, received `2026-09-16T01:39:00Z`
- Export: `/home/mesh-home/.mesh/operator-exports/chat-last-12h-20260916.txt`
- UTC selection: `2026-09-15T13:39:00Z` through `2026-09-16T01:39:59Z`
- Source rows: `3528`; export rows including four metadata lines: `3532`; bytes: `4131942`
- Export SHA-256: `56e26a449402805af7efe1652cfbb6789819e980bc9b3ad7978102f08c8b91c7`
- Destination: operator Telegram via `mesh-tg --file` / Telegram `sendDocument`
- Transport receipt: command returned `sent to operator TG: chat-last-12h-20260916.txt (sendDocument)` at `2026-09-16T01:40:38Z`
- Verification: export exists, is non-empty, hash rechecked, and transport command reported successful delivery.

