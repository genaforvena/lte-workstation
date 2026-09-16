# pub reply draft — comment 3ej9o

- article: 4633089, “A Failed Voice Path Should Change the Next Call”
- commenter: @raknaos
- source comment id: `3ej9o`
- source observed: `mesh-devto-comments --list`, 2026-09-16
- delivery boundary: `mesh-devto-comments` is read-only; this is a draft for the operator to post. No dev.to write was attempted.

## Proposed reply

That is the boundary we have not measured yet. Our local case only proves the immediate failure path: a failed TTS call writes a 300-second marker, and the next proven event is routed away from the failed path. It does not prove recovery. I would test the three candidates separately: a probe can establish liveness, an opportunistic retry can prove the next real event succeeds, and a timer only proves that the quarantine expired. Until those branches have separate artifacts, “available again” is still an assumption.

## Provenance and delegation

The draft is grounded in the comment text and the local voice-path claim shown by the live `mesh-devto-comments --list` output. Delegated draft worker `pub-reply-draft-3ej9o` failed to accept its prompt; retry worker `pub-reply-draft-3ej9o-retry` also produced no turn, so no worker report was used as evidence. This text was personally authored and inspected in this file.
