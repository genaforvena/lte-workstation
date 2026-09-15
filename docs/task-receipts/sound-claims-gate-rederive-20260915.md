# Sound claims gate re-derivation — 2026-09-15

## Evidence

- UTC run: `2026-09-15T23:29:54Z`
- Corpus: `/home/mesh-home/.mesh/records.log`
- Corpus metadata: `665191 bytes`, mtime `2026-09-15 23:29:51Z`, `2429` lines
- Command: `mesh-series-stats --claims`
- Command exit: `2`
- Source reported by the command: `2429 rows`; ROM: `series-stats.rom`

The command explicitly says the corpus is pruned per organ and that `n` moves both ways; no
standing number below is treated as durable without another live run.

## Live verdicts

1. Claim 2 (`act` never exceeds `.544`): `UNKNOWN`. The current `n=2350` exceeds the ROM domain
   `2343`; the tool refused stats and did not silently window the data.
2. Claim 3 (live medians `dyn .265 / act .319 / move .141`): `UNKNOWN` for all three axes for the
   same ROM-domain overflow (`n=2350 > 2343`). The old medians are not revalidated.
3. Claim 1 (score/rhythm relationship): `INDISTINGUISHABLE`. Live means are `13.56` beats for
   score>=55 and `11.37` for score<55; difference `-2.190`, 95% CI `[-6.554,+2.175]`. Density is
   `1.01x`, and the tool identifies a window-length artifact; neither direction is supported.
4. Claim 4 (sub-window beats never exceed whole-file beats): `REFUTED`. `302/1640` rows violate
   the relation (`18.4%`); `278/302` violations are among `327` degenerate whole-file scans
   (`fbeats=1`). The note3 arm accounts for `298/459` violations (`64.9%`).

## Bounded decision

The claims gate remains failed (`rc=2`). Keep claim 2 and all three axes of claim 3 explicitly
unknown; keep claim 1 unendorsed; keep claim 4 audit-only and refuted. This receipt changes no
ranker, estimator, or gate. Next trigger: rerun after a corpus/ROM-domain change or a new claim
audit that either supplies a non-windowed live calibration or isolates the non-degenerate claim-4
population.
