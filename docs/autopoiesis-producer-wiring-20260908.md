# Autopoietic producer wiring acceptance

Date: 2026-09-08
Task: `autopoiesis-task-ledger-20260908/wire-autopoietic-producers`

## Landed behavior

- `scripts/mesh-autopoiesis` validates the six-field origin envelope and delegates
  eligible plans to the existing `mesh-task create` store.
- `scripts/mesh-autopoiesis intake --raw` retains incomplete novelty in the
  existing `~/.mesh/ideas-queue`, keyed by content digest; it does not mint a
  task chain from incomplete material.
- `scripts/mesh-autopoiesis feedback` replays the authoritative task ledger and
  groups `kind`, stable `source`, outcome, observed spend-log turns, and chain.
  A missing task tag remains `0` observed turns; no synthetic cost is created.
- `scripts/mesh-ideate --admit PLAN` (including `--lit --admit PLAN`) and
  `scripts/mesh-needs --admit PLAN` are producer routes into that adapter.
  Their ordinary paths continue to emit raw queue material.

No second task store was added. Source-ID deduplication remains enforced by
`mesh-task create`, including against settled chains.

## Evidence

Focused test:

```text
$ tests/test-autopoietic-producers.sh
mesh-autopoiesis: smoke-test ok (six-field admission, raw retention, derived feedback)
retained raw novelty key=264c3f0982ff7301 queue=<isolated mesh>/ideas-queue
mesh-autopoiesis: incomplete admission envelope: missing hypothesis, question, acceptance, feedback
test-autopoietic-producers: ok
```

The same test exercises an eligible plan through a task-command stub and proves
that an incomplete plan is refused. Shell syntax and Python compilation also
passed:

```text
$ bash -n scripts/mesh-ideate scripts/mesh-needs
$ python3 -m py_compile scripts/mesh-autopoiesis
```

Live derived feedback from the current task ledger:

```text
kind    source                                                   outcome  observed_turns  chains
literature  review:map-elites-illumination-literature-lane-2026-07-28  adopted  0  literature-canary-map-elites-20260908
```

The preceding literature canary bundle remains the end-to-end source/application
evidence: `docs/autopoiesis-literature-canary-review-20260908.md`,
`docs/autopoiesis-literature-canary-application-20260908.md`,
`docs/autopoiesis-literature-canary-acceptance-20260908.md`, and
`docs/autopoiesis-literature-canary-spend-20260908.md`.
