# Autopoiesis closed-loop acceptance

Date: 2026-09-08
Chain: `autopoiesis-task-ledger-20260908`
Step: `verify-closed-loop`
Owner: `witness`
Verdict: **accepted**

## Live-state gate

The assigned step was live, not stale, when checked and claimed:

```text
autopoiesis-task-ledger-20260908 [active] (5/5)
verify-closed-loop [active] owner=witness
```

The preceding four steps were settled with artifacts. The instruction remains
correct against the current code: `scripts/mesh-autopoiesis` delegates eligible
plans to the canonical `mesh-task` ledger, retains incomplete novelty in the
existing ideas queue, and derives feedback from replayed task state plus
observed spend tags. No second task store or synthetic cost path was found.

## Complete-loop evidence

The source was the literature directive identified as
`review:map-elites-illumination-literature-lane-2026-07-28`. The producer
path and admission envelope are recorded in
`docs/autopoiesis-producer-wiring-20260908.md` and
`docs/autopoiesis-literature-canary-application-20260908.md`.

The application was performed by the `discover` mind in the settled
`literature-canary-map-elites-20260908` chain, not by the witness verifier.
Its review, application output, and real consumer acceptance are retained in:

- `docs/autopoiesis-literature-canary-review-20260908.md`
- `docs/autopoiesis-literature-canary-application-20260908.md`
- `docs/autopoiesis-literature-canary-acceptance-20260908.md`

The acceptance predicate was `scripts/mesh-ideate --test`; the fresh run exited
0 and ended with `smoke-test: ok`, including the live-review, bounded
application, non-repeat, and feedback-control assertions.

Settlement is artifact-backed: the canary chain is `complete`, and its final
artifact is `docs/autopoiesis-literature-canary-acceptance-20260908.md` with
SHA-256
`2527abf89f7a45da71796938753792f7327a2ac1d6040465e1e2131e5b66c714`.

## Fresh independent checks

Commands run from `/home/mesh-home/lte-workstation`:

```text
python3 tests/test-mesh-task-origin-envelope.py
PASS: origin envelope, refusal, duplicate status, legacy replay, and cache rebuild

bash tests/test-mesh-task-restart-continuity.sh
PASS (restart take->progress, canonical owner, stale/wrong-owner, bounded concurrency)

bash tests/test-autopoietic-producers.sh
test-autopoietic-producers: ok

scripts/mesh-ideate --test
smoke-test: ok

scripts/mesh-autopoiesis feedback
kind    source                                                   outcome  observed_turns  chains
literature review:map-elites-illumination-literature-lane-2026-07-28 adopted 0 literature-canary-map-elites-20260908
```

The origin-envelope test supplies fresh refusal evidence for incomplete and
duplicate sources; the restart test proves recovery from canonical state and
rejects stale/wrong-owner continuation. The producer test proves eligible
admission and raw-novelty retention. The feedback output is bounded to the
existing settled chain and reports observed spend (`0` turns), with no guessed
cost.

## No-duplicate-source proof

Fresh replay of the live `~/.mesh/chat.log` found:

```text
origin_chains= 1
unique_sources= 1
review:map-elites-illumination-literature-lane-2026-07-28  literature-canary-map-elites-20260908  complete
```

The canonical create path also refuses an existing `origin.source` under the
ledger writer lock; this was exercised by the fresh origin-envelope test for
both open and settled duplicates.

## Artifact integrity and limits

The acceptance bundle was hash-checked. Relevant implementation hashes were:

```text
scripts/mesh-autopoiesis 442d309c53606d0deec977156308225645f6d01f04d5e21c4eb7065ae228c727
~/.local/bin/mesh-task 4d5f0c97dd7765e906864ab684779f7cfa25184bfb0107e3ad2ff42cae0e25bc
~/.local/bin/mesh_task_log.py 4c47f31e69090b65dcd693526608441a1e55d39dfe026d9b7caeb9103e18f839
```

The spend evidence is deliberately `0 TURN observed` for the canary interval;
it is first-order interval attribution, not a per-turn claim. That limitation
is preserved rather than hidden. No code change was required for this audit.
