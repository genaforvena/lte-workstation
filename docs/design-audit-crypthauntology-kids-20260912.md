# Crypthauntology for Kids expansion audit — 2026-09-12

## Verdict

The plan has substantial implementation evidence, but its lesson-review and expansion gates remain
open. The existing protocol is explicitly `offline-gate-only`: it forbids child research subjects,
requires adult mediation and paper alternatives, and sets `live_model_campaign_authorized` to false.
No child-facing deployment is represented or authorized here. A separate, ordered follow-up chain
has been recorded at `docs/plans/2026-09-12-crypthauntology-kids-followup.tsv` as
`crypthauntology-kids-followup-20260912`; it adds no deployment tags.

## Package map

| Expansion package | Evidence and disposition | Durable follow-up |
|---|---|---|
| Freeze contract; age-banded lessons; content/safety gate | `protocol/design-manifest.json`, `protocol/lesson-schema.json`, three age-band lesson files, answer key, facilitator guide, glossary, safety checklist, and mutation fixtures exist. The persisted offline report says PASS and both unsafe-content and missing-paper-path mutations fail. However, `lessons/reviewer-signoffs.md` leaves reviewers A and B PENDING, the safety checklist is unchecked, and `cryptohaunt/gate.py` does not read the sign-off record. **Open safety gate.** | `crypthauntology-kids-followup-20260912/lesson-review-safety-gate` — owner `haunt`; adult review and an honest fail-closed/pending disposition are required before any live pilot. |
| Probe matrix and offline pilot | Canary registry, disjoint calibration/holdout split, synthetic three-arm tape, replay transcript, and seeded power worksheet exist. The two-repetition pilot is provider-free and deterministically replays, but reports 77% MDE for neutral/assent and UNDERPOWERED for identity/provenance; the plan's 3–5 canaries per category and frozen provider/prompt runtime inputs are not evidenced as complete. No live pilot can be inferred from these artifacts; the design manifest still disallows live campaigns. | `crypthauntology-kids-followup-20260912/offline-probe-pilot-reconciliation` — owner `haunt`; offline work only, preserve insufficient-power verdicts, and record any live prerequisite as blocked. |
| Adult-only powered study and educational release | The clean project checkout at `/home/mesh-home/src/hyperhauntology_for_kids` is at `811bd8dd7b0a5a9ecaac2d942da9c0926a252e92`. The v1 release records 30 complete / 25 inferentially eligible repetitions, tape SHA-256 `b0fde7028828b52481582672b41baa6383b1fa166a80f07102837cb040abba0a`, a disjoint holdout, and byte-stable offline replay. Neutral and assent are NULL at MDE 13%/19%; identity and provenance are BLIND. This is existing adult-only evidence, not authorization for another campaign. The release's educational review is explicitly PENDING, and its witness is the automated release verifier rather than the independent witness required by the plan. | `crypthauntology-kids-followup-20260912/adult-study-release-independent-review` — owner `witness`; independently verify the extant bundle offline and retain the pending educational-review boundary. |

The older board task `crypthauntology-protocol-lesson-schema` was completed by `haunt` on
2026-09-07 with the initial schema and offline gate. It is a board promise, not a structured
`mesh-task` chain. The three new steps cover remaining gaps and verify existing evidence; they do
not duplicate the initial schema task or claim the expansion plan complete.

## Verification

- `mesh-dash --once haunt` showed the intended project lane, clean checkout, no run in flight, and
  the latest tape verdict `NOT-ESTABLISHED` (no eligible result inferred from that tape).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v` in the project checkout: **54 tests
  passed**. This exercises detector, lesson, offline-pilot, release-validation, and tape behavior;
  it does not exercise a live provider or complete the independent human reviews.
- Read the persisted offline-gate, safety-review, pilot, power, release, holdout, replay, and witness
  artifacts. No live model call or child-facing use was performed.
- The project checkout was clean at audit time; no files in it were changed.

## Unresolved obligations

The two independent adult sign-offs and safety checklist remain pending. The offline probe matrix
and pilot do not meet the plan's full expansion/power criteria. Existing study/release evidence is
auditable, but the requested independent witness and educational review remain outstanding. The
manifest still denies authority for new live model campaigns. The first next action is `haunt`'s
`lesson-review-safety-gate` task; do not proceed to any live pilot or child-facing activity from
this audit.
