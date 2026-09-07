# Historical scope reproduction receipt — Green Lies continuation

**Run date:** 2026-09-07  
**Purpose:** resolve the count mismatch without silently replacing a published-in-repository
historical measurement with a working-tree scan.

## Decision

The continuation retains the historical tables in `docs/paper/green-lies-taxonomy.md`.
The corpus scope is now locked to the commits below. The 2026-09-07 working-tree scans remain a
dated drift observation, not a replacement measurement.

## Reproduction commands and results

Each system corpus was materialized with `git archive` into a temporary directory. D1 and D2 were
run from the detector version present at their original measurement commits. D3 was run with the
committed detector against the corpus commit named by the source manuscript.

| result | corpus commit | detector | reproduced result |
|---|---|---|---|
| D1 | `0a620fe295f195c40364fa4a1ed4c538772d9be5` (2026-08-20) | detector at same commit | 60 sites; 28 undecidable; 20 decidable boolean gates; 3 vacuous |
| D2 | `e6481f0ebe5fb5563da6d7b9c68d37720ee8953e` (2026-08-21) | detector at same commit | 12,351 `|| echo` sites; 5,693 undecidable; 2,852 ternary/conditional; 3,806 decidable fallbacks; 645 silent; 13 critical; 533 numeric; 391 colliding; 7,613 bare silenced sites |
| D3 | `4ef597078037ea5714c884928875db1e4c6df761` (2026-08-25) | current committed D3 detector | 320 cadence-header tools; 275 undecidable; 11 sample-as-state; 9 honest; 25 full |

For D2, the detector's JSON `decidable=6,658` includes the 2,852 `not-a-fallback` ternary or
conditional sites; the manuscript's 3,806 is the eligible fallback denominator (`6,658 - 2,852`).

The external comparison counts (1,296 files across the ten named public projects) remain the
bounded comparison already recorded in the source manuscript. They were not silently regenerated
in this run and are not claimed as a fresh 2026-09-07 measurement.

## Working-tree drift observation

The same detectors on the 2026-09-07 working tree produced D1 `121/40/62/29`, D2 `14,969` total
fallback sites with `7,950` detector-decidable sites, and D3 `337/285/13/7/32` for
total/undecidable/sample-as-state/honest/full. Those values explain the earlier review warning;
they do not alter the historical tables.

This distinction is intentional: changing corpus scope is a new measurement, not a correction to
the older result.
