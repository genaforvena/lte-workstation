# Promise writeoff/reroute design audit — 2026-09-12

## Scope and evidence

Audited `docs/superpowers/specs/2026-07-24-promise-writeoff-reroute-design.md` against
`scripts/mesh-promises`, its implementation plan, the CLI dispatch, current task ledger, and the
tool's synthetic-board suite. The audited inputs were:

- Spec SHA-256: `aab116152ea8b818845fff1b9ba32193f467d4417dba2cf5cbe7aaf069832587`.
- Implementation SHA-256: `34661f4e46ddadb3f13a6a78764392916c08ab759c8d15193aed8a894b788ba1`.
- Plan SHA-256: `7a741480286893dfa6b09279856cc503412531e9f89c64b8744fe0b7f22f858e`.

The July spec and matching plan remain present, and no later decision superseding their Components
A–D was found. Before this audit the only current task was this spec audit; no implementation task
for these components was present in the canonical task ledger.

## Findings

| Component | Current behavior | Disposition |
|---|---|---|
| A. Uniform unrouted accounting | The replay computes and exposes unrouted count only for promises. The `counts` row has no `claim_unrouted`/`hold_unrouted`; claim and hold JSON rows lack `unrouted`; `--check`'s roster section checks promise quarantine only. The journal's `acct_window()` quarantine remains in place for promise, claim, and hold accounts. | Still required: expose the existing claim/hold quarantine on the same reporting surfaces without changing journal routing. |
| B. Manual writeoff/reroute | CLI dispatch and usage expose neither `--writeoff` nor `--reroute`; no `do_writeoff()` or `do_reroute()` is present. Existing writeoff is a distinct legacy path: with `MESH_CLAIM_WRITEOFF_H > 0`, only old `reflex-broadcast` claims are marked written off, removed from the leak list, and booked to `expenses:claims:uncollectible`. The default horizon is zero (disabled); ordinary window-owed claims are guarded from writeoff. There are no general board-posted close events or distinct `equity:*:writeoff`/`equity:*:reroute` legs. | Still required as designed, while preserving the narrow bad-debt path as separate behavior. The spec's open identity question remains: implement its stated default that any real window may explicitly triage, with the actual poster retained in board history; do not impersonate another window. |
| C. Suggested owner | No charter-overlap suggestion function or rendering is present. | Still required as advisory output only, including an explicit no-match result. |
| D. Confidence-gated reaction | No `MESH_PROMISE_AUTOREACT`, auto-reroute, auto-mute, or corresponding CLI path is present. | Still required as described: default-off, reroute only with an unambiguous suggestion and incident exclusion, mute without changing liabilities, and never automated writeoff. |

The existing narrow writeoff test is real but does not satisfy Component B: the test covers the
48-hour reflex-claim dead-letter path, the guard that an addressed claim stays leaked, balanced
expense accounting, and `--check` agreement after that writeoff. That path must not be mistaken for
the requested operator-posted action with exact item lookup, an equity disposition leg, and a board
trail. The spec's tests for exact-key refusal, reroute reopening, uniform claim/hold quarantine,
suggestions, ambiguity/incident guards, mute preservation, and default-off behavior remain unbuilt.

## Remaining implementation work

Recorded a four-step implementation chain in `promise-writeoff-implementation-20260912` (plan at
`docs/plans/2026-09-12-promise-writeoff-implementation.tsv`), owned by `witness`:

1. Surface claim/hold unrouted counts, row fields, report marks, and roster checks without changing
   existing journal quarantine.
2. Add validated board-posted writeoff/reroute actions with separate outcome accounting; keep hold
   reroute forbidden and retain the narrow automatic bad-debt rule as separate behavior.
3. Add charter-overlap suggestions, including a truthful no-overlap result.
4. Add the opt-in `--feed` reroute/mute behavior with ambiguity, incident, no-writeoff, and
   liability-preservation tests.

The manual-action implementation should carry the spec's current identity default: an explicit
action may be posted by any actual window, and its board poster remains visible. This is the design's
stated assumption, not a newly observed operator answer to the open question.

## Verification

- `rtk bash scripts/mesh-promises --test`: PASS, exit 0. This runs the synthetic fixtures, including
  the current automatic bad-debt writeoff and its accounting guard.
- Read-only inspection of the script's counts, JSON, check, dispatch, writeoff, and test paths
  confirmed the table above. No live writeoff, reroute, or automatic board mutation was issued.
- Did not run `--check` against the shared materialized journal: the earlier
  `docs/design-audit-promise-lifecycle-20260912.md` records an unresolved default-path promises
  journal inconsistency. The synthetic `--test` result does not certify that live materialization.

## Next action

`witness` can start the implementation chain at `uniform-unrouted-accounting`; after Components A–D
and their fixtures land, rerun `rtk bash scripts/mesh-promises --test` and verify the exact
`--check` behavior against a private `MESH_PROMISES_DIR` before checking live materialization.
