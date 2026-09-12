# Sound pane records disposition — 2026-09-07

## Status (as audited 2026-09-08)

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

## Disposition at audit time (2026-09-08)

`REJECTED FOR CLOSURE`: the requested evidence classes now exist, but closing
the task would claim a design-compliant reflex while the live wiring remains
`*/10` and the design says `*/5`. Exact next action: owner/board must choose
the cadence contract, then rerun wiring verification and settle the ledger row.

## Resolution (2026-09-12)

The cadence contract is resolved from the existing operator-approved implementation
change, rather than changing the live schedule. Commit `4fe555866` (2026-07-20,
"window-set-consolidation: ... sound-reflex */10") records the operator-approved
move from `*/5` to `*/10`. The script declares `*/10`, its coverage-slot constant
is 600 seconds, and live cron runs `mesh-sound-reflex` at `*/10` behind
`mesh-load-gate --quiet-hours sound-reflex 11`. The governing design now documents
that contract. A 14-minute render previously wedged multiple `*/5` ticks while
holding the lane lock, and the load gate may stretch the interval further; coverage
remains based on actual evaluations and missed intervals are not claimed as samples.

| Requirement | Outcome | Evidence |
|---|---|---|
| Resolve design/live cadence conflict | DONE | Governing cadence section; approved change `4fe555866`; source declaration and live cron both `*/10` |
| Exercise the records archivist | DONE | `scripts/mesh-records --test` rc 0; measured and archived a real 14-second WAV |
| Exercise the sound reflex | DONE | `scripts/mesh-sound-reflex --test` rc 0 |
| Verify source and deployed wiring | DONE | `mesh-records` SHA-256 `593e6c111d7cf4f3f12d844a46ed4a914718808c1219eae4a697ab565743315a`; `mesh-sound-reflex` SHA-256 `030160982a5f9324b68a9677c728e32a0d6ddc27b5afae004dcdb8361324ce44`; scripts resolve to deployed paths; cron lines 142/144 are `*/2` and `*/10` |
| Verify a fresh quiet-window reflex output and provenance | DONE | `unblock-tg-bc9722e64e8166d4-resolve-20260912.md`: playable MP3 SHA-256 `5864126586e816ead1ffd519b4747bfd3c1187a9e4fd7f1dc73f0119a1982ed5`, full decode rc 0, matching records and params ledger rows |
| Settle this audit in the task ledger | PENDING | Close the active owner task with `mesh-task done` after this receipt is finalized |

No live cron or sound-producing state was changed in this resolution. After the final
task-ledger settlement, replace the last `PENDING` outcome with its settled row ID and
record the resulting receipt hash.
