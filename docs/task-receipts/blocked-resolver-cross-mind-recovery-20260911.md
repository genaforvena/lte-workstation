# Blocked resolver cross-mind recovery — implementation receipt

Date: 2026-09-11 UTC

## Change

`scripts/mesh-task` now keeps blocked resolver chains actionable. If a resolver
itself blocks, the coordinator selects another currently live mind, creates a
second-level resolver with the exact blocked resolver as `unblock_parent`, and
the resolver's artifact-backed `unblock=cleared` result internally resumes only
that exact parent. `unblock-sweep` also scans resolver chains, so pre-existing
blocked resolvers are migrated on the next sweep. If no other live mind exists,
the system emits a visible yield instead of silently claiming recovery.

## Verification

- `python3 -m unittest tests/test-mesh-task-blocked-self-unblock.py` — PASS, 12 tests.
- `python3 scripts/mesh-task --test` — PASS.
- `bash scripts/mesh-task-unblock-sweep --test` — PASS.
- `python3 -m py_compile scripts/mesh-task` — PASS.

## Retry storm control

Repeated unresolved resolver results now use bounded exponential backoff after
the first retry (`300s`, then doubling up to `3600s`). A fresh retry remains
automatic, but periodic sweeps cannot manufacture unbounded duplicate chains
while the same concrete prerequisite is still absent. The regression suite
covers this invariant; 16 tests pass and source/deployed parity is verified.

## Operator-input policy

Resolver descriptions for `operator-input` blockers now explicitly assume operator
agreement. Minds must not ask for permission: they derive and safely implement the
needed prerequisite, or produce an artifact-backed operator-action packet naming the
exact command, input, or condition required. A task may remain blocked only on a
concrete external capability or missing datum, never on approval. Existing immutable
history is preserved; new and retried resolver attempts carry this instruction.

Additional verification on 2026-09-11:

- `python3 -m unittest tests/test-mesh-task-blocked-self-unblock.py` — PASS, 14 tests.
- `python3 scripts/mesh-task --test` — PASS.
- `bash scripts/mesh-task-unblock-sweep --test` — PASS.
- `python3 -m py_compile scripts/mesh-task` — PASS.
- Source/deployed parity — PASS: both `scripts/mesh-task` and
  `~/.local/bin/mesh-task` SHA-256 `7c50bafdf0ed9b5f3105e7683598aee4f141e8bb1287dd817831c3f7e2e96dc7`.

## Operator-directed event extension

The same policy also applies when a row is typed `external-event` but its blocker
text names an operator decision, input, or recovery path. This closes the semantic
escape hatch where an operator gate could be mislabeled as an external event.

Verification: blocked-resolver test suite PASS, 15 tests; mesh-task smoke test PASS;
unblock-sweep smoke test PASS; compilation PASS; source/deployed SHA-256 parity PASS
at `c1ef782c61f3a72a1ee317ee487654079d034e32b4edc237d2d66e116378cecd`.

Live follow-through evidence:

- `unblock/adint/6c5597c955121d96/resolve` completed with artifact
  `/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-adint-6c5597c955121d96-20260911.md`
  and an explicit partial result; the exact Haunt resolver remained blocked.
- The next sweep materialized retry attempt 2 as
  `unblock/adint/2efe508c50b2779b/resolve`, owner `adint`, dispatch `sent`.
- This proves the unresolved partial result is neither silently terminalized
  nor repeatedly duplicated while an attempt is open.
- Source/deployed parity — PASS: `scripts/mesh-task` and
  `~/.local/bin/mesh-task` both SHA-256
  `0b91255ae43e4cead9cdd2af3fd82c9bf67939ff4daf7bdbe2feeb907361d47a`.
- Live all-owner sweep — PASS: five nested recovery tasks were materialized
  for currently blocked resolver epochs, including
  `unblock/adint/6c5597c955121d96/resolve` for Haunt's blocked resolver
  `unblock/haunt/f2571f5df1359758/resolve`.
- Live audit — PASS for visibility: the nested tasks are queued with owner
  `adint`, while the original Haunt resolver remains visibly blocked pending
  runner implementation/headroom.
- Live pane — PASS: `mesh-dash --once witness` shows the updated unfinished
  count, source age, and unfiltered 20-line board tail.

## Remaining work

Haunt's study runner is present as uncommitted work in `/home/mesh-home/tiny-fleet`
but full execution remains intentionally incomplete and resource constrained.
The recovery task is therefore correctly queued for another live mind; Haunt's
original resolver must not be marked done until the runner prerequisite has an
artifact-backed result.

## Follow-through correction

A resolver may produce a valid partial artifact while explicitly leaving its
parent blocked. The coordinator now treats that as a completed attempt rather
than a durable resolution: the next all-owner sweep creates one fresh attempt
with an incremented `unblock_attempt`, while open/active or cleared attempts
remain idempotent.

Additional verification:

- `python3 -m unittest tests/test-mesh-task-blocked-self-unblock.py` — PASS, 13 tests.
- `python3 scripts/mesh-task --test` — PASS.
- `bash scripts/mesh-task-unblock-sweep --test` — PASS.
- `python3 -m py_compile scripts/mesh-task` — PASS.
