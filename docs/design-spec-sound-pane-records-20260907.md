# Sound pane records disposition — 2026-09-07

## Status

`REJECTED FOR CLOSURE` with owner `tg`; the audit produced the requested
receipts, but the live reflex cadence still contradicts the governing design.
No synthetic or production sound mutation was performed. The governing design is
`docs/superpowers/specs/2026-07-15-sound-pane-records-reflex-design.md`.

## Evidence captured 2026-09-08

- `bash scripts/mesh-records --test`: rc `0`, output SHA256
  `88ad129e48594122b8b5f09a6e472643e76f9054d223b05ffe193af53881f256`;
  the test measured a real 14-second WAV and exercised concurrency/retention
  assertions.
- `timeout 120 bash scripts/mesh-sound-reflex --test`: rc `0`, output SHA256
  `61e7d6a3f58ead5b7ff9483368d8e69ca1bc6751058f13cfdd3cce318a5b49df`.
- Persistent playable render:
  `/home/mesh-home/.mesh/records/20260908-105347-ext-2c041412.mp3`, size
  `2514563`, duration `186.279184s`, SHA256
  `72e3979041a459f2974170b1b907677b23120ab578d1b23fe39e5e9635413183`;
  `ffprobe` identified `format_name=mp3` and full `ffmpeg` decode returned rc
  `0`.
- Source and deployed copies are the same symlinked files. Current source
  SHA256: `mesh-records`
  `593e6c111d7cf4f3f12d844a46ed4a914718808c1219eae4a697ab565743315a`;
  `mesh-sound-reflex`
  `961cf126db158bbc3ea74a5fac00612333e2e09c8f1c45e10bfc0b3533b5ea20`.
- Live crontab wiring is `mesh-records` at `*/2` and
  `mesh-sound-reflex` at `*/10` (with `mesh-load-gate`), while the governing
  design requires the reflex at `*/5`.
- Live `mesh-sound-reflex --status`: ledger `2131` lines / `171` pending;
  anchor `94ddd63c`; corpus `4090` renders / `127` distinct recipe cells;
  all five per-factor spreads report `live`.

## Missing / contradictory requirement

- per-step owner checklist with DONE/BLOCKED/DECLINED outcomes;
- a settled ledger row for the current audit itself (the live tail remains
  `-> pending`); and
- resolution of the `*/10` live wiring versus `*/5` design contract.

## Retry gate

To reopen, decide whether the live cadence should be changed to `*/5` or the
design should be amended, then capture a settled ledger row after that decision.
Do not treat the otherwise valid receipts above as proof of conformance.

## Independent recheck

- Owner design spec SHA256: `6279f7806fdb5c036db91b0c7395abdfee5cfc65ce3084d32003d81ffdce6f42`.
- `bash scripts/mesh-records --test`: rc `0`, output SHA256
  `c9449637b63fd262daf61243e82b232567d258b9f14aef4f533cd401cebecb80`;
  the test measured a real 14-second WAV.
- `bash scripts/mesh-sound-reflex --test`: rc `0`, but the independent output
  hash is redacted, so this is not sufficient as a reproducible owner receipt.
- Source/deployed hashes match: `mesh-records`
  `593e6c111d7cf4f3f12d844a46ed4a914718808c1219eae4a697ab565743315a` and
  `mesh-sound-reflex`
  `52cdb2a49fe7660efea9ec08e5643c260f37b77beb99ed5212860d70a1a1614f`.
- Live wiring is records `*/2` and sound-reflex `*/10`; the design calls for
  `*/5`. This cadence mismatch is explicitly unresolved and is not silently
  treated as equivalent.
- No persistent playable recording/MP3/WAV was found under `/home/mesh-home/.mesh`
  or `/tmp`, so no valid recording hash exists yet.

## Current disposition

`REJECTED FOR CLOSURE`: the requested evidence classes now exist, but closing
the task would claim a design-compliant reflex while the live wiring remains
`*/10` and the design says `*/5`. Exact next action: owner/board must choose
the cadence contract, then rerun wiring verification and settle the ledger row.
