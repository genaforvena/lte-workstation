# Receipt: `sound-experiments-20260908/nofill-verdict-retention`

Date: 2026-09-08  
Owner: sound

## Change

`scripts/mesh-sound-reflex` now appends the completed drop listen outcome to the never-pruned
`$SR_VERIFY_LOG` tape (default `~/.mesh/room-music-verdicts.tsv`) at verdict time. Rows carry:

```text
timestamp<TAB>hash<TAB>organ<TAB>pass|reject|unverified<TAB>recipe<TAB>detail
```

The detached child passes its sandbox/live log explicitly, and concurrent writers are serialized by
the tape's lock. Analyzer absence and analyzer `rc=2` are `unverified`, not `pass`; a missing row is
therefore still unknown. The historical snapshot is not rewritten.

## Historical audit preserved

The frozen one-shot `/home/mesh-home/.mesh/render-verdicts-snapshot.tsv` remains unchanged:

```text
sha256 43f9db51c8af6ffe078d24090c151e91838dc1905c7b039fb6d6b2533a27c0d8
nofill population 73
  reject              1
  ground-verify-ok    8
  ground-verify-unk  12
  UNKNOWN-pruned     26
  UNKNOWN-pre-horizon 24
  skip:*               2
```

The 50 pruned/pre-horizon rows are not counted as shipped. The live params tape currently contains
226 nofill rows (`2026-08-16T13:50:10Z` through `2026-09-08T20:55:58Z`); rows become re-derivable
against their outcome only when a matching append-only verdict row exists.

## Verification

- `tests/test-nofill-verdict-retention.sh` — passed: pass/reject/unverified rows append, and a
  missing hash is not promoted to shipped.
- `bash -n scripts/mesh-sound-reflex` — passed.
- `scripts/mesh-sound-reflex --test` — honest `n/a`/`rc=2` because the live reflex held
  `/home/mesh-home/.mesh/records.log.reflex.lock`; the run did not alter the frozen snapshot and,
  after sandbox rebinding, did not create a live verdict tape.

Unresolved: a clean full smoke rerun needs the live reflex lock to be free; no production render was
started for this audit.
