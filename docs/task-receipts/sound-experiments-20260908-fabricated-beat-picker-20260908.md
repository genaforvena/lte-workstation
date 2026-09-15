# fabricated-beat-picker — live detector receipt

Task: `sound-experiments-20260908/fabricated-beat-picker`
Owner: `sound`
Date: `2026-09-08`

## Existing detector run

Command: `scripts/mesh-series-stats --claims`

Live source reported by the command:

```text
source: /home/mesh-home/.mesh/records.log (2165 rows, mtime 2026-09-08T22:22:30Z)  ROM: series-stats.rom
```

The existing pure detector is claim 4, the structural sanity predicate
`beats > fbeats` on strict subwindows. Its live output was:

```text
claim 4 — measured 2026-08-29: "a strict sub-window's beat count never exceeds its whole file's" (same estimator, so >0 is structurally impossible)
  sub-window rows: n=1290  impossible=244 (18.9%)  abstained(no whole-file scan)=407
  => REFUTED: 244 of n=1290 strict sub-windows report MORE beats than the file containing them
     arms: ext 0/79=0.0% voice 0/3=0.0% ear 14/471=3.0% note3 229/424=54.0% scape 1/120=0.8% drop 0/193=0.0%
     degenerate whole-file scans (fbeats=1 — one beat defines no inter-beat interval, so that file has no period at all): 246 of n=1290, and 203 of the 244 violation(s)
     side[ear]: viol n=14 beats=21.4 fbeats=15.1 | clean n=457 beats=10.2 fbeats=34.4 -> window +111%, file -56% => the SUB-WINDOW count is what moves (the window inflated)
     side[note3]: viol n=229 beats=6.2 fbeats=1.4 | clean n=195 beats=4.5 fbeats=14.1 -> window +38%, file -90% => the WHOLE-FILE count is what moves (the file side collapsed; the window did not inflate)
     side[scape]: viol n=1 beats=4.0 fbeats=3.0 | clean n=119 beats=11.6 fbeats=77.3 -> window -65%, file -96% => the WHOLE-FILE count is what moves (the window did not inflate)
```

The command ended with `claim-gate: rc=1`; that is the honest standing-claim
state because claim 4 is REFUTED. This receipt does not claim a ranking win:
`records.log` retains winners after per-organ pruning, so candidate-level
alternatives, enrichment, preservation, and counterfactual picker rankings
cannot be reconstructed from the retained ledger. No production detector or
picker was added.

## Reconciliation

The existing detector is the real artifact requested by the task. The task is
closed on this bounded result: the live `beats > fbeats` detector is a useful
fabrication signal, but its dominant mechanism is whole-file collapse in
`note3`, not a general window-inflation picker. A future counterfactual test
requires `mesh-soundscape` to persist candidate-level traces.
