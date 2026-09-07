# Ask→answer funnel Unit 1 — explicit key evidence

Date: 2026-09-07
Task: `ask-answer-funnel-implementation-20260907/unit-1-explicit-key`

## Change

`[task]` lines already mint `task:<id>`. The live task-side `idof()` and shared
`claim_id_of()` now preserve that complete explicit id, including its namespace. Untagged
legacy board lines retain the old derivation path and are not guessed into a new join.

Changed:

- `scripts/mesh-dispatch`
- `scripts/mesh-claim-shape.sh`
- deployed shared parser: `/home/mesh-home/.local/bin/mesh-claim-shape.sh`

The repository and deployed shared parser have identical SHA-256:
`3cc3f66da36a25e79fb3d3d5b58c9f512ff1e12029b6936224f7b903fe3831d6`.

## Red before green

The pre-fix namespace join reduced
`ask-answer-funnel-implementation-20260907/unit-1-explicit-key` to
`unit-1-explicit-key` and failed the exact-key assertion with `rc=1`.

## Green evidence

The real parser join test now drives task, dispatch/claim, and terminal done shapes through
`mesh-dispatch --derive-ids` and asserts the same full key at both ends.

- `scripts/mesh-dispatch --test` — PASS, 260 assertions.
- `scripts/mesh-claim --test` — PASS.
- `mesh-task status ask-answer-funnel-implementation-20260907` — Unit 1 active with owner `tg`.
- `mesh-promises --check` — PASS before implementation.

## Sound dependency recheck

The owning `mesh-sound-reflex` produced a fresh real artifact before this recheck:
`/home/mesh-home/.mesh/records/20260907-162346-ext-1ac71c41.mp3`, 4,722,669 bytes.
The reflex `--test` was retried with a 15-second bound; it emitted fixture evidence but did not
finish (`rc=124`). The typed sound dependency block is preserved; no lock was removed or bypassed.

Live recheck at 16:30Z: `mesh-sound-reflex --status` passed (`rc=0`), reporting 2,090 ledger
lines, 148 pending, and 12/12 distinct trailing recipe cells. `records.log` also contains fresh
16:30Z reflex rows (`cc4d2368`, `3447c431`, both `pending`). No newer mp3 than the 16:23Z artifact
was produced, so the sound task remains blocked pending a fresh render; the zero-byte lock was not
removed and `fuser` reported no holder.
