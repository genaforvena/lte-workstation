# Receipt: `sound-experiments-20260908/skip-not-picked-retirement`

Date: 2026-09-08  
Owner: sound

## Decision

Keep `skip:not-picked` as permanent retirement for streaming organs (`ear`, `note3`,
`scape`, and `ext`). A loser is not silently returned to the score race: doing so would
change the operator-facing meaning of an already-issued verdict and would make the
forward-only cursor claim a false recovery.

Rare or filesystem-retained organs (`voice`, and any future static/reference organ) get a
different contract, but not an automatic ledger rewrite: their organ definition must opt
into a bounded re-offer lane that enumerates files on disk, records an explicit operator
visible re-offer, applies a lifetime cap and cooldown, and repels the new recipe from every
recipe already worn. If that wiring is absent, the material stays retired and the lane must
report the unreachable inventory rather than claiming recovery. No live knob change is
proposed by this receipt.

## Live census

The 2026-09-08 `mesh-dash --once sound` stream showed 1160 corpus rows, no pending operator
drop, and one idle render lane. `mesh-sound-reflex --repick` showed 243 eligible and 129
`refused:evicted` sources; the eligible set is the existing worn-source re-pick lane, not
recovery of never-picked rows.

Filesystem enumeration of `/home/mesh-home/.mesh/records` found 861 retained record files:

```text
                 ground   skip:not-picked   other/current   no ledger row
drop                214          367              17             422
ear                   1            0              67               0
ext                  11            3              10               0
note3                11            2               8               0
scape                 5           20              5               0
total               242          392             107             422
```

The 422 rowless retained files are not reachable by rewriting a verdict: they are behind
the archivist's forward cursor. The static `voice` organ separately still has 5 files
(19,111,984 bytes), 3 of which have the permanent `skip:not-picked` verdict and none of
which has been ground. This is why a generic ledger-based re-offer is rejected; a future
voice/static exception must enumerate the filesystem and surface its cost to the operator.

## Verification

- `mesh-dash --once sound` — passed; live unfiltered state read at 2026-09-08T23:24:47Z.
- `mesh-sound-reflex --repick` — passed; live pool reported 243 eligible / 129 evicted.
- Filesystem enumeration plus ledger join — completed; counts above.
- No production render, ledger rewrite, or live picker change was made.

Next action: leave the policy pending for an operator decision before implementing any
bounded static-organ re-offer lane.
