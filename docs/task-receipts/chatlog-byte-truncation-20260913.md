# Chat and generation log UTF-8 boundaries — 2026-09-13

Task: `chatlog-byte-truncation-20260913/fix-byte-based-truncation`

The board summary writer was already corrected in `scripts/mesh-handoff` by commit `76693598`:
its `cut -c1-240` was byte-oriented and is now `_utf8_head 240`. The regression fixture exercises
that real writer through the raw-append fallback with 239 ASCII characters followed by `я` at the
boundary.

The remaining live defect was in `scripts/mesh-generate`. Its prune diagnostic used `head -c 60`,
and other `generate.log` previews used Bash substring lengths, which split UTF-8 under `LC_ALL=C`.
The fixture failed before the fix with a strict-decoding error on byte `0xd1` in both cases: the
prune preview and the generated-task preview. The source now routes all four truncated diagnostic
previews through a Python Unicode-character slicer. Invalid UTF-8 queue text fails visibly before
the corresponding queue/backlog mutation.

The regression is wired into `scripts/mesh-generate --test` as
`tests/test-mesh-chat-generate-utf8-boundaries.sh`. It tests prune and generation previews under a
forced C locale and the board summary through `mesh-handoff`; all fixture logs are decoded with
Python's strict UTF-8 decoder. It uses temporary homes and does not modify live history.

Verification:

- `scripts/mesh-generate --test` — PASS, including both multibyte boundary arms.
- `scripts/mesh-handoff --test` — PASS.
- `bash -n scripts/mesh-generate tests/test-mesh-chat-generate-utf8-boundaries.sh` — PASS.
- `git diff --check -- scripts/mesh-generate tests/test-mesh-chat-generate-utf8-boundaries.sh` — PASS.
- Full strict UTF-8 reads after landing: `~/.mesh/chat.log` (60,625 lines, 55 U+FFFD repair markers)
  and `~/.mesh/generate.log` (20,067 lines, 57 U+FFFD repair markers) — PASS.
- Historical logs were not rewritten or truncated.

The focused test landed first as `49d83334`; the generator landed and deployed second as `22aea028`.
Both commits are synchronized with `origin/main`. Source and deployed `mesh-generate` SHA-256 are
`492a54a1dc1f2825733ad52a29ebd86c8a158d7ab97588491288b40cfecf0db5`; installed
`~/.local/bin/mesh-generate --test` passes.
