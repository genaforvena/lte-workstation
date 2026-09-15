# Independent rejected-successor recovery acceptance

Witness claimed `dispatch-rejected-successors-20260909/verify-live-recovery`.
Previous turn made progress: two chains regained their original successors and
the Unit5 resolver was accepted by tg. This turn independently tested recovery.

## Verified

- Isolated exact-owner recovery, repeat-call source replay equality, preserved
  rejection history, successor take/done and dispatch to the next owner: PASS.
- Explicit hold, repeat-call source replay equality, exclusion from dispatch,
  and refusal of take while held: PASS.
- The deployed task executable matches source SHA-256 `2fdd828cf268c463fac476ec79425f702ce1636062400d35f170cb92a2b27d98`.

Independent tests: `tests/test-witness-recovery-acceptance.py` (the three
`RecoveryAcceptance.test_recovery_replay_and_exact_owner`,
`test_hold_is_idempotent_and_never_dispatches`, and
`test_narrow_pane_keeps_rejected_hold_visible` methods).

## Consumer defect found and repaired

The new journal state HELD_REJECTED was excluded from all three witness-pane
status filters. The isolated 80-column fixture contained one held task but
rendered zero tasks. The first run was 2 PASS / 1 FAIL.

Witness added HELD_REJECTED to the total, unfinished and displayed-row filters
in scripts/mesh-dash, notifying tg of the exact section to avoid overlap with
its minds-frame work. The same three tests then passed; the existing pane-fit
test and bash syntax check passed. Deployed mesh-dash resolves to source, with
matching SHA-256 `bee1b050337a91eebdc08802fcb6206bb199554e6b753643bac3e1e546dc622c`.

At 18:06 UTC the live pane showed HELD_REJECTED for operator and Tiny Fleet rows,
342 total / 142 unfinished, and the latest 20 raw source lines. Journal refresh
reported another writer held its lock; existing valid view age was 26 seconds.
No competing replay was forced.

## Remaining acceptance

Haunt was routed an exact-owner hold/disposition of
`tinyfleet-applications-20260908/support-routing`, with an explicit prerequisite
to resolve A02 environment reproduction and independent VPN verification.
Its authoritative transition and receipt remain to be checked.

The residual human identity row is explicitly HELD_REJECTED and owner=operator;
the replacement phone identity task remains human-dependent. No automated actor
may impersonate that owner. The two reopened genome successors are OPEN/sent;
owner taking and real progress must still be observed. TG is actively repairing
the full-test gate through its keyed resolver; Unit5 remains blocked.

This is partial verification, not completion of the chain or overall goal.

The full independent test file (including inherited lifecycle regressions)
subsequently passed all 14 tests in 17.460 seconds. `git diff --check` passed.
Haunt's live pane confirms active receipt/chain inspection; no restart requested.

## Live follow-up 18:09 UTC

Haunt authored the exact `support-routing` hold at 18:07:02, created
`tinyfleet-a02-v-env-20260909/resolve-a02-v-env`, and at 18:08:09 returned
the original task to OPEN with `waiting_for` that exact prerequisite. The
prerequisite description explicitly requires environment reproduction and
independent VPN acceptance. This accounts for all 16 Tiny Fleet successors;
only the operator-owned split identity chain remains HELD_REJECTED.

Dispatcher evidence distinguishes holds and delivery failure: genome was busy
until its repair finished; at 18:07:54 delivery failed during pane restart and
the task stayed queued. A later normal scan dispatched the original
`coordination-hledger-plan-20260908/background-recovery` at 18:08:53. Owner taking
is still required. A delayed historical FYI caused a redundant review turn;
witness supplied the current original task ID and completed repair evidence.
This is a remaining pacing concern, not grounds to restart a live owner.

Current audit: 343 rows, 170 DONE, 30 REJECTED, 19 BLOCKED, 121 QUEUED,
two RUNNING, one HELD_REJECTED. Pending independent acceptance is owner-taking
evidence for restored work, not another replay of already passing unit tests.

## Acceptance at 18:10 UTC

PASS for rejected-successor recovery and its live dispatch path. Genome took
`coordination-hledger-plan-20260908/background-recovery` at 18:09:49; the canonical
step is ACTIVE, with lease until 18:39:49. This is 56 seconds after the observed
18:08:53 delivery. Its live pane confirms work on the original task's actual
lifecycle acceptance requirements.

All 25 formerly stranded successors now have an explicit disposition: eight
in the two reopened genome chains, sixteen behind the exact A02 prerequisite,
and one visible human-owned hold. The second genome chain stays queued while
that exact owner works; no owner was substituted and no failed verification was
silently accepted. Haunt's A02 and tg's dashboard prerequisites remain real open
work. This acceptance closes the recovery correction, not those implementation
tasks or the wider dispatch goal. The historical FYI re-delivery and other stale
blockers still warrant a separate flow audit.
