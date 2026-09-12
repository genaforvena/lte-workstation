# Persona/code corpus reconciliation — 2026-09-12

## Decision: `insufficient-data`

The existing persona/code run does not meet the operator-ideas contract's corpus or held-out gates.
Do not use these adapters as evidence of learned operator style or repository culture, and do not
propose retraining from this corpus. The digest-pinned counts and findings are in
[`tinyfleet-persona-code-reconciliation-2026-09-12.json`](tinyfleet-persona-code-reconciliation-2026-09-12.json).

The audit found 12 persona and 10 code training rows. Every row is marked synthetic, and the runner
builds them from hard-coded seed lists; the measured Telegram and operator-field files are not read
to construct examples. The corpus therefore contains no attributable operator-authored style data.
Persona seed examples also combine style cues with mesh vocabulary and operational claims, without
a separate factual-recall set.

The four-row held-out set in each domain has one unique normalized text repeated four times. All
train and held-out rows share the same generated date. Their `source_id` fields are unique across
splits but are generated from the split name and row ordinal, so zero ID overlap is only syntactic;
it does not establish independent conversations, time buckets, speakers, source files, or code
blobs. Code rows have no repository file/blob, license, or snapshot reference. The old manifest's
`redacted: true` flags do not repair these provenance and independence gaps.

Existing behavior has a separate evidence integrity issue: the current `eval-all.json` digest does
not match the digest recorded in the 2026-09-07 verification note. The reported evaluation scores
cannot be attributed to the currently pinned evaluation file without a fresh reconciliation.

No raw message, voice, or code sample is copied into this decision. Existing run artifacts report
two NUL-corrupt operator-field lines rejected by the builder; differing operator-field hashes across
the saved measurements also show that these measurements are not a frozen source boundary.

Verification performed: recounted all six JSONL datasets and recomputed their SHA-256 digests;
checked normalized held-out duplicates, source-ID/text overlap, provenance flags, source-file fields,
and generated dates; confirmed the corpus-builder logic uses synthetic constants; and ran
`/home/mesh-home/tiny-fleet/.venv/bin/python scripts/persona_code.py self-test` (`self-test: ok`).
No training or raw-content export was performed.

Next: resolve `tinyfleet-promise-gaps-20260912/reconcile-spoken-style-source`. Only a permitted,
source-backed dataset with immutable source/time/file provenance and genuinely independent held-out
families can reopen the data-adequacy decision.
