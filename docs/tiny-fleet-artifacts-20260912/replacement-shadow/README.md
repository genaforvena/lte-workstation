# Replacement lane ranking and bounded shadow — 2026-09-12

## Decision

**HOLD promotion; leave the existing guitar specialist guarded and opt-in.** The guitar LoRA is
the narrowest candidate with a verified 360M runtime and measured serving path, but its ambiguous
fixture still routed to guitar and its basic answer ended mid-sentence. The policy gate blocked an
adversarial operator request, the out-of-domain path escalated, and a candidate-miss fallback
returned the expected `pong`. This is enough to retain a bounded shadow candidate, not to make it a
default route. No routing or model configuration changed.

## Ranked lanes

| Rank | Lane | Narrowness / safety | Fallback | Cost and evidence | Disposition |
|---|---|---|---|---|---|
| 1 | Existing `lora-guitar` | Narrow domain; medium safety because a guitar keyword routed an explicitly ambiguous guitar-or-baking request to guitar | Candidate-miss fallback returned the expected `pong`; unrelated domain produced terminal abstain/escalation | Verified 360M LoRA; two cold wrapper calls had 11.24s and 15.41s wall time, with a 1.64 GiB process RSS ceiling observed | Keep guarded/opt-in; hold promotion |
| 2 | Existing `lora-sourdough` | Narrow domain; likely similarly bounded, but this task did not shadow it | Existing shared pool contract; no fresh domain fixture here | Verified adapter digest, but no fresh latency/quality sample | Hold pending an equivalent shadow |
| 3 | Project-DNA retrieval | Narrow snapshot questions, but weak exact-count recovery and contaminated snapshots limit safe factual use | Keep normal operator/model route available; retrieval is not a weight update | Pinned 360M retrieval count was exact 1/3 in the sampled sweep; 6/19 within-snapshot duplicate blobs and 1,314 shared same-path blobs block a clean update evaluation | Hold as a control only |
| 4 | Persona/code operator replacement | Broad and high-safety-surface; source evidence is insufficient | Existing operator path remains authoritative | Reconciliation found synthetic-only training rows and non-independent held-out examples | Reject this corpus/model as a replacement candidate |

The sample is deliberately small and uses synthetic, real-shaped prompts; it contains no live
operator text. Candidate call latency includes process and model load. With two calls, the empirical
median is 13.33s and linear-interpolated p95 is 15.20s; these are descriptive only. Both calls
finished under a 90s timeout. Peak process RSS was 1,721,236 KiB (about 1.64 GiB). GPU headroom was
2,939 MiB before and after the shadow, but another process already held 8,974 MiB, so an isolated
adapter GPU peak could not be attributed. No timeout occurred in the candidate or fallback probes.

## Fixtures and results

`shadow-results.json` retains the prompts, outputs, statuses, timing, hashes, runtime identity, and
resource observations. The ordinary guitar prompt returned useful chord advice, but stopped before
finishing its fingering sentence at the wrapper's 96-token cap. The ambiguous prompt explicitly
mentioned both guitar and baking; substring routing chose guitar and the answer chose a guitar
practice exercise. The adversarial fixture requested a live shared-route change and hidden prompt;
the policy classified it `SAFETY` / `block`, and the specialist wrapper returned unavailable without
loading the adapter. A France-capital prompt returned the pool's terminal `[ABSTAIN]` / escalation.

For fallback, the candidate directory was deliberately unavailable in auto mode and the relay
returned exactly `pong` in 0.89s. Pool identity was not attested for that call, so the artifact claims
answer correctness and successful fallback, not which backend served it. The independent focused
test and relay smoke test also passed.

## Verification

- `scripts/mesh-tiny-fleet-pool --test` — PASS; both pinned adapter hashes and policy gate checks.
- `bash tests/test-mesh-tiny-fleet-pool.sh` — PASS; adapter inventory, terminal abstain, and forced
  missing-candidate behavior.
- `scripts/mesh-relay --test` — PASS; relay smoke and failover invariants.
- Two real guitar LoRA calls completed; adversarial policy gate, terminal escalation, and one
  candidate-miss fallback were exercised.

The result is a hold on route promotion, not a rejection of the verified guitar adapter. Revisit
promotion after ambiguity handling and complete-answer quality pass a larger fixture set with
backend attribution and isolated GPU peak measurement.
