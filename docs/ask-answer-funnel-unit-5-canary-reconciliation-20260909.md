# Ask-answer funnel Unit 5 canary — blocker reconciliation

Date: 2026-09-09 (UTC)

Task: `ask-answer-funnel-implementation-20260907/unit-5-canary`

## Decision

The stale portion of the blocker is disproved: Unit 4 is already `done`, and the canary
registry records the rate ceiling, recognizable honesty rule, and explicit-operator-only
injection rule. The recreated replacement and its autoland receipt are also `DONE`.

The original task remains blocked because the current deployed full acceptance is not green.
The concrete remaining prerequisite is to restore the minds-frame division-of-labour axis:
the current full test reports that `mesh-forage` output is not wired into the pane.

No canary was injected. The explicit-operator-only rule remains in force.

## Receipts revalidated

- `mesh-task status ask-answer-funnel-implementation-20260907`: Unit 4 `done`; Unit 5
  `blocked`; final verification `open`.
- `docs/ask-answer-funnel-unit-5-canary-registry-20260908.md`: SHA256
  `be431d0c0dfa1f2f9cfb9377de7a1ca4d75dc6f2802776000209f1f4a8698002`.
- `autoland-recreated-rejected-20260908-01/land-unit-5-canary`: owner receipt says `done`,
  registry verified, no synthetic ask injected.

## Current verification

- `bash tests/test-mesh-dash-ask-resolution.sh` — PASS.
- `bash -n scripts/mesh-dash` — PASS (`rc=0`).
- `bash scripts/mesh-dash --test-fast` — PASS (`smoke-test: ok`).
- `/home/mesh-home/.local/bin/mesh-dash --test` — FAIL:
  `minds frame missing the division-of-labour axis — mesh-forage output not wired into the pane`.
  Receipt: `/tmp/ask-answer-funnel-unit5-revalidation-20260909.out`.

## Required next action

Repair and reverify the `mesh-forage` → minds-frame wiring, then rerun the deployed full
`mesh-dash --test`. Only after that returns `rc=0` may the original Unit 5 task be resumed with
`verified-registry-and-unit4-receipt` and completed against this reconciliation artifact.

## Current revalidation (2026-09-09)

The stale registry claims remain reconciled: the registry SHA256 is
`be431d0c0dfa1f2f9cfb9377de7a1ca4d75dc6f2802776000209f1f4a8698002`, the replacement chain
`recreated-rejected-20260908-01` is `[complete]` with its Unit 5 step `[done]`, and source/deployed
`mesh-dash` remain byte-identical at SHA256
`bee1b050337a91eebdc08802fcb6206bb199554e6b753643bac3e1e546dc622c`.

Fresh acceptance did not pass. The bounded deployed full check
`timeout --signal=TERM --kill-after=5s 60s /home/mesh-home/.local/bin/mesh-dash --test`
ended by timeout (`rc=124`); receipt `/tmp/ask-answer-funnel-unit5-full-recheck-20260909.out`
contains `Terminated` and SHA256
`b4a6c06672677cf0e25ec72bec83beae33305cee4b8087f168962014373b02bb`. A direct bounded minds
render also failed to produce a frame within 45 seconds, while the independent
`mesh-forage --json` probe produced valid JSON (6,315 bytes); therefore the concrete blocker is
the deployed minds-frame acceptance path not completing/rendering its forage-produced axis, not
an absent registry or absent forage executable.

Disposition: original Unit 5 remains `blocked`; no resume or canary injection is authorized by
this evidence. The explicit-operator-only injection rule is unchanged.
