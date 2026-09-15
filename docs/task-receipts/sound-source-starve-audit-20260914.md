# Sound source-starvation gate audit — 2026-09-14

Task: `sound-source-starve-audit-20260914/audit-source-starve-gate` (owner `sound`).

## Finding

Keep the gate and quiet-hours wiring unchanged. The live diversity measurement still identifies an
ext-only lane, while the grinder and scanner were held by quiet-hours in the 01:14Z sound pane. A
manual render would either duplicate pending grinder work or bypass the source-specific recipe and
load gate. The next decision point is the first load-gate-admitted `mesh-sound-reflex` evaluation:
check whether its source-starvation tiebreak promotes a present non-ext record and whether that
promotion becomes a lane render.

## Evidence

- `mesh-dash --once sound` at `2026-09-14T01:14:06Z`: grinder and scanner HELD by quiet-hours;
  last real run 33 minutes earlier; no grind in flight; renders SOURCE-STARVED, `ext 4/4` over the
  1h30m window with seven distinct parameter combinations. The current inbox has no pending drops.
  The corpus has 272 pending records; ear has 70 records / 6 ground in-window, note3 12 / 5, and ext
  40 / 16. Those records are already queued for the reflex, so manually rendering one would duplicate
  lane work.
- `mesh-room-music --diversity` during this audit: `SOURCE-STARVED — ext is 4/4 of last 4
  lane render(s) (params fine: 7 distinct combo(s)) · organs: ext 4 · source: ext 4/4 · same-source:
  ext · window 1h30m`; exit 1, the expected alarm verdict. The latest ext-bearing parameter rows are
  `2026-09-14T00:18:41Z`, `00:30:07Z`, and `00:57:19Z`; the source-mix calculation is taken from
  lane-tagged rows rather than every line in the shared parameter log. The four ext rows supplying
  that verdict are `2026-09-13T23:26:45Z src=ext/ca5ebe5f`, `2026-09-14T00:18:41Z
  src=ext/517bf74d`, `00:30:07Z src=ext/6d1ed082`, and `00:57:19Z src=ext/55ce4f07`. The first-to-last
  span is 1h30m34s, displayed by the tool as 1h30m; the intervening collage rows are not organ rows
  in the source-share calculation.
- The only sound experiment chain, `sound-experiments-20260908`, is complete (10/10). Before this
  audit task was created, `mesh-task queue --dispatch --owner sound` was empty and replay showed no
  open, claimed, blocked, or queued sound steps.
- Quiet-hours wiring is present in `~/.mesh/reflexes.cron:144`:
  `*/10 * * * * ... mesh-load-gate --quiet-hours sound-reflex 11 && ... mesh-sound-reflex`.
  The starve tiebreak runs in the reflex; the starved edge is held only when that same evaluation
  promoted an alternative, and its own log counts those evaluations up to 2. The recovery edge is
  held for four healthy evaluations. Its code and messages report evaluations as points, distinguish
  holes inside the streak from the gap after it, and call a streak with no missed slots clean.
- Live starved-edge state is `starved`; the state file was refreshed at `2026-09-14T00:40:02Z`.
  The starve-deferral counter is 0 and its ledger's newest held edge is `2026-09-07T20:20Z` at 2/2.
  No current starved hold is in progress. The last delivered starved note is `2026-09-08T22:00Z`;
  the durable notable log itself was last written `2026-09-13T11:40Z`. The state file's mtime is a
  per-evaluation liveness stamp, not evidence of a new delivered edge.
- The unstarve counter is 0 and was reset at `2026-09-13T23:30:03Z`; there is no active recovery
  streak. Its held-edge log ends at `2026-09-11T06:50Z`, a 3/4 evaluation with a 601s step gap and
  one unobserved slot already inside that streak. The last delivered recovery note is
  `2026-09-08T08:50Z`: four healthy evaluations over 60 minutes, with three slots unobserved inside
  the streak, explicitly not a continuous interval. There is no basis to call the current period a
  clean recovery or a current streak.

## Commands and verification

- `mesh-dash --once sound`: exit 0; one-shot pane evidence above.
- `mesh-series-stats --claims`: exit 1; live standing-claim gate remains REFUTED/MIXTURE/
  INDISTINGUISHABLE. This audit did not edit those claims.
- `mesh-task status sound-experiments-20260908`: complete, 10/10.
- `mesh-task check dispatch sound-source-starve-audit-20260914/audit-source-starve-gate sound`:
  exit 0; task claimed as `sound`.
- `mesh-room-music --diversity`: exit 1, expected for the current SOURCE-STARVED verdict.
- No code, quiet-hours setting, gate threshold, record verdict, or render log was changed by this audit.

## Decision and next trigger

No retune is justified: the detector names the ext monoculture and the current available material is
already queued behind a deliberately held actuator. On the first run admitted by quiet-hours, verify
the tiebreak's selected organ and whether its record reaches a render. If a tiebreak is held, read its
own evaluation count; if recovery is held, keep the streak, internal holes, post-streak delivery gap,
and clean streak as separate states. Reassess only after that evaluated-run evidence exists.
