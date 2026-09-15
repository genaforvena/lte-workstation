# mesh-series-stats escalation disposition — 2026-09-08

Decision: **(a) diagnose and fix why the deficit never cleared**. The repair is already
landed; this turn does not repeat it.

## Root cause

The repeated cue was the decay lane's persisted `DECAY CANDIDATE` for `mesh-series-stats`,
not a failure of the statistics organ. `mesh-reflex-decay --candidates` previously accepted
a cached report by age alone. The report could therefore outlive both the scanner that produced
it and the subject it judged. The 2026-08-21 tape records four decay filings at 05:00, 06:45,
07:00, and 07:15 UTC, followed by cue-pinned escalation at 07:30 UTC.

The landed fix stamps reports with the classifier hash and rejects foreign/unstamped reports;
it also drops candidates whose deployed subject changed after the report. These are
suppression-only checks, so they cannot hide a newly created candidate.

## Evidence

- `scripts/mesh-reflex-decay --test`: rc 0; its end-to-end test covers foreign/unstamped
  reports and post-report subject changes.
- `mesh-reflex-decay --candidates`: rc 0, no candidates.
- `mesh-needs --check`: `needs: none — no acute deficit`.
- `scripts/mesh-reflex-decay` and `~/.local/bin/mesh-reflex-decay` are identical
  (`c34695aac7ca5c9c…`). `scripts/mesh-series-stats` and its deployed copy are identical
  (`6a9ba1339a3f66d1…`).
- `scripts/mesh-series-stats --test`: rc 0.

Retirement is rejected: the tool is wired into `mesh-claims-tick` and the live sound dash.
Muting is rejected: the old decay cue is cleared and no current decay deficit exists.

The separate `mesh-series-stats --claims` result is intentionally non-zero on the current
2,153-row corpus because standing doctrine claims are currently REFUTED/MIXTURE/
INDISTINGUISHABLE. That is a real measurement verdict, not the old decay deficit, and is
left visible for its consumers.
