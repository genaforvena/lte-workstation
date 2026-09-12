# Expansion implementation tasks — 2026-09-07

Parent board task: `task:ask-20260907t074729z-turn-the-three-expa`.

This manifest turns the three dated plans into independently executable board tasks. Each task has
one owner, an ordered scope, a concrete artifact, and a verification condition. Tasks within a
plan are ordered; later tasks must not claim completion until the preceding artifact exists.

## Self-ADINT (`docs/plans/2026-09-07-self-adint-expansion.md`) — owner `adint`

### `self-adint-expansion/baseline-and-receiver`

1. Reconcile the separate `~/self-adint` tree and record revision, dirty paths, runtime inputs,
   and the device-lane blocker.
2. Repair or explicitly disposition the receiver blocker, then run the real receiver gate and its
   red-before-green mutation.
3. Artifacts: dated baseline note, receiver corpus and mutation report, plus either the source
   SHA-256 manifest and append-only device-observations JSONL **or** an explicit
   `BLOCKED_OPERATOR_EXPORT` artifact naming the missing complete PCAPdroid CSV, reachable host,
   and device label. Do not fabricate an empty device artifact.
4. Verify: existing offline tests plus a fresh receiver run; the deliberate bad mutation fails and
   the restored implementation passes without writing outside the declared output tree. A missing
   operator export is a terminal block for the device lane, not a failure to finish this task's
   receiver work.

### `self-adint-expansion/passive-oracle-persistence`

1. Establish the passive baseline and schema contract, then assess active-oracle eligibility
   without treating an unavailable oracle as a success. Preserve the passive-only refusal/replay
   evidence when eligibility is absent.
2. An active treatment/control persistence run is a separate gated successor. Do not start it until
   a measured payload gate and independent return-vantage assessment exist and the operator gives
   an exact go for that intervention.
3. Artifacts for this passive task: passive ledger/source reference, schema/egress report, oracle
   verdict, passive-only schedule/events/runs, checksum manifest, and explicit active-run block
   where eligibility is absent. Active event/run rows and a persistence estimate are not required
   and must not be fabricated to close the passive task.
4. Verify: schema/checksum validation, refusal-path test, replay of one passive control cell, and a
   check that the refused active path wrote no active result.

### `self-adint-expansion/operator-gated-release`

1. Keep operator-gated branches in a separate question/decision ledger; do not silently execute
   them. Include seat onboarding/agreement/payment, outbound DSAR letters/mailbox, and GAID reset
   as separate rows with their exact per-step decision gate; absence of an operator decision is a
   block, not permission.
2. Package the reproducibility bundle, redacted guide, letter evidence blocks, baseline hash,
   reset instructions, and handoff note.
3. Artifacts: complete decision ledger (including the outbound-letter branch), evidence blocks,
   reproducible bundle, manifest, and handoff note.
4. Verify: clean-tree/reproduction check, checksum match, reset-to-baseline check, and explicit
   witness disposition for every unfinished or refused branch. Packaging and read-only preparation
   may proceed; no onboarding, agreement, payment, mail, active study, or reset may proceed without
   its own satisfied gate.

## Tiny-fleet (`docs/plans/2026-09-07-tiny-fleet-expansion.md`) — owner `genome`

### `tinyfleet-expansion/protocol-corpus-fixtures`

1. Freeze the protocol and provenance manifest before collecting data.
2. Assemble the larger license-safe corpus and build deterministic fixtures, including toy control,
   leakage, and adversarial negative cases.
3. Artifacts: versioned protocol hash, source/license manifest, corpus lock, fixture inputs/outputs,
   and fixture report.
4. Verify: clean-room rebuild from the manifest, deterministic hashes on a second run, and all
   negative controls fail for the intended reason.

### `tinyfleet-expansion/measurement-controls`

1. Expand the measurement ladder across the declared snapshots and model-capacity controls.
2. Add falsification arms, uncertainty/denominator calculations, and explicit separation of
   prompt conditioning from genuine LoRA/QLoRA fine-tuning.
3. Artifacts: raw run manifests, evaluator outputs, control results, uncertainty table, and
   dependency/preflight report.
4. Verify: evaluator and validation tests, replay-equals-recorded output for one fixture, and
   unavailable fine-tuning dependencies produce a recorded blocked arm rather than a proxy claim.

### `tinyfleet-expansion/report-and-review`

1. Package the publishable report schema, limitations, interpretation rules, weekly extension, and
   repo-onboarding checklist from the measured arms only.
2. Run independent review and reconcile every claim to a raw artifact; leave blocked work explicit.
3. Artifacts: report bundle, drift/close methodology, review receipt, claim-to-artifact matrix, and
   prioritized roadmap.
4. Verify: source/deployed parity where applicable, full focused test suite, checksum manifest, and
   independent reviewer PASS or a concrete failure record.

## Crypthauntology for Kids (`docs/plans/2026-09-07-crypthauntology-for-kids-expansion.md`) — owner `haunt`

### `crypthauntology-kids/protocol-lessons-gate`

1. Freeze the research contract and child-safety boundary.
2. Build age-banded safe lesson modules, glossary, facilitator guide, answer key, and content/safety
   gate with redacted fixtures.
3. Artifacts: versioned protocol/design manifest, lesson bundle, safety review, lint report, and
   mutation report.
4. Verify: lint and safety gate pass on valid fixtures, deliberate unsafe/content mutations fail,
   and no production study data is touched.

### `crypthauntology-kids/probes-and-offline-pilot`

1. Expand the probe matrix without broadening the claim; define canaries, graders, expected labels,
   and prompt-family split.
2. Run the offline pilot first and compare replay with live transcript while calculating denominators
   and minimum detectable effect per family.
3. Artifacts: canary registry, split manifest, pilot manifests, replay/live transcript, and power
   worksheet.
4. Verify: deterministic replay, holdout separation, expected-label grading, and a blocked verdict
   when a family lacks sufficient denominator.

### `crypthauntology-kids/adult-study-and-release`

1. Run the powered adult-only study only after the prior gate and pilot artifacts pass.
2. Publish the educational package, teacher guide, safety/version changelog, raw append-only tapes,
   hashes, holdout manifest, replay report, and witness review.
3. Artifacts: study bundle, release bundle, raw counts, checksum manifest, and witness report.
4. Verify: adult-only eligibility gate, append-only/hash checks, independent replay, and explicit
   close or blocked disposition for every acceptance criterion.

## Board dispatch contract

Each task is posted separately with its exact slug, owner, ordered dependency, artifact path under
the owning repository, and verification condition. A task is not complete on dispatch alone: the
owner must post `[taking]`, then `[done]` with the artifact and verification evidence (or
`[blocked]` with the missing dependency).
