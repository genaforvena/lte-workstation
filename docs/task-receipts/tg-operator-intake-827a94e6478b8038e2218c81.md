# Operator intake reconciliation: `827a94e6478b8038e2218c81`

Task: `operator-intake/827a94e6478b8038e2218c81/reconcile`
Source: `/home/mesh-home/.mesh/voice-in.log:1332`
Source timestamp: `2026-09-16T11:13:24Z`

## Evidence

The source row is:

```text
2026-09-16T11:13:24Z  VOICE  [voice: local transcription exceeded its 405s budget for a 115s note and cloud STT was unavailable — your note was NOT empty; please resend as text if urgent]
```

`sha256sum` of the exact row without its trailing newline is
`827a94e6478b8038e2218c8140de9dea76f939b1e4b2f114193809dd83584914`; the required prefix matches
`827a94e6478b8038e2218c81`. The row proves a non-empty operator voice note existed, but it does
not contain the note's words. No source audio artifact keyed to this intake was found in the
durable intake record; nearby `.mesh/records` files are continuous ear recordings and are not
identified as this Telegram note.

The later operator text at `2026-09-16T11:18:26Z` is a follow-up about Ollama ownership, and the
later replies address that follow-up. They are not a verified transcription or delivery of the
unrecoverable 11:13 voice note. No transport receipt exists for a reply to the voice note itself.

## Disposition

This reconciliation is complete as a coverage-gap finding; no message is resent because the
original request content is unavailable and repeating side effects would be unsafe. The durable
corrective task is:

`operator/voice-intake-recovery-20260916/implement-lossless-voice-retry` — owner `genome`,
status `open` at creation. It requires retaining the original voice artifact before STT, bounded
retry with explicit `UNKNOWN`, an exact retry receipt/task, and red/green live-caller verification.

The current reconciliation design is reliable for proving that an input was received and avoiding
duplicate side effects, but not reliable enough to prevent this pain: it records a digestible
failure notice after the content has already been lost. The corrective task is therefore required
before this class of request can be considered durably handled.

Delegation: read-only source/receipt search was delegated to `tg-reconcile-827`; this receipt and
its digest/ledger mapping were independently inspected and verified by `tg`.
