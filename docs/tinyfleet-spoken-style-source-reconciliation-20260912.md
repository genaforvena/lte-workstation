# Tiny Fleet spoken-style source reconciliation — 2026-09-12

## Decision: blocked — no publishable source-backed split

The existing operator-style run did not use spoken material. Its pinned manifest lists only the
Telegram corpus and operator-field context as raw inputs. The 12 persona training rows and four
held-out rows are generated synthetic examples; the builder does not read voice transcripts to
construct them. The held-out examples also do not establish independent source or date families.
Do not describe the existing adapter as learned from the operator's speech.

There is a substantial local speech-derived source: the current `~/.mesh/voice-in.log` snapshot has
390 `VOICE` rows (187,987 body characters), alongside 572 `TEXT` rows. Its current SHA-256 is
`1d7fb11e7f348daf1a08aae19ffa50246a97ece0c2d705ddaf19784b5f5a8b5b`; it spans 2026-07-14 through
2026-09-12. These are inventory measurements only. No transcript text, audio, or private sample is
included here.

The source is not ready to turn into a publishable training split. `mesh-voice-rx` labels inbound
transcriptions as `VOICE`, but its writer explicitly falls back to raw log writes when the scrubber
is unavailable or fails. The current log has no per-message source-audio digest, transcription
engine/version, or scrubber outcome, so its file digest cannot prove which rows were redacted or
reconstruct individual source provenance. The existing persona manifest has no voice input,
voice-specific redaction receipt, or source-backed split. Copying selected rows now would silently
assume privacy review and split independence that the artifacts do not establish.

## Existing run evidence

- Plan: `/home/mesh-home/tiny-fleet/docs/persona-and-code-plan-2026-09-07.md` explicitly treated
  voice as future work and excluded raw voice recordings from checked-in data.
- Run manifest: `/home/mesh-home/tiny-fleet/runs/persona-code/manifest.json` records 815 Telegram
  rows and operator-field context, but no voice input.
- Current persona corpus hashes: train `140a4bb1f7e37e7262dd6bec617dfe025b9e85b3b79657613525e50804c32055`
  (12 rows), held-out `3fe342268a542a766f01e76326de9450394086c3c0ce0566486a40ff3fc90632`
  (4 rows), adversarial `3b6c42fe5c67fbb3ac3dbfbbe9cd391b887c1e84a6920cf7d3220f921ca547e8`
  (14 rows). The independent corpus reconciliation already
  found these rows synthetic, duplicated across held-out text, and non-independent by date/source;
  see `docs/reviews/tinyfleet-persona-code-reconciliation-2026-09-12.md`.
- The local voice log is operator-only input by the `mesh-voice-rx` contract. Its ingestion path
  does not provide a durable, per-row redaction-success receipt.

## Unblock criteria

Before training from speech, create a new immutable run snapshot with a source manifest that records
the snapshot digest, stable per-record locators, date/conversation grouping, transcription
provenance, and redaction outcome without copying raw audio or raw private text. Redact and review
each selected derived example for secrets, third-party details, and operational facts; reject rows
whose status cannot be proved. Freeze train/held-out groups by date or conversation, verify no
normalized-text or source-family overlap, and publish only derived examples plus the manifest. Then
have the source/redaction/split evidence independently checked before training.

## Verification

- Read the plan, run manifest, builder, and voice receiver's write path.
- Counted source rows by kind and measured date coverage, byte count, and current SHA-256 without
  emitting transcript contents.
- Recomputed the three checked-in persona JSONL hashes and confirmed their row counts.
- No corpus, model, training run, or raw/private material was changed or copied.
